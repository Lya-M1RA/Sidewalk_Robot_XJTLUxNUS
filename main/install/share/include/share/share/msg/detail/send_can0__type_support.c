// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from share:msg/SendCAN0.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "share/msg/detail/send_can0__rosidl_typesupport_introspection_c.h"
#include "share/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "share/msg/detail/send_can0__functions.h"
#include "share/msg/detail/send_can0__struct.h"


#ifdef __cplusplus
extern "C"
{
#endif

void share__msg__SendCAN0__rosidl_typesupport_introspection_c__SendCAN0_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  share__msg__SendCAN0__init(message_memory);
}

void share__msg__SendCAN0__rosidl_typesupport_introspection_c__SendCAN0_fini_function(void * message_memory)
{
  share__msg__SendCAN0__fini(message_memory);
}

size_t share__msg__SendCAN0__rosidl_typesupport_introspection_c__size_function__SendCAN0__left_motor_data(
  const void * untyped_member)
{
  (void)untyped_member;
  return 8;
}

const void * share__msg__SendCAN0__rosidl_typesupport_introspection_c__get_const_function__SendCAN0__left_motor_data(
  const void * untyped_member, size_t index)
{
  const uint8_t * member =
    (const uint8_t *)(untyped_member);
  return &member[index];
}

void * share__msg__SendCAN0__rosidl_typesupport_introspection_c__get_function__SendCAN0__left_motor_data(
  void * untyped_member, size_t index)
{
  uint8_t * member =
    (uint8_t *)(untyped_member);
  return &member[index];
}

void share__msg__SendCAN0__rosidl_typesupport_introspection_c__fetch_function__SendCAN0__left_motor_data(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const uint8_t * item =
    ((const uint8_t *)
    share__msg__SendCAN0__rosidl_typesupport_introspection_c__get_const_function__SendCAN0__left_motor_data(untyped_member, index));
  uint8_t * value =
    (uint8_t *)(untyped_value);
  *value = *item;
}

void share__msg__SendCAN0__rosidl_typesupport_introspection_c__assign_function__SendCAN0__left_motor_data(
  void * untyped_member, size_t index, const void * untyped_value)
{
  uint8_t * item =
    ((uint8_t *)
    share__msg__SendCAN0__rosidl_typesupport_introspection_c__get_function__SendCAN0__left_motor_data(untyped_member, index));
  const uint8_t * value =
    (const uint8_t *)(untyped_value);
  *item = *value;
}

size_t share__msg__SendCAN0__rosidl_typesupport_introspection_c__size_function__SendCAN0__right_motor_data(
  const void * untyped_member)
{
  (void)untyped_member;
  return 8;
}

const void * share__msg__SendCAN0__rosidl_typesupport_introspection_c__get_const_function__SendCAN0__right_motor_data(
  const void * untyped_member, size_t index)
{
  const uint8_t * member =
    (const uint8_t *)(untyped_member);
  return &member[index];
}

void * share__msg__SendCAN0__rosidl_typesupport_introspection_c__get_function__SendCAN0__right_motor_data(
  void * untyped_member, size_t index)
{
  uint8_t * member =
    (uint8_t *)(untyped_member);
  return &member[index];
}

void share__msg__SendCAN0__rosidl_typesupport_introspection_c__fetch_function__SendCAN0__right_motor_data(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const uint8_t * item =
    ((const uint8_t *)
    share__msg__SendCAN0__rosidl_typesupport_introspection_c__get_const_function__SendCAN0__right_motor_data(untyped_member, index));
  uint8_t * value =
    (uint8_t *)(untyped_value);
  *value = *item;
}

void share__msg__SendCAN0__rosidl_typesupport_introspection_c__assign_function__SendCAN0__right_motor_data(
  void * untyped_member, size_t index, const void * untyped_value)
{
  uint8_t * item =
    ((uint8_t *)
    share__msg__SendCAN0__rosidl_typesupport_introspection_c__get_function__SendCAN0__right_motor_data(untyped_member, index));
  const uint8_t * value =
    (const uint8_t *)(untyped_value);
  *item = *value;
}

static rosidl_typesupport_introspection_c__MessageMember share__msg__SendCAN0__rosidl_typesupport_introspection_c__SendCAN0_message_member_array[2] = {
  {
    "left_motor_data",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT8,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    8,  // array size
    false,  // is upper bound
    offsetof(share__msg__SendCAN0, left_motor_data),  // bytes offset in struct
    NULL,  // default value
    share__msg__SendCAN0__rosidl_typesupport_introspection_c__size_function__SendCAN0__left_motor_data,  // size() function pointer
    share__msg__SendCAN0__rosidl_typesupport_introspection_c__get_const_function__SendCAN0__left_motor_data,  // get_const(index) function pointer
    share__msg__SendCAN0__rosidl_typesupport_introspection_c__get_function__SendCAN0__left_motor_data,  // get(index) function pointer
    share__msg__SendCAN0__rosidl_typesupport_introspection_c__fetch_function__SendCAN0__left_motor_data,  // fetch(index, &value) function pointer
    share__msg__SendCAN0__rosidl_typesupport_introspection_c__assign_function__SendCAN0__left_motor_data,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "right_motor_data",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT8,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    8,  // array size
    false,  // is upper bound
    offsetof(share__msg__SendCAN0, right_motor_data),  // bytes offset in struct
    NULL,  // default value
    share__msg__SendCAN0__rosidl_typesupport_introspection_c__size_function__SendCAN0__right_motor_data,  // size() function pointer
    share__msg__SendCAN0__rosidl_typesupport_introspection_c__get_const_function__SendCAN0__right_motor_data,  // get_const(index) function pointer
    share__msg__SendCAN0__rosidl_typesupport_introspection_c__get_function__SendCAN0__right_motor_data,  // get(index) function pointer
    share__msg__SendCAN0__rosidl_typesupport_introspection_c__fetch_function__SendCAN0__right_motor_data,  // fetch(index, &value) function pointer
    share__msg__SendCAN0__rosidl_typesupport_introspection_c__assign_function__SendCAN0__right_motor_data,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers share__msg__SendCAN0__rosidl_typesupport_introspection_c__SendCAN0_message_members = {
  "share__msg",  // message namespace
  "SendCAN0",  // message name
  2,  // number of fields
  sizeof(share__msg__SendCAN0),
  share__msg__SendCAN0__rosidl_typesupport_introspection_c__SendCAN0_message_member_array,  // message members
  share__msg__SendCAN0__rosidl_typesupport_introspection_c__SendCAN0_init_function,  // function to initialize message memory (memory has to be allocated)
  share__msg__SendCAN0__rosidl_typesupport_introspection_c__SendCAN0_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t share__msg__SendCAN0__rosidl_typesupport_introspection_c__SendCAN0_message_type_support_handle = {
  0,
  &share__msg__SendCAN0__rosidl_typesupport_introspection_c__SendCAN0_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_share
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, share, msg, SendCAN0)() {
  if (!share__msg__SendCAN0__rosidl_typesupport_introspection_c__SendCAN0_message_type_support_handle.typesupport_identifier) {
    share__msg__SendCAN0__rosidl_typesupport_introspection_c__SendCAN0_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &share__msg__SendCAN0__rosidl_typesupport_introspection_c__SendCAN0_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
