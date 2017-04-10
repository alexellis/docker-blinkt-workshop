#!/usr/bin/env python
from blinkt import set_clear_on_exit, set_pixel, show

import time

set_clear_on_exit()

red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
colors = [red,green,blue]

for color in colors:
    for i in range(0, 8):
       set_pixel(i, color[0], color[1], color[2])
       show()
       time.sleep(0.5)
