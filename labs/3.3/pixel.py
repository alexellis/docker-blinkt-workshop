#!/usr/bin/env python
from blinkt import set_clear_on_exit, set_pixel, show

import time

set_clear_on_exit()

for i in range(0, 8):
   set_pixel(i, 0, 255, 0)
show()

time.sleep(1) # 1 = 1 second
