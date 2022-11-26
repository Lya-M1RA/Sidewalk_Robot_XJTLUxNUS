// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from share:msg/SendCAN0.idl
// generated code does not contain a copyright notice

#ifndef SHARE__MSG__DETAIL__SEND_CAN0__STRUCT_H_
#define SHARE__MSG__DETAIL__SEND_CAN0__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in msg/SendCAN0 in the package share.
/**
  * std_msgs/Header header
 */
typedef struct share__msg__SendCAN0
{
  /// CAN frame data to be sent to left motor
  uint8_t left_motor_data[8];
  /// CAN frame data to be sent to right motor
  uint8_t right_motor_data[8];
} share__msg__SendCAN0;

// Struct for a sequence of share__msg__SendCAN0.
typedef struct share__msg__SendCAN0__Sequence
{
  share__msg__SendCAN0 * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} share__msg__SendCAN0__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // SHARE__MSG__DETAIL__SEND_CAN0__STRUCT_H_
