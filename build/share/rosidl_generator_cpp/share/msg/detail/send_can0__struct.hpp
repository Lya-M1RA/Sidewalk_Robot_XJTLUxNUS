// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from share:msg/SendCAN0.idl
// generated code does not contain a copyright notice

#ifndef SHARE__MSG__DETAIL__SEND_CAN0__STRUCT_HPP_
#define SHARE__MSG__DETAIL__SEND_CAN0__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__share__msg__SendCAN0 __attribute__((deprecated))
#else
# define DEPRECATED__share__msg__SendCAN0 __declspec(deprecated)
#endif

namespace share
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct SendCAN0_
{
  using Type = SendCAN0_<ContainerAllocator>;

  explicit SendCAN0_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      std::fill<typename std::array<uint8_t, 8>::iterator, uint8_t>(this->left_motor_data.begin(), this->left_motor_data.end(), 0);
      std::fill<typename std::array<uint8_t, 8>::iterator, uint8_t>(this->right_motor_data.begin(), this->right_motor_data.end(), 0);
    }
  }

  explicit SendCAN0_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : left_motor_data(_alloc),
    right_motor_data(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      std::fill<typename std::array<uint8_t, 8>::iterator, uint8_t>(this->left_motor_data.begin(), this->left_motor_data.end(), 0);
      std::fill<typename std::array<uint8_t, 8>::iterator, uint8_t>(this->right_motor_data.begin(), this->right_motor_data.end(), 0);
    }
  }

  // field types and members
  using _left_motor_data_type =
    std::array<uint8_t, 8>;
  _left_motor_data_type left_motor_data;
  using _right_motor_data_type =
    std::array<uint8_t, 8>;
  _right_motor_data_type right_motor_data;

  // setters for named parameter idiom
  Type & set__left_motor_data(
    const std::array<uint8_t, 8> & _arg)
  {
    this->left_motor_data = _arg;
    return *this;
  }
  Type & set__right_motor_data(
    const std::array<uint8_t, 8> & _arg)
  {
    this->right_motor_data = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    share::msg::SendCAN0_<ContainerAllocator> *;
  using ConstRawPtr =
    const share::msg::SendCAN0_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<share::msg::SendCAN0_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<share::msg::SendCAN0_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      share::msg::SendCAN0_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<share::msg::SendCAN0_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      share::msg::SendCAN0_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<share::msg::SendCAN0_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<share::msg::SendCAN0_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<share::msg::SendCAN0_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__share__msg__SendCAN0
    std::shared_ptr<share::msg::SendCAN0_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__share__msg__SendCAN0
    std::shared_ptr<share::msg::SendCAN0_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const SendCAN0_ & other) const
  {
    if (this->left_motor_data != other.left_motor_data) {
      return false;
    }
    if (this->right_motor_data != other.right_motor_data) {
      return false;
    }
    return true;
  }
  bool operator!=(const SendCAN0_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct SendCAN0_

// alias to use template instance with default allocator
using SendCAN0 =
  share::msg::SendCAN0_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace share

#endif  // SHARE__MSG__DETAIL__SEND_CAN0__STRUCT_HPP_
