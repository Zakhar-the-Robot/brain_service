#!/usr/bin/python

import sys, os
from time import sleep
from threading import Lock
from zakhar_pycore.zakhar__i2c import *
from zakhar_pycore.zakhar__control import *
bus = SMBus(1)  # indicates /dev/ic2-1


def wait_key():
    ''' Wait for a key press on the console and return it. '''
    result = None
    if os.name == 'nt':
        import msvcrt
        result = msvcrt.getch()
    else:
        import termios
        fd = sys.stdin.fileno()

        oldterm = termios.tcgetattr(fd)
        newattr = termios.tcgetattr(fd)
        newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
        termios.tcsetattr(fd, termios.TCSANOW, newattr)

        try:
            result = sys.stdin.read(1)
        except IOError:
            pass
        finally:
            termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)

    return result

if __name__ == "__main__":
    # scan_all()
    addr= 0x2c
    val=0xab
    # bus.write_block_data(addr, reg, [0x1])
    # sleep(.01)
    # sleep(.02)
    # bus.write_byte_data(addr, reg, val) # write
    # sleep(.02)
    # sleep(.02)
    while(1):
        # i2c_write_byte_data(addr, 0x10, val)# write
        # i2c_write_byte_data(12addr, 0x10, val)# write
        print("Press the key: ")
        i2c_write_byte_data(addr, 0, ord(wait_key()))# write
        # print( "[ 0x%x\t 0x%x\t 0x%x\t 0x%x\t 0x%x\t 0x%x\t 0x%x\t 0x%x ]" %
        #     (
        #         i2c_read_byte_from(addr,0x0),
        #         i2c_read_byte_from(addr,0x1),
        #         i2c_read_byte_from(addr,0x2),
        #         i2c_read_byte_from(addr,0x3),
        #         i2c_read_byte_from(addr,0x4),
        #         i2c_read_byte_from(addr,0x5),
        #         i2c_read_byte_from(addr,0x6),
        #         i2c_read_byte_from(addr,0x7)
        #     ))
        # sleep(.1)