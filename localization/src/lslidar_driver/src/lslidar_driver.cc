/*
 * This file is part of lslidar driver.
 *
 * The driver is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * The driver is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with the driver.  If not, see <http://www.gnu.org/licenses/>.
 */
#include <string>
#include <cmath>
#include <unistd.h>
#include <sys/socket.h>
#include <sys/time.h>
#include <arpa/inet.h>
#include <poll.h>
#include <errno.h>
#include <fcntl.h>
#include <sys/file.h>
#include <stdio.h>
#include <stdlib.h>
 
#include "rclcpp/rclcpp.hpp"
#include "lslidar_driver/lslidar_driver.h"
#include <functional>

int angle_min[]={135}; 	//雷达屏蔽角度，这里屏蔽角度为135°到225°，
                        //如果要多角度屏蔽，如10~30，50~60，改为：angle_min[]={10，50};angle_max[]={30，60};
int angle_max[]={225};  //修改后编译即可
namespace lslidar_driver {

static void my_hander(int sig)
{
    printf("sig: %d",sig);
	abort();
}
LslidarDriver::LslidarDriver() : LslidarDriver(rclcpp::NodeOptions()) {}
LslidarDriver::LslidarDriver(const rclcpp::NodeOptions& options) : 
    Node("lslidar_driver_node", options), diagnostics(this)
{
	signal(SIGINT, my_hander);
	
	if (!this->initialize()) 
		RCLCPP_ERROR(this->get_logger(), "Could not initialize the driver...");
	else
		RCLCPP_INFO(this->get_logger(), "Successfully initialize driver...");
}

LslidarDriver::~LslidarDriver() {
    return;
}

bool LslidarDriver::loadParameters() {
    pubscan_thread_ = new boost::thread(boost::bind(&LslidarDriver::pubScanThread, this));
	interface_selection = std::string("net");
	frame_id = std::string("laser_link");
    scan_topic = std::string("/scan");
	lidar_name = std::string("M10");
	is_start = true;
    min_range = 0.3;
    max_range = 100.0;
	use_gps_ts = true;
    angle_disable_min = 0.0;
    angle_disable_max = 0.0;
    truncated_mode_ = 0;


	this->declare_parameter<std::string>("lidar_name","M10");
	this->declare_parameter<std::string>("frame_id","laser_link");
	this->declare_parameter<std::string>("scan_topic","/scan");
	this->declare_parameter<double>("min_range",0.3);
	this->declare_parameter<double>("max_range",100.0);
	this->declare_parameter<bool>("use_gps_ts",false);
	this->declare_parameter<double>("angle_disable_min",0.0);
	this->declare_parameter<double>("angle_disable_max",0.0);
	this->declare_parameter<std::string>("interface_selection","net");
	this->declare_parameter<int>("truncated_mode_",0);

	this->get_parameter("lidar_name", lidar_name);
	this->get_parameter("frame_id", frame_id);
	this->get_parameter("scan_topic", scan_topic);
	this->get_parameter("min_range", min_range);
	this->get_parameter("max_range", max_range);
	this->get_parameter("use_gps_ts", use_gps_ts);
	this->get_parameter("angle_disable_min", angle_disable_min);
	this->get_parameter("angle_disable_max", angle_disable_max);
	this->get_parameter("interface_selection", interface_selection);
	this->get_parameter("truncated_mode_", truncated_mode_);

    while(angle_disable_min<0)	angle_disable_min+=360;
    while(angle_disable_max<0)	angle_disable_max+=360;
    while(angle_disable_min>360)	angle_disable_min-=360;
    while(angle_disable_max>360)	angle_disable_max-=360;
    if(angle_disable_max == angle_disable_min ){
        angle_able_min = 0;
        angle_able_max = 360;
    }
    else{
        if(angle_disable_min<angle_disable_max && angle_disable_min !=0.0){
            angle_able_min = angle_disable_max;
            angle_able_max = angle_disable_min+360;
        }
        if (angle_disable_min<angle_disable_max && angle_disable_min == 0.0){
            angle_able_min = angle_disable_max;
            angle_able_max = 360;
        }
        if (angle_disable_min>angle_disable_max ){
            angle_able_min = angle_disable_max;
            angle_able_max = angle_disable_min;
        }
    }
    count_num = 0;

    scan_points_.resize(4000);
        
    if (lidar_name == "M10"){
        use_gps_ts = false;
        PACKET_SIZE = 92;
        package_points = 42;
        data_bits_start = 6;
        degree_bits_start = 2;
        rpm_bits_start = 4;
        baud_rate_= 460800;
        points_size_ = 1008;
        printf("Lidar is M10 \n");
    }
    else if (lidar_name == "M10_P"){
        PACKET_SIZE = 160;
        package_points = 70;
        data_bits_start = 8;
        degree_bits_start = 4;
        rpm_bits_start = 6;
        baud_rate_=500000;
        points_size_ = 2000;
        printf("Lidar is M10_P \n");
    }
    else if (lidar_name == "M10_PLUS")
    {
        PACKET_SIZE = 104;
        package_points = 41;
        data_bits_start = 8;
        degree_bits_start = 4;
        rpm_bits_start = 6;
        points_size_ = 4000;
        baud_rate_=921600;
        printf("Lidar is M10_PLUS ! \n");
    }
    else if (lidar_name == "M10_TEST")
    {
        PACKET_SIZE = 176;
        package_points = 84;
        data_bits_start = 6;
        degree_bits_start = 2;
        rpm_bits_start = 4;
        baud_rate_= 460800;
        points_size_ = 2000; 
        use_gps_ts = false;
        printf("Lidar is M10 10K 5HZ \n");
    }
    else if (lidar_name == "N10")
    {
        PACKET_SIZE = 58;
        package_points = 16;
        data_bits_start = 7;
        degree_bits_start = 5;
        end_degree_bits_start = 55;
        baud_rate_= 230400;
        points_size_ = 2000; 
        use_gps_ts = false;
        printf("Lidar is N10 ! \n");
    }
    else if (lidar_name == "M10_GPS"){
        PACKET_SIZE = 102;
        package_points = 42;
        data_bits_start = 6;
        degree_bits_start = 2;
        rpm_bits_start = 4;
        baud_rate_= 460800;
        points_size_ = 1008;
        printf("Lidar is M10_GPS \n");
    }

    scan_pub = this->create_publisher<sensor_msgs::msg::LaserScan>(scan_topic, 10);	
	difop_switch = this->create_subscription<std_msgs::msg::Int8>("lslidar_order",1 ,std::bind(&LslidarDriver::lidar_order,this,std::placeholders::_1));          //转速输入
	return true;
}

void LslidarDriver::lidar_order(const std_msgs::msg::Int8::SharedPtr msg) {
    int i = msg->data;
    if( i == 0) is_start = false;
    else        is_start = true;
    if(interface_selection == "net") msop_input_->UDP_order(*msg);
    else{
        int i = msg->data;
    for(int k = 0 ; k <10 ; k++)
    {   
		int rtn;
        unsigned char data[188]= {0x00};
        data[0] = 0xA5;
        data[1] = 0x5A;
        data[2] = 0x55;
        data[186] = 0xFA;
        data[187] = 0xFB;

		if(lidar_name == "M10" || lidar_name == "M10_TEST" || lidar_name == "M10_GPS"){
            if (i <= 1){				    //雷达启停
				data[184] = 0x01;
				data[185] = char(i);
			}
			else if (i == 2){			    //雷达点云不滤波
				data[181] = 0x0A;
				data[184] = 0x06;
				if(is_start) data[185] = 0x01;
			}
			else if (i == 3){				//雷达点云正常滤波
				data[181] = 0x0B;
				data[184] = 0x06;
				if(is_start) data[185] = 0x01;
			}
			else if (i == 4){				//雷达近距离滤波
				data[181] = 0x0C;
				data[184] = 0x06;
				if(is_start) data[185] = 0x01;
			}       
            else return; 
		}
		else if(lidar_name == "M10_P"){
            if(i <= 1){
            data[185] = char(i);
            data[184] = 0x01;
            }
            else return;
		}
		else if (lidar_name == "M10_PLUS"){
            data[184] = 0x0A;
            data[185] = 0x01;
            if(i == 5)       {
            data[141] = 0x01;
            data[142] = 0x2c;
            }
            else if(i == 6)  {
            data[141] = 0x01;
            data[142] = 0x68;
            }
            else if(i == 8)  {
            data[141] = 0x01;
            data[142] = 0xe0;
            }
            else if(i == 10) {
            data[141] = 0x02;
            data[142] = 0x58;
            }
            else if(i == 12) {
            data[141] = 0x02;
            data[142] = 0xd0;
            }
            else if(i == 15) {
            data[141] = 0x03;
            data[142] = 0x84;
            }
            else if(i == 20) {
            data[141] = 0x04;
            data[142] = 0xb0;
            }
            else if(i <= 1)  {
            data[184] = 0x01;
            data[185] = char(i);
            }			
            else return; 
		}
		else if(lidar_name == "N10"){
            if(i <= 1){
            data[185] = char(i);
            data[184] = 0x01;
            }
            else if(i>=6 && i<=12){
            data[172] = char(i);
            data[184] = 0x0a;
            data[185] = 0X01;
            }
            else return; 
		}
        rtn= serial_->send((const char*)data, 188);
        printf("rtn = %d\n",rtn);
		if (rtn < 0)
			printf("start scan error !\n");
        else{
            if(i == 1)  usleep(1000000);     //1.0s
            
            if(i == 0)  is_start = false;
            if(i == 1)  is_start = true;
            return ;
        }   
    }
    return ;
    }
}

void LslidarDriver::open_serial()
{
        diagnostics.setHardwareID("Lslidar");

    int code = 0;
    serial_port_ = std::string("/dev/ttyUSB0");
    this->declare_parameter<std::string>("serial_port_","/dev/ttyUSB0");
    this->get_parameter("serial_port_", serial_port_);
    serial_ = LSIOSR::instance(serial_port_, baud_rate_);
    code = serial_->init();
    if(code != 0)
    {
        printf("open_port %s ERROR !\n", serial_port_.c_str());
        rclcpp::shutdown();
        exit(0);
    }
    printf("open_port %s  OK !\n", serial_port_.c_str());
}

bool LslidarDriver::createRosIO() {
    UDP_PORT_NUMBER = 2368;
    this->declare_parameter<int>("msop_port",2368);
    this->get_parameter("msop_port", UDP_PORT_NUMBER);
    RCLCPP_INFO_STREAM(this->get_logger(), "Opening UDP socket: port " << UDP_PORT_NUMBER);
    dump_file = std::string("");
    this->declare_parameter<std::string>("pcap","");
    this->get_parameter("pcap", dump_file);
    // ROS diagnostics
    diagnostics.setHardwareID("Lslidar");

    const double diag_freq = 12*24;
    diag_max_freq = diag_freq;
    diag_min_freq = diag_freq;
    RCLCPP_INFO(this->get_logger(), "expected frequency: %.3f (Hz)", diag_freq);

    using namespace diagnostic_updater;
        diag_topic.reset(new TopicDiagnostic(
                        "lslidar_packets", diagnostics,
                        FrequencyStatusParam(&diag_min_freq, &diag_max_freq, 0.1, 10),
                        TimeStampStatusParam()));

	int hz = 10;
    if (lidar_name == "M10_P")  hz = 12;
    else if (lidar_name == "M10_PLUS")  hz = 20;
    
	double packet_rate = hz*24;
    if(dump_file !="")
    {
        msop_input_.reset(new lslidar_driver::InputPCAP(this,UDP_PORT_NUMBER,packet_rate,dump_file));
    }else{
        msop_input_.reset(new lslidar_driver::InputSocket(this,UDP_PORT_NUMBER));

    }
	
    // Output
	return true;
}

int LslidarDriver::getScan(std::vector<ScanPoint> &points, rclcpp::Time &scan_time, float &scan_duration)
{
  boost::unique_lock<boost::mutex> lock(mutex_);
  points.assign(scan_points_bak_.begin(), scan_points_bak_.end());
  scan_time = pre_time_;
  scan_duration = time_.seconds()-pre_time_.seconds();
  return 1;
}

uint64_t LslidarDriver::get_gps_stamp(struct tm t){

   uint64_t ptime =static_cast<uint64_t>(timegm(&t));
   return ptime;
}

bool LslidarDriver::initialize() {
    if (!loadParameters()) {
        RCLCPP_ERROR(this->get_logger(), "Cannot load all required ROS parameters...");
        return false;
    }
    if(interface_selection == "net"){
        if (!createRosIO()) {
            RCLCPP_ERROR(this->get_logger(), "Cannot create all ROS IO...");
            return false;
        }
    }
    else
    {
        open_serial();
    }
    RCLCPP_INFO(this->get_logger(), "Initialised lslidar without error");
    return true;
}

void LslidarDriver::recvThread_crc(int &count,int &link_time)
{
	if(count <= 0) 
		link_time++;
	else
		link_time = 0;
	
	if(link_time > 150)
	{
		serial_->close();
		int ret = serial_->init();
		if(ret < 0)
		{
            RCLCPP_ERROR(this->get_logger(),"serial open fail");
			usleep(200000);
		}
		link_time = 0;
	}
}

int LslidarDriver::receive_data(unsigned char *packet_bytes){
    int link_time = 0;
    int q = 0;
    int len_H = 0;
    int len_L = 0;
    int len = 0;
    int count_2 = 0;
    int count = 0;
    while(count <= 0)
    {
        count = serial_->read(packet_bytes, 1);
        LslidarDriver::recvThread_crc(count,link_time);
    }
    if(packet_bytes[0] != 0xA5)	return 0;

    while(count_2 <= 0)
    {
        count_2 = serial_->read(packet_bytes+count, 1);
        if(count_2 >= 0) count += count_2;
        LslidarDriver::recvThread_crc(count_2,link_time);
    }

    count_2 = 0;
    if(packet_bytes[1] != 0x5A)	return 0;
    while(count_2 <= 0)
    {
        count_2 = serial_->read(packet_bytes+count, 2);
        if(count_2 >= 0) count += count_2;
        LslidarDriver::recvThread_crc(count_2,link_time);
    }
    
    count_2 = 0;

    if(lidar_name == "M10")                     len = 92;
    else if(lidar_name == "M10_TEST")           len = 176;
    else if(lidar_name == "M10_GPS")            len = 102;
    else if(lidar_name == "N10")                len = packet_bytes[2];
    else
    {
        len_H = packet_bytes[2];
        len_L = packet_bytes[3];
        len = len_H*256 + len_L;
    }

    while(count < len)
    {
        count_2 = serial_->read(packet_bytes+count, len-count);
        if(count_2 >= 0) count += count_2;
        LslidarDriver::recvThread_crc(count_2,link_time);
    }
    q = len;
    if(lidar_name == "N10") 
    {
        if(packet_bytes[PACKET_SIZE-1] != N10_CalCRC8(packet_bytes, PACKET_SIZE-1))						return 0;
    }
    return q;
}

uint8_t LslidarDriver::N10_CalCRC8(unsigned char * p, int len)
{
  uint8_t crc = 0;
  int sum = 0;

  for (int i = 0; i < len; i++)
  {
    sum += uint8_t(p[i]);
  }
  crc = sum & 0xff;
  return crc;
}

void LslidarDriver::data_processing(unsigned char *packet_bytes,int len)                                 //处理每一包的数据
{
    double degree;
    double end_degree;
    double degree_interval = 15.0;
    boost::posix_time::ptime t1,t2;
    t1 = boost::posix_time::microsec_clock::universal_time();

    int s = packet_bytes[degree_bits_start];
	int z = packet_bytes[degree_bits_start + 1];

	degree = (s * 256 + z) / 100.f;
	degree = (degree > 360) ? degree-360 : degree;
    if(lidar_name == "N10") 
    {
		int s_e = packet_bytes[end_degree_bits_start];
		int z_e = packet_bytes[end_degree_bits_start+1];
		end_degree = (s_e * 256 + z_e) / 100.f;    
        //printf("degree = %f end_degree = %f lidar_end_degree = %f\n",degree,end_degree,lidar_end_degree);
        end_degree = (end_degree > 360) ? end_degree-360 : end_degree;    

		if(degree > end_degree)
			degree_interval = end_degree + 360 - degree;
		else
			degree_interval = end_degree - degree;	
    }

    //boost::unique_lock<boost::mutex> lock(mutex_);
    if (lidar_name == "M10_PLUS"||lidar_name == "M10_P")
    {
        PACKET_SIZE = len;
        package_points = (PACKET_SIZE - 20)/2;
	}
    int invalidValue = 0;
    int point_len = 2;
    if(lidar_name == "N10")     point_len = 3;
    
    if(lidar_name == "M10_GPS"||lidar_name == "M10")
    {
		int err_data_84 = packet_bytes[84];
		int err_data_85 = packet_bytes[85];
        if((err_data_84 * 256 + err_data_85) == 0xFFFF || packet_bytes[86] >= 0xF5)
        {
            packet_bytes[86] = 0xFF;
            packet_bytes[87] = 0xFF;
        }
    }
    
	for (int num = 0; num < point_len*package_points; num+=point_len)
	{
		int s = packet_bytes[num + data_bits_start];
		int z = packet_bytes[num + data_bits_start + 1];
		if ((s * 256 + z) == 0xFFFF)
			invalidValue++;
	}
	if(use_gps_ts)
	{
		pTime.tm_year 	= packet_bytes[PACKET_SIZE - 12]+2000-1900;	//x+2000
		pTime.tm_mon 	= packet_bytes[PACKET_SIZE - 11]-1;			//1-12
		pTime.tm_mday 	= packet_bytes[PACKET_SIZE - 10];			//1-31
		pTime.tm_hour 	= packet_bytes[PACKET_SIZE - 9];			//0-23
		pTime.tm_min 	= packet_bytes[PACKET_SIZE - 8];			//0-59
		pTime.tm_sec 	= packet_bytes[PACKET_SIZE - 7];			//0-59
		sub_second		= (packet_bytes[PACKET_SIZE - 6]*256+packet_bytes[PACKET_SIZE - 5])*1000000 + (packet_bytes[PACKET_SIZE - 4]*256+packet_bytes[PACKET_SIZE - 3])*1000;		
		sweep_end_time_gps = get_gps_stamp(pTime);
		sweep_end_time_hardware = sub_second%1000000000;
	}
    invalidValue = package_points - invalidValue;
	for (int num = 0; num < package_points; num++)
	{
		int s = packet_bytes[num*point_len + data_bits_start];
		int z = packet_bytes[num*point_len + data_bits_start + 1];
        int y  = 0;
		if(lidar_name == "N10")     y = packet_bytes[num*point_len + data_bits_start+2];
		int dist_temp = s & 0x7F;
		int inten_temp = s & 0x80;

		if ((s * 256 + z) != 0xFFFF)
		{	
            if(lidar_name != "N10")
            {
                scan_points_[idx].range = double(dist_temp * 256 + (z)) / 1000.f;
                if (inten_temp)	scan_points_[idx].intensity = 255;
                else 	        scan_points_[idx].intensity = 0;
            }
            else
            {
				scan_points_[idx].range = double(s * 256 + (z)) / 1000.f;
				scan_points_[idx].intensity = int(y);
            }
            if ((degree + (degree_interval / invalidValue * num)) > 360)
                scan_points_[idx].degree = degree + (degree_interval / invalidValue * num) - 360;
            else
                scan_points_[idx].degree = degree + (degree_interval / invalidValue * num);
            
		}
        
        if ((scan_points_[idx].degree < last_degree && scan_points_[idx].degree < 2 && last_degree > 358)|| idx>=points_size_) 	
        {
            last_degree = scan_points_[idx].degree;
            count_num = idx;
            idx = 0;
            for(long unsigned int k=0;k<scan_points_.size();k++)
            {	
                if(scan_points_[k].range < min_range || scan_points_[k].range > max_range)
                    scan_points_[k].range = 0;
            }
            boost::unique_lock<boost::mutex> lock(mutex_);
            scan_points_bak_.resize(scan_points_.size());
            scan_points_bak_.assign(scan_points_.begin(), scan_points_.end());
            for(long unsigned int k=0; k<scan_points_.size(); k++)
            {
                scan_points_[k].range = 0;
                scan_points_[k].degree = 0;
            }
            pre_time_ = time_;
            lock.unlock();
            pubscan_cond_.notify_one();
            time_ = get_clock()->now();
        }
        else
        {
            last_degree = scan_points_[idx].degree;;
            idx++;
        }
        
	}
	//lock.unlock();
    packet_bytes = {0x00};
	
    if (packet_bytes)
    {
        packet_bytes = NULL;
        delete packet_bytes;
    }
}

void LslidarDriver::pubScanThread()
{
  bool wait_for_wake = true;
  boost::unique_lock<boost::mutex> lock(pubscan_mutex_);

  while (rclcpp::ok())
  {
    
    while (wait_for_wake)
    {
      pubscan_cond_.wait(lock);
      wait_for_wake = false;
    }
    auto scan = sensor_msgs::msg::LaserScan::UniquePtr(new sensor_msgs::msg::LaserScan());
	if(count_num <= 42 )
		continue;
	//int scan_num = ceil((angle_able_max-angle_able_min)/360*count_num)+1;           //原代码
	int scan_num = ceil((angle_able_max-angle_able_min)/360*count_num)-1;           //这样修改后，你那算法不会报错，但不合理，存在丢去1到2点可能。
        //printf("count_num = %d\n",count_num);
    std::vector<ScanPoint> points;
    rclcpp::Time start_time;
    float scan_time;
    this->getScan(points, start_time, scan_time);
    scan->header.frame_id = frame_id;
	if (use_gps_ts){
		scan->header.stamp = rclcpp::Time(sweep_end_time_gps, sweep_end_time_hardware);
	}
    else{
    	scan->header.stamp = this->now();  // timestamp will obtained from sweep data stamp
	}

	if(angle_able_max >360){
	scan->angle_min = 2 * M_PI * (angle_able_min-360) / 360;
    scan->angle_max = 2 * M_PI * (angle_able_max-360) / 360;
	}
	else{
    scan->angle_min = 2 * M_PI * angle_able_min / 360;
    scan->angle_max = 2 * M_PI * angle_able_max / 360;
	}
	scan->angle_increment = 2 * M_PI / (double)(count_num - 1);

    scan->range_min = min_range;
    scan->range_max = max_range;
    scan->ranges.reserve(scan_num);
    scan->ranges.assign(scan_num, std::numeric_limits<float>::infinity());
    scan->intensities.reserve(scan_num);
    scan->intensities.assign(scan_num, std::numeric_limits<float>::infinity());
    scan->scan_time = scan_time;
    scan->time_increment = scan_time / (double)(count_num - 1);
	
	int start_num = floor(angle_able_min * count_num / 360);
	int end_num = floor(angle_able_max * count_num / 360);

	for (int i = 0; i < count_num; i++) {
		int point_idx = round((360 - points[i].degree) * count_num / 360);
		if(point_idx<(end_num-count_num))
			point_idx += count_num;
		point_idx =  point_idx - start_num;
		if(point_idx < 0 || point_idx >= scan_num) 
			continue;
		if (points[i].range == 0.0) {
			scan->ranges[point_idx] = std::numeric_limits<float>::infinity();
		}
		else {
			double dist = points[i].range;
			scan->ranges[point_idx] = (float) dist;
		}
	    scan->intensities[point_idx] = points[i].intensity;

    if(truncated_mode_==1){
        int len=sizeof(angle_max) / sizeof(angle_max[0]);
		for (int j = 0; j < len; ++j) {
		if ((point_idx >= (angle_min[j] * count_num / 360) ) &&(point_idx <= (angle_max[j] * count_num / 360 ))) {
		    scan->ranges[point_idx] = std::numeric_limits<float>::infinity();
		    scan->intensities[point_idx] = 0;
		        }
		    }
    }
    }

	count_num = 0;
    scan_pub->publish(std::move(scan));
    wait_for_wake = true;
  }
}

bool LslidarDriver::polling()
{
    if(!is_start) return true;
    // Allocate a new shared pointer for zero-copy sharing with other nodelets.
     unsigned char * packet_bytes = new unsigned char[400];
     int len = 0;
    if(interface_selection == "net")
    {	 
        auto packet =  lslidar_msgs::msg::LslidarPacket::UniquePtr(
                   new lslidar_msgs::msg::LslidarPacket());
		
        std_msgs::msg::Byte msg;
        while (true)
        {
            len = 0;
            // keep reading until full packet received
            len = msop_input_->getPacket(packet);
            if(packet->data[0] == 0x5a && packet->data[1] == 0x00)  
            {
                int len_H = packet->data[1];
                int len_L = packet->data[2];
                len = len_H*256 + len_L;
                for (int i = len-1; i >0; i--)
                {
                    packet->data[i] = packet->data[i-1];
                }
                packet->data[0] = 0xa5;
            }
            
            if(dump_file !="")
            {
                if(lidar_name == "N10")             len = 58;
                else if(lidar_name == "M10")        len = 92;
                else if(lidar_name == "M10_GPS")    len = 102;
                else
                {
                    int len_H = packet->data[2];
                    int len_L = packet->data[3];
                    len = len_H*256 + len_L;
                }
            }
            if(len <= 0||len>500)    continue;
            if(packet->data[0] != 0xa5 && packet->data[1] != 0x5a)                  continue; 
            for (int i = 0; i < len; i++)
            {
                packet_bytes[i] = packet->data[i];
            }
            if(lidar_name == "N10" && packet_bytes[len-1] != N10_CalCRC8(packet_bytes, len-1))                      continue;   
            break;
        }
    }
    else{
        while (true)
        {
            len = 0;
            len = LslidarDriver::receive_data(packet_bytes);
            if(len == 0)    continue;
            break;
        }
        
	}
    LslidarDriver::data_processing(packet_bytes,len);
    return true;
}

} // namespace lslidar_driver
