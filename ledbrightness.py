#!/usr/bin/python
# -*- coding: utf-8 -*-
 
# graphical test of pyfirmata and Arduino; read from an LM35 on A0,
#                                          brighten an LED on D3 using PWM
# Connections:
# - small LED connected from D3, through a 1kO resistor to GND;
# - LM35: +Vs -> +5V, Vout -> A0, and GND -> GND.

 
import pyfirmata
import sys                              # just for script name and window
from Tkinter import *
 
# Create a new board, specifying serial port
board = pyfirmata.Arduino('/dev/ttyACM0')
 
# start an iterator thread so that serial buffer doesn't overflow
it = pyfirmata.util.Iterator(board)
it.start()
 
# set up pins
pin0=board.get_pin('a:0:i')             # A0 Input      (LM35)
pin3=board.get_pin('d:3:p')             # D3 PWM Output (LED)
 
# IMPORTANT! discard first reads until A0 gets something valid
while pin0.read() is None:
    pass
 
def get_temp():                         # LM35 reading in °C to label
    selection = "Temperature: %6.1f °C" % (pin0.read() * 5 * 100)
    label.config(text = selection)
    root.after(500, get_temp)           # reschedule after half second
 
def set_brightness(x):  # set LED; range 0 .. 100 called by Scale widget
    y=float(x)
    pin3.write(y / 100.0)               # pyfirmata expects 0 .. 1.0
 
def cleanup():                          # on exit
    print("Shutting down ...")
    pin3.write(0)                       # turn LED back off
    board.exit()
 
# now set up GUI
root = Tk()
root.wm_title(sys.argv[0])              # set window title to program name
root.wm_protocol("WM_DELETE_WINDOW", cleanup) # cleanup called on exit
scale = Scale( root, command=set_brightness, orient=HORIZONTAL, length=400,
               label='Brightness')      # a nice big slider for LED brightness
scale.pack(anchor=CENTER)
 
label = Label(root)
label.pack(anchor='nw')                 # place label up against scale widget
 
root.after(500, get_temp)               # start temperature read loop
root.mainloop()