#!/usr/bin/env python3
import struct
import subprocess
import re

"""
NOTE: Read from /dev/input/event3
    struct input_event {
      struct timeval time;
      unsigned short type;
      unsigned short code;
      unsigned int value;
    }
values for timeval, type, code and value are located in /usr/include/linux/input-event-codes.h
"""
#TODO: Change value when there is shift combinatins, i.e 1 to !,
#      also figure out how to do this over multiple keyboard layouts
#TODO: Ensure works with different keyboard layouts, not just qwerty
