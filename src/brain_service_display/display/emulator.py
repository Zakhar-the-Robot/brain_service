# #!/usr/bin/env python3
# *************************************************************************
#
# Copyright (c) 2022 Andrei Gramakov. All rights reserved.
#
# This file is licensed under the terms of the MIT license.  
# For a copy, see: https://opensource.org/licenses/MIT
#
# site:    https://agramakov.me
# e-mail:  mail@agramakov.me
#
# *************************************************************************

# from tkinter import Tk, Canvas, Frame, BOTH, W

# class Example(Frame):

#     def __init__(self):
#         super().__init__()

#         self.initUI()


#     def initUI(self):

#         self.master.title("OLED")
#         self.pack(fill=BOTH, expand=1)

#         canvas = Canvas(self)
#         canvas.create_text(20, 30, anchor=W, font="Purisa",
#             text="Most relationships seem so transitory")

#         canvas.pack(fill=BOTH, expand=1)


# def main():

#     root = Tk()
#     ex = Example()
#     root.geometry("256x64+300+300")
#     root.mainloop()


# if __name__ == '__main__':
#     main()

import time
import tkinter as tk
from threading import Thread

# class EmuOled():
#     def __init__(self):
#         self.root = tk.Tk()
#         self.root.geometry("256x64+300+300")
#         self.elements = []
#         # self.label1 = tk.Label(self.root, text="Text")
#         # self.label2 = tk.Label(self.root, text="Text")
#         # self.label1.pack()
#         # self.label2.pack()
#         # # self.label1.place(relx = 0.0,
#         # #          rely = 1.0,
#         # #          anchor ='nw')
#         # self.label2.place(relx = 1.0,
#         #          rely = 0.0,
#         #          anchor ='sw')

#     # def changeText(self):
#         # self.label1['text'] = "Text updated"  
        
#     def Text(self, text):
#         self.elements.append(tk.Label(self.root, text="Text"))
        
#     def Clear(self):
#         for el in self.elements:
#             el.delete("1.0", tk.END)
        
#     def start(self):
#         self.root.mainloop()
        
        
# Run tkinter code in another thread

import os
import tkinter as tk
import threading

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
FONT = SCRIPT_PATH + "/long_pixel-7.ttf"

class EmuOled(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.elements = []
        self.root = None
        self.start()
        while not self.root:
            pass
        
    def __del__(self):
        self.clear()

    def callback(self):
        self.root.quit()

    def run(self):
        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        self.root.geometry("256x64+300+300")
        self.root.mainloop()
        
    def text(self, text, y=0, size=15):
        l = tk.Label(self.root, text=text, borderwidth=0,font=("Long Pixel-7",size))
        l.pack(side=tk.TOP, anchor=tk.NW)
        l.place(x=0, y=y)
        self.elements.append(l)
        
    def clear(self, wait_before_sec=0):
        time.sleep(wait_before_sec)
        for el in self.elements:
            el.destroy()
            
    def show_l(self, text, wait_sec: int = 0):
        self.text(text, size=18, y=10)
        self.clear(wait_sec)
        
    def show_sl(self, text_line1, text_line2="", wait_sec: int = 0):
        self.text(text_line1, size=8)
        self.text(text_line2, size=18, y=25)
        self.clear(wait_sec)
            
    def show_mm(self, text_line1, text_line2="", wait_sec: int = 0):
        self.text(text_line1)
        self.text(text_line2, y=30)
        self.clear(wait_sec)                

    def show_clear(self):
        self.clear()

    

if __name__ == "__main__":

    oled = EmuOled()
    oled.show_l("Hello!", 3)
    oled.show_l("I'm Zakhar", 3)
    oled.show_sl("small text", "BIG text", 3)
    oled.show_mm("IP:0.0.0.0", "HOST:NAME", 3)
    print('Now we can continue running code while mainloop runs!')

    for i in range(10000):
        print(i)        
    # oled.clear()
    
    
    

