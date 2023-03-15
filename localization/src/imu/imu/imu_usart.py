import rclpy                                     # ROS2 Python Client Library
from rclpy.node import Node                      # ROS2 Node
from sensor_msgs.msg import Imu

# Usart Library
import serial
import struct
import binascii

'''
    Author: Liu Yuxiang 
    Time: 2022.12.13
    description: IMU底层串口收发代码
'''


# imu接收数据类型
class IMU(Node):
    send_data = []
    def __init__(self):
        super().__init__('imu_publisher')
        self.publisher_ = self.create_publisher(Imu, 'imu_data', 1)

        # 串口初始化
        self.IMU_Usart = serial.Serial(
            port = '/dev/tty_imu',      # 串口
            #port = '/dev/ttyUSB0',
            baudrate=115200,            # 波特率
            timeout = 0.001             # 由于后续使用read_all按照一个timeout周期时间读取数据
                                        # imu在波特率115200返回数据时间大概是1ms,9600下大概是10ms
                                        # 所以读取时间设置0.001s
        )
        # 接收数据初始化
        self.ACC_X:float = 0.0                   # X轴加速度
        self.ACC_Y:float = 0.0                   # Y轴加速度
        self.ACC_Z:float  =  0.0                 # Z轴加速度
        self.GYRO_X :float = 0.0                 # X轴陀螺仪
        self.GYRO_Y :float = 0.0                 # Y轴陀螺仪
        self.GYRO_Z :float = 0.0                 # Z轴陀螺仪
        self.roll :float = 0.0                   # 横滚角    
        self.pitch :float = 0.0                  # 俯仰角
        self.yaw :float = 0.0                    # 航向角
        self.leve :float = 0.0                   # 磁场校准精度
        self.temp :float = 0.0                   # 器件温度
        self.MAG_X :float = 0.0                  # 磁场X轴
        self.MAG_Y :float = 0.0                  # 磁场Y轴
        self.MAG_Z :float = 0.0                  # 磁场Z轴
        self.Q0 :float = 0.0                     # 四元数Q0.0
        self.Q1 :float = 0.0                     # 四元数Q1
        self.Q2 :float = 0.0                     # 四元数Q2
        self.Q3 :float = 0.0                     # 四元数Q3
        # 判断串口是否打开成功
        if self.IMU_Usart.isOpen():
            print("open success")
        else:
            print("open failed")

        # 回调函数返回周期
        time_period = 0.001         
        self.timer = self.create_timer(time_period, self.timer_callback)

        # 发送读取指令
        self.Send_ReadCommand()

    def Send_ReadCommand(self):
        '''
        Author: Liu Yuxiang 
        Time: 2022.12.13
        description: 发送读取IMU内部数据指令
        · 第一个寄存器0x08 最后一个读取寄存器0x2A 共35个
        · 读寄存器例子,读取模块内部温度,主站发送帧为:A4 03 1B 02 C4
            |   A4    |    03    |    1B   |     02    |    C4
            |  帧头ID  | 读功能码 |起始寄存器| 寄存器数量 |校验和低 8 位
        '''
        # 使用优雅的方式发送串口数据
        send_data = [0xA4,0x03,0x08,0x23,0xD2]                      #需要发送的串口包
        #send_data = [0xA4,0x03,0x08,0x1B,0xCA]                      #需要发送的串口包
        send_data=struct.pack("%dB"%(len(send_data)),*send_data)    #解析成16进制
        print(send_data)
        self.IMU_Usart.write(send_data)                             #发送

    def Read_data(self):
        '''
        Author: Liu Yuxiang 
        Time: 2022.12.13
        description: 读取IMU数据
        '''
        # 初始化数据
        counter = 0 
        Recv_flag = 0
        Read_buffer = []
        # 接收数据至缓存区
        Read_buffer=self.IMU_Usart.read(40)         # 我们需要读取的是40个寄存器数据，即40个字节
        # 状态机判断收包数据是否准确
        while(1):
            # 第1帧是否是帧头ID 0xA4
            if (counter == 0):
                if(Read_buffer[0] != 0xA4):
                    break    

            # 第2帧是否是读功能码 0x03  
            elif (counter == 1):
                if(Read_buffer[1] != 0x03):
                    counter=0
                    break

            # 第3帧判断起始帧        
            elif (counter == 2):
                if(Read_buffer[2] < 0x2c):
                    start_reg=Read_buffer[2]
                else:
                    counter=0 

            # 第4帧判断帧有多少数量 
            elif (counter == 3):
                if((start_reg+Read_buffer[3]) < 0x2C): # 最大寄存器为2C 大于0x2C说明数据肯定错了
                    len=Read_buffer[3]
                else:
                    counter=0
                    break                  
                 
            else:
                if(len+5==counter):
                    #print('Recv done!')
                    Recv_flag=1

            # 收包完毕
            if(Recv_flag):
                Recv_flag = 0
                sum = 0
                #print(Read_buffer)                                 # Read_buffer中的是byte数据字节流，用struct包解包
                data_inspect = str(binascii.b2a_hex(Read_buffer))   # data是将数据转化为原本的按照16进制的数据

                try:        # 如果接收数据无误，则执行数据解算操作
                    for i in range(2,80,2):                 # 根据手册，检验所有帧之和低八位是否等于末尾帧
                            sum += int(data_inspect[i:i+2],16)

                    if (str(hex(sum))[-2:] == data_inspect[80:82]): # 如果数据检验没有问题，则进入解包过程
                        #print('the Rev data is right')
                        
                        # 数据低八位在前，高八位在后
                        #print(Read_buffer[4:-1])                       
                        unpack_data = struct.unpack('<hhhhhhhhhBhhhhhhhh',Read_buffer[4:-1])
                        # 切片并将其解析为我们所需要的数据，切出我们所需要的数据部分
                        g = 9.8
                        
                        self.ACC_X  = unpack_data[0]/2048 * g       # unit m/s^2
                        self.ACC_Y  = unpack_data[1]/2048 * g    
                        self.ACC_Z  = unpack_data[2]/2048 * g
                        self.GYRO_X = unpack_data[3]/16.4           # unit 度/s
                        self.GYRO_Y = unpack_data[4]/16.4                
                        self.GYRO_Z = unpack_data[5]/16.4                     
                        self.roll   = unpack_data[6]/100                
                        self.pitch  = unpack_data[7]/100                 
                        self.yaw    = unpack_data[8]/100                          
                        self.level  = unpack_data[9]
                        self.temp   = unpack_data[10]/100 
                        self.MAG_X  = unpack_data[11]/1000          # unit Gaos             
                        self.MAG_Y  = unpack_data[12]/1000           
                        self.MAG_Z  = unpack_data[13]/1000
                        self.Q0     = unpack_data[14]/10000        
                        self.Q1     = unpack_data[15]/10000                 
                        self.Q2     = unpack_data[16]/10000                 
                        self.Q3     = unpack_data[17]/10000
                        #print(self.__dict__) 
                except:
                    print("Have Error in receiving data!!")
                counter=0               
                break
            else:
                counter += 1                        # 遍历整个接收数据的buffer
        
    def timer_callback(self):

        # ----读取IMU的内部数据-----------------------------------
        try:
            count = self.IMU_Usart.inWaiting()
            if count > 0:
                self.Read_data()
                

                # 发布sensor_msgs/Imu 数据类型
                # imu_data = Imu()
                # imu_data.header.frame_id = "imu_link"
                # imu_data.header.stamp = self.get_clock().now().to_msg()
                # imu_data.linear_acceleration.x = self.ACC_X
                # imu_data.linear_acceleration.y = self.ACC_Y
                # imu_data.linear_acceleration.z = self.ACC_Z
                # imu_data.angular_velocity.x = self.GYRO_X * 3.1415926 / 180.0  # unit transfer to rad/s
                # imu_data.angular_velocity.y = self.GYRO_Y * 3.1415926 / 180.0
                # imu_data.angular_velocity.z = self.GYRO_Z * 3.1415926 / 180.0
                # imu_data.orientation.x = self.Q0
                # imu_data.orientation.y = self.Q1
                # imu_data.orientation.z = self.Q2
                # imu_data.orientation.w = self.Q3
                # self.publisher_.publish(imu_data)             # 发布imu的数据

                # --------------------------------------------------------
                #print('读取中')
            imu_data = Imu()
            imu_data.header.frame_id = "imu_link"
            imu_data.header.stamp = self.get_clock().now().to_msg()
            imu_data.linear_acceleration.x = self.ACC_Z  # 将x和z轴交换
            imu_data.linear_acceleration.y = self.ACC_Y
            imu_data.linear_acceleration.z = self.ACC_X
            imu_data.angular_velocity.x = self.GYRO_Z * 3.1415926 / 180.0  # 将x和z轴交换，并转换为弧度/秒
            imu_data.angular_velocity.y = self.GYRO_Y * 3.1415926 / 180.0
            imu_data.angular_velocity.z = self.GYRO_X * 3.1415926 / 180.0
            imu_data.orientation.x = -self.Q2  # 将x和z轴交换，并修改方向四元数
            imu_data.orientation.y = self.Q1
            imu_data.orientation.z = -self.Q0
            imu_data.orientation.w = self.Q3
            self.publisher_.publish(imu_data)  # 发布imu的数据


        except KeyboardInterrupt:
            if serial != None:
                print("close serial port")
                self.IMU_Usart.close()
        
        #--------------------------------------------------------



def main(args=None):

    # 变量初始化---------------------------------------------    
    rclpy.init(args=args)
    IMU_node = IMU()
    rclpy.spin(IMU_node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()


'''
░░░░░░░░░░░░░░░░░░░░░░░░▄░░
░░░░░░░░░▐█░░░░░░░░░░░▄▀▒▌░
░░░░░░░░▐▀▒█░░░░░░░░▄▀▒▒▒▐░
░░░░░▄▄▀▒░▒▒▒▒▒▒▒▒▒█▒▒▄█▒▐░
░░░▄▀▒▒▒░░░▒▒▒░░░▒▒▒▀██▀▒▌░
░░▐▒▒▒▄▄▒▒▒▒░░░▒▒▒▒▒▒▒▀▄▒▒░
░░▌░░▌█▀▒▒▒▒▒▄▀█▄▒▒▒▒▒▒▒█▒▐
░▐░░░▒▒▒▒▒▒▒▒▌██▀▒▒░░░▒▒▒▀▄
░▌░▒▄██▄▒▒▒▒▒▒▒▒▒░░░░░░▒▒▒▒
▀▒▀▐████▌▄░▀▒▒░░░░░░░░░░▒▒▒
狗狗保佑代码无bug！
'''
