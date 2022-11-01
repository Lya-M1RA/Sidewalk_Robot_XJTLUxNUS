// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from share:msg/SendCAN0.idl
// generated code does not contain a copyright notice

#ifndef SHARE__MSG__DETAIL__SEND_CAN0__FUNCTIONS_H_
#define SHARE__MSG__DETAIL__SEND_CAN0__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/visibility_control.h"
#include "share/msg/rosidl_generator_c__visibility_control.h"

#include "share/msg/detail/send_can0__struct.h"

/// Initialize msg/SendCAN0 message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * share__msg__SendCAN0
 * )) before or use
 * share__msg__SendCAN0__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_share
bool
share__msg__SendCAN0__init(share__msg__SendCAN0 * msg);

/// Finalize msg/SendCAN0 message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_share
void
share__msg__SendCAN0__fini(share__msg__SendCAN0 * msg);

/// Create msg/SendCAN0 message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * share__msg__SendCAN0__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_share
share__msg__SendCAN0 *
share__msg__SendCAN0__create();

/// Destroy msg/SendCAN0 message.
/**
 * It calls
 * share__msg__SendCAN0__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_share
void
share__msg__SendCAN0__destroy(share__msg__SendCAN0 * msg);

/// Check for msg/SendCAN0 message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_share
bool
share__msg__SendCAN0__are_equal(const share__msg__SendCAN0 * lhs, const share__msg__SendCAN0 * rhs);

/// Copy a msg/SendCAN0 message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_share
bool
share__msg__SendCAN0__copy(
  const share__msg__SendCAN0 * input,
  share__msg__SendCAN0 * output);

/// Initialize array of msg/SendCAN0 messages.
/**
 * It allocates the memory for the number of elements and calls
 * share__msg__SendCAN0__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_share
bool
share__msg__SendCAN0__Sequence__init(share__msg__SendCAN0__Sequence * array, size_t size);

/// Finalize array of msg/SendCAN0 messages.
/**
 * It calls
 * share__msg__SendCAN0__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_share
void
share__msg__SendCAN0__Sequence__fini(share__msg__SendCAN0__Sequence * array);

/// Create array of msg/SendCAN0 messages.
/**
 * It allocates the memory for the array and calls
 * share__msg__SendCAN0__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_share
share__msg__SendCAN0__Sequence *
share__msg__SendCAN0__Sequence__create(size_t size);

/// Destroy array of msg/SendCAN0 messages.
/**
 * It calls
 * share__msg__SendCAN0__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_share
void
share__msg__SendCAN0__Sequence__destroy(share__msg__SendCAN0__Sequence * array);

/// Check for msg/SendCAN0 message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_share
bool
share__msg__SendCAN0__Sequence__are_equal(const share__msg__SendCAN0__Sequence * lhs, const share__msg__SendCAN0__Sequence * rhs);

/// Copy an array of msg/SendCAN0 messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_share
bool
share__msg__SendCAN0__Sequence__copy(
  const share__msg__SendCAN0__Sequence * input,
  share__msg__SendCAN0__Sequence * output);

#ifdef __cplusplus
}
#endif

#endif  // SHARE__MSG__DETAIL__SEND_CAN0__FUNCTIONS_H_
