// generated from rosidl_typesupport_c/resource/idl__type_support.cpp.em
// with input from share:msg/SendCAN0.idl
// generated code does not contain a copyright notice

#include "cstddef"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "share/msg/detail/send_can0__struct.h"
#include "share/msg/detail/send_can0__type_support.h"
#include "rosidl_typesupport_c/identifier.h"
#include "rosidl_typesupport_c/message_type_support_dispatch.h"
#include "rosidl_typesupport_c/type_support_map.h"
#include "rosidl_typesupport_c/visibility_control.h"
#include "rosidl_typesupport_interface/macros.h"

namespace share
{

namespace msg
{

namespace rosidl_typesupport_c
{

typedef struct _SendCAN0_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _SendCAN0_type_support_ids_t;

static const _SendCAN0_type_support_ids_t _SendCAN0_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _SendCAN0_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _SendCAN0_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _SendCAN0_type_support_symbol_names_t _SendCAN0_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, share, msg, SendCAN0)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, share, msg, SendCAN0)),
  }
};

typedef struct _SendCAN0_type_support_data_t
{
  void * data[2];
} _SendCAN0_type_support_data_t;

static _SendCAN0_type_support_data_t _SendCAN0_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _SendCAN0_message_typesupport_map = {
  2,
  "share",
  &_SendCAN0_message_typesupport_ids.typesupport_identifier[0],
  &_SendCAN0_message_typesupport_symbol_names.symbol_name[0],
  &_SendCAN0_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t SendCAN0_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_SendCAN0_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_c

}  // namespace msg

}  // namespace share

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, share, msg, SendCAN0)() {
  return &::share::msg::rosidl_typesupport_c::SendCAN0_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif
