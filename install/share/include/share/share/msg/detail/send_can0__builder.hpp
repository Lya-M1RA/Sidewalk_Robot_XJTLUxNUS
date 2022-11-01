// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from share:msg/SendCAN0.idl
// generated code does not contain a copyright notice

#ifndef SHARE__MSG__DETAIL__SEND_CAN0__BUILDER_HPP_
#define SHARE__MSG__DETAIL__SEND_CAN0__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "share/msg/detail/send_can0__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace share
{

namespace msg
{

namespace builder
{

class Init_SendCAN0_right_motor_data
{
public:
  explicit Init_SendCAN0_right_motor_data(::share::msg::SendCAN0 & msg)
  : msg_(msg)
  {}
  ::share::msg::SendCAN0 right_motor_data(::share::msg::SendCAN0::_right_motor_data_type arg)
  {
    msg_.right_motor_data = std::move(arg);
    return std::move(msg_);
  }

private:
  ::share::msg::SendCAN0 msg_;
};

class Init_SendCAN0_left_motor_data
{
public:
  Init_SendCAN0_left_motor_data()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_SendCAN0_right_motor_data left_motor_data(::share::msg::SendCAN0::_left_motor_data_type arg)
  {
    msg_.left_motor_data = std::move(arg);
    return Init_SendCAN0_right_motor_data(msg_);
  }

private:
  ::share::msg::SendCAN0 msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::share::msg::SendCAN0>()
{
  return share::msg::builder::Init_SendCAN0_left_motor_data();
}

}  // namespace share

#endif  // SHARE__MSG__DETAIL__SEND_CAN0__BUILDER_HPP_
