# *************************************************************************
#
# Copyright (c) 2021 Andrei Gramakov. All rights reserved.
#
# This file is licensed under the terms of the MIT license.  
# For a copy, see: https://opensource.org/licenses/MIT
#
# site:    https://agramakov.me
# e-mail:  mail@agramakov.me
#
# *************************************************************************

class Display:
    def __init__(self, emulator=False) -> None:
        self.emulator = emulator
        if self.emulator:
            from .emulator import EmuOled
            self.display = EmuOled()
        else:
            from .luma_ssd1306_mod import ssd1306_mod
            from luma.core.interface.serial import i2c
            bus = i2c(port=1, address=0x3C)
            self.display = ssd1306_mod(bus, rotate=2, height=32)

    def clear(self):
        self.display.show_clear()

    def show_l(self, text, wait_sec: float = 0):
        if text is None:
            text = ""
        self.display.show_l(text, wait_sec)

    def show_sl(self, text_line1, text_line2="", wait_sec: float = 0):
        if text_line1 is None:
            text_line1 = ""
        if text_line2 is None:
            text_line2 = ""
        self.display.show_sl(text_line1, text_line2, wait_sec)

    def show_mm(self, text_line1, text_line2="", wait_sec: float = 0):
        if text_line1 is None:
            text_line1 = ""
        if text_line2 is None:
            text_line2 = ""
        self.display.show_mm(text_line1, text_line2, wait_sec)
