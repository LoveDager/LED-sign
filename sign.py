#!/usr/bin/env python
# coding=utf-8
# Display a runtext with double-buffering.
from itertools import count
import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/../rpi-rgb-led-matrix/bindings/python'))
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/../rpi-rgb-led-matrix/bindings/python/build'))
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/../rpi-rgb-led-matrix/bindings/python/rgbmatrix'))
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/../rpi-rgb-led-matrix/bindings/python/samples'))
sys.path.append(os.path.abspath('/usr/lib/python3/dist-packages'))

import urllib3
import requests
import httplib

from samplebase import SampleBase
from rgbmatrix import graphics
import time
import json

from dateutil.relativedelta import relativedelta
from datetime import datetime


class RunText(SampleBase):
    def __init__(self, *args, **kwargs):
        super(RunText, self).__init__(*args, **kwargs)

    def waitForInternet(self):
        conn = httplib.HTTPConnection("www.google.com", timeout=5)
        while True:
            try:
                conn.request("HEAD", "/")
                conn.close()
                return
            except:
                conn.close()
                pass
    
    def updateData(self):
        endDate = datetime(2023,2,27,11,15)
        rd = relativedelta(endDate, datetime.now())

        print(rd.__dict__)

        # Countdown
        if(rd.month > 0):
            countdown = "%(months)dm, %(days)dd left" % rd.__dict__
        elif(rd.days > 0):
            countdown = "%(days)dd, %(hours)dh left" % rd.__dict__
        elif(rd.hours > 0):
            countdown = "%(hours)dh, %(minutes)dm left" % rd.__dict__
        else:
            countdown = "%(minutes)dm, %(seconds)ds left" % rd.__dict__

        return countdown

    def run(self):

        ### Check for internet connection

        self.waitForInternet()
    
        ### Script start

        timeLeft = self.updateData()

        ##### Set up LED #####
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font11 = graphics.Font()
        font11.LoadFont("./font11.bdf") # Load font file
        font14 = graphics.Font()
        font14.LoadFont("./font14.bdf") # Load font file
        textColor = graphics.Color(180, 160, 90) # Set color to beige
        textColorBlue = graphics.Color(50, 50, 200) # Set color to blue
        pos = offscreen_canvas.width
        
        width = graphics.DrawText(offscreen_canvas, font14, 0, 30, textColor, "1")

        while True:
            offscreen_canvas.Clear()
            # Destination text
            graphics.DrawText(offscreen_canvas, font11, 1, 12, textColor, u'Boarding')
            graphics.DrawText(offscreen_canvas, font11, 50, 12, textColor, u'in:')

            graphics.DrawText(offscreen_canvas, font14, 0, 28, textColorBlue, timeLeft)

            # Update every second
            time.sleep(1)
            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)

            timeLeft = self.updateData()

# Main function
if __name__ == "__main__":
    run_text = RunText()
    if (not run_text.process()):
        run_text.print_help()
