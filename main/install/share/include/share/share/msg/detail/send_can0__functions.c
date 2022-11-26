// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from share:msg/SendCAN0.idl
// generated code does not contain a copyright notice
#include "share/msg/detail/send_can0__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


bool
share__msg__SendCAN0__init(share__msg__SendCAN0 * msg)
{
  if (!msg) {
    return false;
  }
  // left_motor_data
  // right_motor_data
  return true;
}

void
share__msg__SendCAN0__fini(share__msg__SendCAN0 * msg)
{
  if (!msg) {
    return;
  }
  // left_motor_data
  // right_motor_data
}

bool
share__msg__SendCAN0__are_equal(const share__msg__SendCAN0 * lhs, const share__msg__SendCAN0 * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // left_motor_data
  for (size_t i = 0; i < 8; ++i) {
    if (lhs->left_motor_data[i] != rhs->left_motor_data[i]) {
      return false;
    }
  }
  // right_motor_data
  for (size_t i = 0; i < 8; ++i) {
    if (lhs->right_motor_data[i] != rhs->right_motor_data[i]) {
      return false;
    }
  }
  return true;
}

bool
share__msg__SendCAN0__copy(
  const share__msg__SendCAN0 * input,
  share__msg__SendCAN0 * output)
{
  if (!input || !output) {
    return false;
  }
  // left_motor_data
  for (size_t i = 0; i < 8; ++i) {
    output->left_motor_data[i] = input->left_motor_data[i];
  }
  // right_motor_data
  for (size_t i = 0; i < 8; ++i) {
    output->right_motor_data[i] = input->right_motor_data[i];
  }
  return true;
}

share__msg__SendCAN0 *
share__msg__SendCAN0__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  share__msg__SendCAN0 * msg = (share__msg__SendCAN0 *)allocator.allocate(sizeof(share__msg__SendCAN0), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(share__msg__SendCAN0));
  bool success = share__msg__SendCAN0__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
share__msg__SendCAN0__destroy(share__msg__SendCAN0 * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    share__msg__SendCAN0__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
share__msg__SendCAN0__Sequence__init(share__msg__SendCAN0__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  share__msg__SendCAN0 * data = NULL;

  if (size) {
    data = (share__msg__SendCAN0 *)allocator.zero_allocate(size, sizeof(share__msg__SendCAN0), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = share__msg__SendCAN0__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        share__msg__SendCAN0__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
share__msg__SendCAN0__Sequence__fini(share__msg__SendCAN0__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      share__msg__SendCAN0__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

share__msg__SendCAN0__Sequence *
share__msg__SendCAN0__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  share__msg__SendCAN0__Sequence * array = (share__msg__SendCAN0__Sequence *)allocator.allocate(sizeof(share__msg__SendCAN0__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = share__msg__SendCAN0__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
share__msg__SendCAN0__Sequence__destroy(share__msg__SendCAN0__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    share__msg__SendCAN0__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
share__msg__SendCAN0__Sequence__are_equal(const share__msg__SendCAN0__Sequence * lhs, const share__msg__SendCAN0__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!share__msg__SendCAN0__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
share__msg__SendCAN0__Sequence__copy(
  const share__msg__SendCAN0__Sequence * input,
  share__msg__SendCAN0__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(share__msg__SendCAN0);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    share__msg__SendCAN0 * data =
      (share__msg__SendCAN0 *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!share__msg__SendCAN0__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          share__msg__SendCAN0__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!share__msg__SendCAN0__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
