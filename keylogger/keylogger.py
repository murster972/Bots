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

class Keylogger:
    def __init__(self):
        pass

    def parse_input_event_codes(self):
        pass

    def key_code_to_ascii(self):
        pass

    def get_capsnum_lock(self):
        pass

    def get_keyboard_layout(self):
        pass

    def get_focused_window(self):
        pass
