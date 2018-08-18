# -*- coding: utf-8 -*-
"""
Created on Sat Dec 16 22:20:29 2017

@author: luoxi
"""

#!usr/bin/python
# -*- coding: utf-8 -*-
import pyaudio
import struct
import wave
import math
import numpy as np
from tkinter import *
from PIL import ImageTk
gain=0
#--------------------------------------------
class DragableRect:
    def __init__(self, options):

      self.parent = options["parent"] # canvas
      self.x = options["x"]
      self.y = options["y"]
      self.width = options["width"]
      self.height = options["height"]
      self.outline = options["outline"]
      self.fill = options["fill"]
      self.tag = options["tag"]
      self.axis = options["axis"] # 'h', 'v' or 'both'

      self.selected = False

    def display(self):
      """
      draw rect on parent Canvas
      """
      self.parent.create_rectangle(
            self.x,
            self.y,
            self.x + self.width,
            self.y + self.height,
            fill = self.fill,
            outline = self.outline,
            tags = self.tag)

    def getPos(self):
        """
        return self coords as (x0, y0, x1, y1)
        """
        return self.parent.coords(self.tag)

class DragableCircle:
    pass

#-----------------------------------------------------------------
class DragAndDrop(Tk):
    """
    Tkinter app based on Tk()
    """
    def __init__(self):
        Tk.__init__(self)
        self.title("Tkinter drag and drop")
        self.geometry("1300x650+400+400")
        self.can = Canvas(self, width=1300, height=650, bg="white")
        self.can.pack(expand = YES, fill = BOTH)
        self.image = ImageTk.PhotoImage(file = "Bg.png")
        self.can.create_image(0, 0, image = self.image, anchor = NW)
    #these attributes are used in click, drag and drop methods
        self.click_flag = False
        self.offset_x = 0
        self.offset_y = 0

        self.items = [
        DragableRect({
            "parent": self.can,
            "x": 600,
            "y": 400,
            "width": 10,
            "height": 10,
            "outline": "red",
            "fill": "red",
            "tag": "red",
            "axis": "both"
            }),
        DragableRect({
            "parent": self.can,
            "x": 700,
            "y": 400,
            "width":10,
            "height":10,
            "outline": "yellow",
            "fill": "yellow",
            "tag": "yellow",
            "axis": "both"
        })]

        for i in self.items:
            i.display()

            self.bind("<Button-1>", self.click)
            self.bind("<ButtonRelease-1>", self.drop)
            self.bind("<B1-Motion>", self.drag)  
        
        

    def click(self, evt):
        """
        if a rect is clicked :
        - switch 'click_flag' to True
        - switch rect's 'selected' attribute to True
        - detect mouse offset from top-left corner of clicked rect
        """
        x, y = evt.x, evt.y
        for i in self.items:
            coords = i.getPos()
            if x > coords[0] and x < coords[2]:
                if y > coords[1] and y < coords[3]:
                    self.click_flag = True
                    i.selected = True
                    self.offset_x = x - i.x
                    self.offset_y = y - i.y
                    break

    def drop(self, evt):
        """
        - switch 'click_flag' and dragged rect's 'selected' attribute to False
        - update rect's 'x' and 'y' attributes
        """
        if self.click_flag:
            x, y = evt.x, evt.y
            #print('You clicked at position %d %d' % (x, y))

            self.click_flag = False
            for i in self.items:
                if i.selected:
                    #if i.tag == "red":
                     #   global gain1
                    #    gain1 = y
                    #    global pan1
                   #     pan1 = x/400
                  #  if i.tag == "green":
                   #     global gain2
                   #     gain2 = y
                   #     global pan2
                  #      pan2 = x/400
                    i.x = x - self.offset_x
                    i.y = y - self.offset_y
                    i.selected = False

    def drag(self, evt):
        if self.click_flag:
            x, y = evt.x, evt.y
            #print('You clicked at position %d %d' % (x, y))   
        for i in self.items:
            if i.selected:
                if i.tag == "red":
                        global gain1
                        gain1 = (650-math.sqrt((650-x)**2+(650-y)**2))/4                       
                        d = math.sqrt((650-x)**2+(650-y)**2)
                        cos = (650-x)/d
                        theta = math.acos(cos)
                        global pan1
                        pan1 = theta/math.pi
                if i.tag == "yellow":
                        global gain2
                        gain2 = (650-math.sqrt((650-x)**2+(650-y)**2))/4           
                        d = math.sqrt((650-x)**2+(650-y)**2)
                        cos = (650-x)/d
                        theta = math.acos(cos)
                        global pan2
                        pan2 = theta/math.pi
                self.can.coords(i.tag,
                    x - self.offset_x,
                    y - self.offset_y,
                    (x - self.offset_x) + i.width,
                    (y - self.offset_y) + i.height)
    

#-------------------------------------------------------------------

app = DragAndDrop() 


def Quit(event):
    global Go
    if event.char == 'q':
        print('Stop')
        Go = 0


app.bind("<Key>", Quit)

#print(app.items[0].x,app.items[0].y,app.items[1].x,app.items[1].y)

def clip16(x):  
    # Clipping for 16 bits
    if x > 32767:
        x = 32767
    elif x < -32768:
        x = -32768
    else:
        x = x
    return(x)



wave_file_name = 'horn.wav'
wave_file_name1 = 'drum.wav'

wf = wave.open(wave_file_name, 'rb')
wf1 = wave.open(wave_file_name1, 'rb')

RATE = wf.getframerate()
WIDTH = wf.getsampwidth()
LEN = wf.getnframes()
CHANNELS = wf.getnchannels()

print('The sampling rate is {0:d} samples per second'.format(RATE))
print('Each sample is {0:d} bytes'.format(WIDTH))
print('The signal is {0:d} samples long'.format(LEN))
print('The signal has {0:d} channel(s)'.format(CHANNELS))

p = pyaudio.PyAudio()
stream = p.open(
    format      = pyaudio.paInt16,
    channels    = 2,
    rate        = RATE,
    input       = False,
    output      = True)


Go = 1
gain1 = (650-math.sqrt((650-600)**2+(650-400)**2))/3
gain2 = (650-math.sqrt((650-700)**2+(650-400)**2))/3
pan1 = 600/1300
pan2 = 700/1300


for i in range(LEN):  
    if Go:
        app.update()
    else: break
    input_string = wf.readframes(1)    
    input_string1 = wf1.readframes(1)
    
    input_tuple = struct.unpack('B', input_string)
    input_tuple1 = struct.unpack('B', input_string1)
    # (1 - pan1) * gain1 * input_tuple[0] + 
    # pan1 * gain1 * input_tuple[0] +
    output_block1 = (1-pan1) * gain1 * input_tuple[0] + (1-pan2) * gain2 * input_tuple1[0]
    output_block2 = pan1 * gain1 * input_tuple[0] + pan2 * gain2 * input_tuple1[0]
   # output_tuple1 = tuple(output_block1.astype(int))
   # output_tuple2 = tuple(output_block2.astype(int))
    
    # Convert values to binary string
    output_values = [clip16(int(output_block1)), clip16(int(output_block2))]

    output_string = struct.pack('hh', *output_values)

    # Write binary string to audio output stream
    stream.write(output_string)

print('* Finished')
stream.stop_stream()
stream.close()
p.terminate()
