#!/usr/bin/env python
# coding=utf-8
# Display a runtext with double-buffering.
import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/../rpi-rgb-led-matrix/bindings/python'))
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/../rpi-rgb-led-matrix/bindings/python/build'))
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/../rpi-rgb-led-matrix/bindings/python/rgbmatrix'))
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/../rpi-rgb-led-matrix/bindings/python/samples'))
sys.path.append(os.path.abspath('/usr/lib/python3/dist-packages'))

import httplib

from samplebase import SampleBase
from rgbmatrix import graphics
import time
import json



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

    def run(self):

        ##### Set up LED #####
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font11 = graphics.Font()
        font11.LoadFont("./font11.bdf") # Load font file
        font14 = graphics.Font()
        font14.LoadFont("./font14.bdf") # Load font file
        textColor = graphics.Color(180, 160, 90) # Set color to beige
        textColorWarning = graphics.Color(220, 100, 50) # Set color to red
        pos = offscreen_canvas.width

        offscreen_canvas.Clear()
        # Destination text
        graphics.DrawText(offscreen_canvas, font11, 2, 12, textColor, u'Starting')
        graphics.DrawText(offscreen_canvas, font11, 2, 25, textColor, u'sign...')
        offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)

        time.sleep(5)

        graphics.DrawText(offscreen_canvas, font11, 2, 12, textColorWarning, u'Awaiting')
        graphics.DrawText(offscreen_canvas, font11, 2, 25, textColorWarning, u'connection')

        self.waitForInternet()

# Main function
if __name__ == "__main__":
    run_text = RunText()
    if (not run_text.process()):
        run_text.print_help()
