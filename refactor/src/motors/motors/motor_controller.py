from time import sleep                              # Sleep
import rclpy                                        # ROS2 Python Client Library
from rclpy.node import Node                         # ROS2 Node
from sensor_msgs.msg import Joy                     # ROS2 standard Joy Message
from share.msg import SendCAN0                      # ROS2 custom SendCAN0 Message
from .motor_instruct import *                       # Motor Instruction
from std_msgs.msg import Float32                    # ROS2 standard Float32 Message
import math                                         # Math Library

#  Light Control Instructions
head_lamp_on =          b'\x68\x09\x00\xFF\x12\x00\x01\x12\x16'
head_lamp_off =         b'\x68\x09\x00\xFF\x12\x00\x00\x11\x16'
daytime_lamp_on =       b'\x68\x09\x00\xFF\x12\x03\x01\x15\x16'
daytime_lamp_off =      b'\x68\x09\x00\xFF\x12\x03\x00\x14\x16'
left_turing_lamp_on =   b'\x68\x09\x00\xFF\x12\x01\x01\x13\x16'
left_turing_lamp_off =  b'\x68\x09\x00\xFF\x12\x01\x00\x12\x16'
right_turing_lamp_on =  b'\x68\x09\x00\xFF\x12\x02\x01\x14\x16'
right_turing_lamp_off = b'\x68\x09\x00\xFF\x12\x02\x00\x13\x16'
stop_lamp_on =          b'\x68\x09\x00\xFF\x12\x04\x01\x16\x16'
stop_lamp_off =         b'\x68\x09\x00\xFF\x12\x04\x00\x15\x16'


#  Motor Control Class
class MotorController(Node):

    # Motor Control Variables
    switch_mode = [False, False, False]                     #  [last right_shoulder_button, current right_shoulder_button, False:Auto True:Manual]
    clear_encoder = [False, False, False]                   #  [last b_button, current b_button, if clear encoder]
    parking_mode = [False, False, False, False]             #  [last left_shoulder_button, current left_shoulder_button, parking_mode, if parking_mode]
    emerg_stop = [False, False, False]                      #  [last x_button, current x_button, emerg_stop]
    combo_lamp = [False, False, 0, 0]                       #  [head light, daytime running light, last dpad_y, current dpad_y]
    turing_lamp = [False, False, False, 0, 0, False, False] #  [left turing lamp, right turing lamp, emerg_lamp, last dpad_x, current dpad_x, last select_button, current select_button]
    stop_lamp = False                                       #  stop lamp
    free_stop = [False, False, False]                       #  [last y_button, current y_button, free_stop]
    gear = 0                                                #  0:Neutral, 1:Forward I, 2:Forward II, -1:Reverse I
    switch_gear = [False, False]                            #  [last a_button, current a_button]
    throttle = 0                                            #  Throttle (right_trigger)
    brake = 0                                               #  Brake (left_trigger)
    orientation = 0                                         #  Turning (left_joy_x)
    if_stop = False                                         #  If stop
    lwheel_freq = 0                                         #  Left Wheel Frequency
    rwheel_freq = 0                                         #  Right Wheel Frequency
    joy_input = {                                           #  Joy Input
            'left_joy_x'            : 0  ,
            'left_joy_y'            : 0  ,
            'right_joy_x'           : 0  ,
            'right_joy_y'           : 0  ,
            'dpad_x'                : 0  ,
            'dpad_y'                : 0  ,
            'left_trigger'          : 1  ,
            'right_trigger'         : 1  ,
            'left_shoulder_button'  : 0  ,
            'right_shoulder_button' : 0  ,
            'a_button'              : 0  ,
            'b_button'              : 0  ,
            'x_button'              : 0  ,
            'y_button'              : 0  ,
            'select_button'         : 0  ,
            'start_button'          : 0  ,
            'xbox_button'           : 0  ,
            'left_joy_button'       : 0  ,
            'right_joy_button'      : 0  
    }


    #  Motor Control Constructor
    def __init__(self,name):
        super().__init__(name)

        #  Subscribe xbox controller input
        self.sub_joy = self.create_subscription(
            Joy, 
            "joy", 
            self.joy_recv, 
            10)
        
        #  Subscribe left wheel frequency
        self.sub_lwheel = self.create_subscription(
            Float32, 
            "lwheel_vtarget", 
            self.lwheel_recv, 
            10)
        
        #  Subscribe right wheel frequency
        self.sub_rwheel = self.create_subscription(
            Float32, 
            "rwheel_vtarget", 
            self.rwheel_recv, 
            10)

        #  Publish CAN0 instructions
        self.pub_can = self.create_publisher(
            SendCAN0,
            'send_can0',
            20)
        
        #  Create timer to process inputs
        self.timer = self.create_timer(0.005, self.timer_callback)


    #  Convert left wheel speed (m/s) to frequency (Hz)
    def lwheel_recv(self, lwheel_vtarget):
        self.lwheel_freq = self.speed2freq(lwheel_vtarget.data)


    #  Convert right wheel speed (m/s) to frequency (Hz)
    def rwheel_recv(self, rwheel_vtarget):  
        self.rwheel_freq = self.speed2freq(rwheel_vtarget.data)


    #  Converting speed (m/s) into wheel rotation (rpm)
    def speed2freq(self, speed):
        wheel_diameter = 285                    #  Measured diameter (mm) of the wheel
        perimeter = wheel_diameter * math.pi    #  Calculate the perimeter (mm) of the wheel
        rpm = speed * 1000 * 60 / perimeter     #  Calculate the rotation speed (rpm) of the wheel
        freq = rpm * 5 * 10                     #  Calculate the rotation frequency (Hz) of the wheel
        return freq


    #  Store xbox controller input
    def joy_recv(self, joy):
            self.joy_input['left_joy_x']            = -joy.axes[0]    
            self.joy_input['left_joy_y']            =  joy.axes[1]    
            self.joy_input['right_joy_x']           = -joy.axes[2]    
            self.joy_input['right_joy_y']           =  joy.axes[3]    
            self.joy_input['dpad_x']                = -joy.axes[6]    
            self.joy_input['dpad_y']                =  joy.axes[7]    
            self.joy_input['left_trigger']          = -joy.axes[5]    
            self.joy_input['right_trigger']         = -joy.axes[4]    
            self.joy_input['left_shoulder_button']  =  joy.buttons[6] 
            self.joy_input['right_shoulder_button'] =  joy.buttons[7] 
            self.joy_input['a_button']              =  joy.buttons[0] 
            self.joy_input['b_button']              =  joy.buttons[1]   
            self.joy_input['x_button']              =  joy.buttons[3] 
            self.joy_input['y_button']              =  joy.buttons[4] 
            self.joy_input['select_button']         =  joy.buttons[15]
            self.joy_input['start_button']          =  joy.buttons[11]
            self.joy_input['xbox_button']           =  joy.buttons[16]
            self.joy_input['left_joy_button']       =  joy.buttons[13]
            self.joy_input['right_joy_button']      =  joy.buttons[14]


    #  Send CAN0 instructions
    def can_send(self, left_frame_data, right_frame_data):
        msg = SendCAN0()
        msg.left_motor_data = left_frame_data
        msg.right_motor_data = right_frame_data
        self.pub_can.publish(msg)


    #  Reset gear when entering manual mode
    def reset_gear(self):
        self.gear = 0                                    
        self.switch_gear = [False, False]                
        self.throttle = 0                               
        self.brake = 0                                               
        self.orientation = 0 
        self.get_logger().info('Gear: 0')



    #  Process universal status
    def status_processor(self):
        #  Switch Control Mode
        self.switch_mode[0] = self.switch_mode[1]
        self.switch_mode[1] = bool(self.joy_input['right_shoulder_button'])
        if not self.switch_mode[0] and self.switch_mode[1]:
            self.switch_mode[2] = not self.switch_mode[2]
            if self.switch_mode[2]:
                self.get_logger().info('Switch to Manual Mode')
                self.reset_gear()
            else:
                self.get_logger().info('Switch to Auto Mode')
        
        #  Clear Encoder
        self.clear_encoder[0] = self.clear_encoder[1]
        self.clear_encoder[1] = bool(self.joy_input['b_button'])
        if not self.clear_encoder[0] and self.clear_encoder[1]:
            self.clear_encoder[2] = True
            self.can_send(ResetPosition(), ResetPosition())
            self.get_logger().info('Clear Encoder')
        else:
            self.clear_encoder[2] = False

        #  Parking Mode
        self.parking_mode[0] = self.parking_mode[1]
        self.parking_mode[1] = bool(self.joy_input['left_shoulder_button'])
        if not self.parking_mode[0] and self.parking_mode[1]:
            self.parking_mode[2] = not self.parking_mode[2]
            if self.parking_mode[2]:
                self.get_logger().info('Switch to Parking Mode')
            else:
                self.get_logger().info('Switch to Normal Mode')
        
        #  Emergency Stop
        self.emerg_stop[0] = self.emerg_stop[1]
        self.emerg_stop[1] = bool(self.joy_input['x_button'])
        if not self.emerg_stop[0] and self.emerg_stop[1]:
            self.emerg_stop[2] = True
            self.get_logger().info('Emergency Stop')
        else:
            self.emerg_stop[2] = False

        #  Free Stop
        self.free_stop[0] = self.free_stop[1]
        self.free_stop[1] = bool(self.joy_input['y_button'])
        if not self.free_stop[0] and self.free_stop[1]:
            self.free_stop[2] = True
            self.get_logger().info('Free Stop')
        else:
            self.free_stop[2] = False

        #  Combo Lamp
        self.combo_lamp[2] = self.combo_lamp[3]
        self.combo_lamp[3] = self.joy_input['dpad_y']
        if self.combo_lamp[2:3] == [0, 1]:
            self.combo_lamp[0] = not self.combo_lamp[0]
        if self.combo_lamp[2:3] == [0, -1]:
            self.combo_lamp[1] = not self.combo_lamp[1]

        #  Emergency Lamp
        self.turing_lamp[5] = self.turing_lamp[6]
        self.turing_lamp[6] = bool(self.joy_input['select_button'])
        if not self.turing_lamp[5] and self.turing_lamp[6]:
            self.turing_lamp[2] = not self.turing_lamp[2]
            if self.turing_lamp[2]:
                self.get_logger().info('Turn Emergency Lamp On')
            else:
                self.get_logger().info('Turn Emergency Lamp Off')

        

        
    # Process Xbox Controller input and speed instructions
    def timer_callback(self):
        self.status_processor()
        #  If the vehicle is in parking mode
        if self.parking_mode[2]:
            if not self.parking_mode[3]:
                self.parking_mode[3] = True
                self.can_send(MotorMode('Position Control'), MotorMode('Position Control'))
                self.can_send(PositionType('Relative Position'), PositionType('Relative Position'))
            self.can_send(TargetPosition(0), TargetPosition(0))
        else:
            self.parking_mode[3] = False
            
            #  If emergency stop is activated
            if self.emerg_stop[2]:
                self.can_send(MotorMode('Emergency Stop'), MotorMode('Emergency Stop'))
                self.if_stop = True
            else:
                if self.free_stop[2]:
                    self.can_send(MotorMode('Free Stop'), MotorMode('Free Stop'))
                    self.if_stop = True
                else:
                    #  If the vehicle is in manual mode
                    if self.switch_mode[2]:                        
                        self.manual_mode()
                    #  If the vehicle is in auto mode
                    else:
                        self.auto_mode()


    def manual_mode(self):
        self.throttle = self.joy_input['right_trigger']
        self.brake = self.joy_input['left_trigger']
        self.orientation = self.joy_input['left_joy_x']

        self.switch_gear[0] = self.switch_gear[1]
        self.switch_gear[1] = bool(self.joy_input['a_button'])
        if not self.switch_gear[0] and self.switch_gear[1]:
            if self.gear == 2:
                self.gear = -1
            else:
                self.gear += 1
            self.get_logger().info('Gear: ' + str(self.gear))
        
        if self.gear == 0:
            self.can_send(MotorMode('Free Stop'), MotorMode('Free Stop'))
            self.if_stop = True
        else:
            if self.if_stop:
                self.can_send(MotorMode('Speed Control'), MotorMode('Speed Control'))
                self.if_stop = False

            #  Actually here rpm means the current switching frequency of the motor
            rpm_factor, rpm_turning_factor = 0, 0
            if self.gear == 1:
                rpm_factor = self.speed2freq(1)
                rpm_turning_factor = 100
            elif self.gear == 2:
                rpm_factor = self.speed2freq(2)
                rpm_turning_factor = 75
            elif self.gear == -1:
                rpm_factor = -self.speed2freq(1)
                rpm_turning_factor = 100
            rpm = rpm_factor * (self.throttle + 1) * 0.5
            left_rpm = - (rpm - (- self.orientation * rpm_turning_factor))
            right_rpm =   rpm + (- self.orientation * rpm_turning_factor)
            self.can_send(RPMControl(left_rpm), RPMControl(right_rpm))


    def auto_mode(self):
        if self.if_stop:
            self.can_send(MotorMode('Speed Control'), MotorMode('Speed Control'))
            self.if_stop = False
        self.can_send(RPMControl(-self.lwheel_freq), RPMControl(self.rwheel_freq))


def main(args=None):
    rclpy.init(args=args)
    node = MotorController('motor_controller')
    rclpy.spin(node)
    node.destory_node()
    rclpy.shutdown()
