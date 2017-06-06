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

'Goes through /usr/include/linux/input-event-codes.h getting key codes'
def parse_input_event_codes():
    f = open("/usr/include/linux/input-event-codes.h", "r")
    data = f.readlines()
    f.close()

    key_const = {}

    for i in data:
        c = [x for x in i.replace("\t", " ").replace("\n", "").split(" ") if x]
        if len(c) < 3 or (c[1][:3] != "KEY" and c[1][:3] != "BTN"): continue
        val = c[2] if "0x" not in c[2] else str(int(c[2], 16))
        if "+" in val:
            v = val[1:-1].split("+")
            val = int(key_const[v[0]]) + int(v[1])
        elif val in key_const:
            val = key_const[val]
        key_const[c[1]] = val
    return {key_const[x]:x for x in key_const}

def get_capsnum_lock():
    ps_res = subprocess.run(["xset", "-q"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    res_out = ps_res.stdout.decode()
    res = re.sub("[0123456789 ]", "", res_out).split("\n")[3].split(":")
    return [res[2], res[4]]

def main():
    f = open("/dev/input/event3", "rb")
    form = "llHHI"
    e_size = struct.calcsize(form)
    key_butn_const = parse_input_event_codes()
    ctrl_shift = [0, 0]
    caps_num_lock = get_capsnum_lock()
    alph = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    try:
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
                if value_ == 1 or value_ == 2:
                    print("KEY: {}".format(key))

            e = f.read(e_size)
    except KeyboardInterrupt: pass
    finally: f.close()

if __name__ == '__main__':
    main()
