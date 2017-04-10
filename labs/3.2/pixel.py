#!/usr/bin/env python
from blinkt import set_clear_on_exit, set_pixel, show

import time

set_clear_on_exit()
set_pixel(0, 255, 0, 0)
show()

time.sleep(1) # 1 = 1 second
