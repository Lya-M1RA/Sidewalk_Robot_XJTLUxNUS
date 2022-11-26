// generated from rosidl_typesupport_fastrtps_c/resource/idl__type_support_c.cpp.em
// with input from share:msg/SendCAN0.idl
// generated code does not contain a copyright notice
#include "share/msg/detail/send_can0__rosidl_typesupport_fastrtps_c.h"


#include <cassert>
#include <limits>
#include <string>
#include "rosidl_typesupport_fastrtps_c/identifier.h"
#include "rosidl_typesupport_fastrtps_c/wstring_conversion.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "share/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "share/msg/detail/send_can0__struct.h"
#include "share/msg/detail/send_can0__functions.h"
#include "fastcdr/Cdr.h"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

// includes and forward declarations of message dependencies and their conversion functions

#if defined(__cplusplus)
extern "C"
{
#endif


// forward declare type support functions


using _SendCAN0__ros_msg_type = share__msg__SendCAN0;

static bool _SendCAN0__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  const _SendCAN0__ros_msg_type * ros_message = static_cast<const _SendCAN0__ros_msg_type *>(untyped_ros_message);
  // Field name: left_motor_data
  {
    size_t size = 8;
    auto array_ptr = ros_message->left_motor_data;
    cdr.serializeArray(array_ptr, size);
  }

  // Field name: right_motor_data
  {
    size_t size = 8;
    auto array_ptr = ros_message->right_motor_data;
    cdr.serializeArray(array_ptr, size);
  }

  return true;
}

static bool _SendCAN0__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  _SendCAN0__ros_msg_type * ros_message = static_cast<_SendCAN0__ros_msg_type *>(untyped_ros_message);
  // Field name: left_motor_data
  {
    size_t size = 8;
    auto array_ptr = ros_message->left_motor_data;
    cdr.deserializeArray(array_ptr, size);
  }

  // Field name: right_motor_data
  {
    size_t size = 8;
    auto array_ptr = ros_message->right_motor_data;
    cdr.deserializeArray(array_ptr, size);
  }

  return true;
}  // NOLINT(readability/fn_size)

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_share
size_t get_serialized_size_share__msg__SendCAN0(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _SendCAN0__ros_msg_type * ros_message = static_cast<const _SendCAN0__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // field.name left_motor_data
  {
    size_t array_size = 8;
    auto array_ptr = ros_message->left_motor_data;
    (void)array_ptr;
    size_t item_size = sizeof(array_ptr[0]);
    current_alignment += array_size * item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name right_motor_data
  {
    size_t array_size = 8;
    auto array_ptr = ros_message->right_motor_data;
    (void)array_ptr;
    size_t item_size = sizeof(array_ptr[0]);
    current_alignment += array_size * item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  return current_alignment - initial_alignment;
}

static uint32_t _SendCAN0__get_serialized_size(const void * untyped_ros_message)
{
  return static_cast<uint32_t>(
    get_serialized_size_share__msg__SendCAN0(
      untyped_ros_message, 0));
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_share
size_t max_serialized_size_share__msg__SendCAN0(
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

  // member: left_motor_data
  {
    size_t array_size = 8;

    current_alignment += array_size * sizeof(uint8_t);
  }
  // member: right_motor_data
  {
    size_t array_size = 8;

    current_alignment += array_size * sizeof(uint8_t);
  }

  return current_alignment - initial_alignment;
}

static size_t _SendCAN0__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_share__msg__SendCAN0(
    full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}


static message_type_support_callbacks_t __callbacks_SendCAN0 = {
  "share::msg",
  "SendCAN0",
  _SendCAN0__cdr_serialize,
  _SendCAN0__cdr_deserialize,
  _SendCAN0__get_serialized_size,
  _SendCAN0__max_serialized_size
};

static rosidl_message_type_support_t _SendCAN0__type_support = {
  rosidl_typesupport_fastrtps_c__identifier,
  &__callbacks_SendCAN0,
  get_message_typesupport_handle_function,
};

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, share, msg, SendCAN0)() {
  return &_SendCAN0__type_support;
}

#if defined(__cplusplus)
}
#endif
