// generated from rosidl_typesupport_fastrtps_cpp/resource/idl__type_support.cpp.em
// with input from share:msg/SendCAN0.idl
// generated code does not contain a copyright notice
#include "share/msg/detail/send_can0__rosidl_typesupport_fastrtps_cpp.hpp"
#include "share/msg/detail/send_can0__struct.hpp"

#include <limits>
#include <stdexcept>
#include <string>
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_fastrtps_cpp/identifier.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_fastrtps_cpp/wstring_conversion.hpp"
#include "fastcdr/Cdr.h"


// forward declaration of message dependencies and their conversion functions

namespace share
{

namespace msg
{

namespace typesupport_fastrtps_cpp
{

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_share
cdr_serialize(
  const share::msg::SendCAN0 & ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  // Member: left_motor_data
  {
    cdr << ros_message.left_motor_data;
  }
  // Member: right_motor_data
  {
    cdr << ros_message.right_motor_data;
  }
  return true;
}

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_share
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  share::msg::SendCAN0 & ros_message)
{
  // Member: left_motor_data
  {
    cdr >> ros_message.left_motor_data;
  }

  // Member: right_motor_data
  {
    cdr >> ros_message.right_motor_data;
  }

  return true;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_share
get_serialized_size(
  const share::msg::SendCAN0 & ros_message,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Member: left_motor_data
  {
    size_t array_size = 8;
    size_t item_size = sizeof(ros_message.left_motor_data[0]);
    current_alignment += array_size * item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: right_motor_data
  {
    size_t array_size = 8;
    size_t item_size = sizeof(ros_message.right_motor_data[0]);
    current_alignment += array_size * item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  return current_alignment - initial_alignment;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_share
max_serialized_size_SendCAN0(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  full_bounded = true;
  is_plain = true;


  // Member: left_motor_data
  {
    size_t array_size = 8;

    current_alignment += array_size * sizeof(uint8_t);
  }

  // Member: right_motor_data
  {
    size_t array_size = 8;

    current_alignment += array_size * sizeof(uint8_t);
  }

  return current_alignment - initial_alignment;
}

static bool _SendCAN0__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  auto typed_message =
    static_cast<const share::msg::SendCAN0 *>(
    untyped_ros_message);
  return cdr_serialize(*typed_message, cdr);
}

static bool _SendCAN0__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  auto typed_message =
    static_cast<share::msg::SendCAN0 *>(
    untyped_ros_message);
  return cdr_deserialize(cdr, *typed_message);
}

static uint32_t _SendCAN0__get_serialized_size(
  const void * untyped_ros_message)
{
  auto typed_message =
    static_cast<const share::msg::SendCAN0 *>(
    untyped_ros_message);
  return static_cast<uint32_t>(get_serialized_size(*typed_message, 0));
}

static size_t _SendCAN0__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_SendCAN0(full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}

static message_type_support_callbacks_t _SendCAN0__callbacks = {
  "share::msg",
  "SendCAN0",
  _SendCAN0__cdr_serialize,
  _SendCAN0__cdr_deserialize,
  _SendCAN0__get_serialized_size,
  _SendCAN0__max_serialized_size
};

static rosidl_message_type_support_t _SendCAN0__handle = {
  rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
  &_SendCAN0__callbacks,
  get_message_typesupport_handle_function,
};

}  // namespace typesupport_fastrtps_cpp

}  // namespace msg

}  // namespace share

namespace rosidl_typesupport_fastrtps_cpp
{

template<>
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_EXPORT_share
const rosidl_message_type_support_t *
get_message_type_support_handle<share::msg::SendCAN0>()
{
  return &share::msg::typesupport_fastrtps_cpp::_SendCAN0__handle;
}

}  // namespace rosidl_typesupport_fastrtps_cpp

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, share, msg, SendCAN0)() {
  return &share::msg::typesupport_fastrtps_cpp::_SendCAN0__handle;
}

#ifdef __cplusplus
}
#endif
