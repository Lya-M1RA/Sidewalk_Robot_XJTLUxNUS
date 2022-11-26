// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from share:msg/SendCAN0.idl
// generated code does not contain a copyright notice

#ifndef SHARE__MSG__DETAIL__SEND_CAN0__TRAITS_HPP_
#define SHARE__MSG__DETAIL__SEND_CAN0__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "share/msg/detail/send_can0__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace share
{

namespace msg
{

inline void to_flow_style_yaml(
  const SendCAN0 & msg,
  std::ostream & out)
{
  out << "{";
  // member: left_motor_data
  {
    if (msg.left_motor_data.size() == 0) {
      out << "left_motor_data: []";
    } else {
      out << "left_motor_data: [";
      size_t pending_items = msg.left_motor_data.size();
      for (auto item : msg.left_motor_data) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: right_motor_data
  {
    if (msg.right_motor_data.size() == 0) {
      out << "right_motor_data: []";
    } else {
      out << "right_motor_data: [";
      size_t pending_items = msg.right_motor_data.size();
      for (auto item : msg.right_motor_data) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const SendCAN0 & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: left_motor_data
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.left_motor_data.size() == 0) {
      out << "left_motor_data: []\n";
    } else {
      out << "left_motor_data:\n";
      for (auto item : msg.left_motor_data) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: right_motor_data
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.right_motor_data.size() == 0) {
      out << "right_motor_data: []\n";
    } else {
      out << "right_motor_data:\n";
      for (auto item : msg.right_motor_data) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const SendCAN0 & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace share

namespace rosidl_generator_traits
{

[[deprecated("use share::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const share::msg::SendCAN0 & msg,
  std::ostream & out, size_t indentation = 0)
{
  share::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use share::msg::to_yaml() instead")]]
inline std::string to_yaml(const share::msg::SendCAN0 & msg)
{
  return share::msg::to_yaml(msg);
}

template<>
inline const char * data_type<share::msg::SendCAN0>()
{
  return "share::msg::SendCAN0";
}

template<>
inline const char * name<share::msg::SendCAN0>()
{
  return "share/msg/SendCAN0";
}

template<>
struct has_fixed_size<share::msg::SendCAN0>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<share::msg::SendCAN0>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<share::msg::SendCAN0>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // SHARE__MSG__DETAIL__SEND_CAN0__TRAITS_HPP_
