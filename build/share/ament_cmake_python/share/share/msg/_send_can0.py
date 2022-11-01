# generated from rosidl_generator_py/resource/_idl.py.em
# with input from share:msg/SendCAN0.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

# Member 'left_motor_data'
# Member 'right_motor_data'
import numpy  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_SendCAN0(type):
    """Metaclass of message 'SendCAN0'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('share')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'share.msg.SendCAN0')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__send_can0
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__send_can0
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__send_can0
            cls._TYPE_SUPPORT = module.type_support_msg__msg__send_can0
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__send_can0

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class SendCAN0(metaclass=Metaclass_SendCAN0):
    """Message class 'SendCAN0'."""

    __slots__ = [
        '_left_motor_data',
        '_right_motor_data',
    ]

    _fields_and_field_types = {
        'left_motor_data': 'uint8[8]',
        'right_motor_data': 'uint8[8]',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.Array(rosidl_parser.definition.BasicType('uint8'), 8),  # noqa: E501
        rosidl_parser.definition.Array(rosidl_parser.definition.BasicType('uint8'), 8),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        if 'left_motor_data' not in kwargs:
            self.left_motor_data = numpy.zeros(8, dtype=numpy.uint8)
        else:
            self.left_motor_data = numpy.array(kwargs.get('left_motor_data'), dtype=numpy.uint8)
            assert self.left_motor_data.shape == (8, )
        if 'right_motor_data' not in kwargs:
            self.right_motor_data = numpy.zeros(8, dtype=numpy.uint8)
        else:
            self.right_motor_data = numpy.array(kwargs.get('right_motor_data'), dtype=numpy.uint8)
            assert self.right_motor_data.shape == (8, )

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.__slots__, self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s[1:] + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if all(self.left_motor_data != other.left_motor_data):
            return False
        if all(self.right_motor_data != other.right_motor_data):
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def left_motor_data(self):
        """Message field 'left_motor_data'."""
        return self._left_motor_data

    @left_motor_data.setter
    def left_motor_data(self, value):
        if isinstance(value, numpy.ndarray):
            assert value.dtype == numpy.uint8, \
                "The 'left_motor_data' numpy.ndarray() must have the dtype of 'numpy.uint8'"
            assert value.size == 8, \
                "The 'left_motor_data' numpy.ndarray() must have a size of 8"
            self._left_motor_data = value
            return
        if __debug__:
            from collections.abc import Sequence
            from collections.abc import Set
            from collections import UserList
            from collections import UserString
            assert \
                ((isinstance(value, Sequence) or
                  isinstance(value, Set) or
                  isinstance(value, UserList)) and
                 not isinstance(value, str) and
                 not isinstance(value, UserString) and
                 len(value) == 8 and
                 all(isinstance(v, int) for v in value) and
                 all(val >= 0 and val < 256 for val in value)), \
                "The 'left_motor_data' field must be a set or sequence with length 8 and each value of type 'int' and each unsigned integer in [0, 255]"
        self._left_motor_data = numpy.array(value, dtype=numpy.uint8)

    @builtins.property
    def right_motor_data(self):
        """Message field 'right_motor_data'."""
        return self._right_motor_data

    @right_motor_data.setter
    def right_motor_data(self, value):
        if isinstance(value, numpy.ndarray):
            assert value.dtype == numpy.uint8, \
                "The 'right_motor_data' numpy.ndarray() must have the dtype of 'numpy.uint8'"
            assert value.size == 8, \
                "The 'right_motor_data' numpy.ndarray() must have a size of 8"
            self._right_motor_data = value
            return
        if __debug__:
            from collections.abc import Sequence
            from collections.abc import Set
            from collections import UserList
            from collections import UserString
            assert \
                ((isinstance(value, Sequence) or
                  isinstance(value, Set) or
                  isinstance(value, UserList)) and
                 not isinstance(value, str) and
                 not isinstance(value, UserString) and
                 len(value) == 8 and
                 all(isinstance(v, int) for v in value) and
                 all(val >= 0 and val < 256 for val in value)), \
                "The 'right_motor_data' field must be a set or sequence with length 8 and each value of type 'int' and each unsigned integer in [0, 255]"
        self._right_motor_data = numpy.array(value, dtype=numpy.uint8)
