# 3 Blinkt

### 3.1 - Knight Rider

**System privileges**

Docker runs containers by default in a sandbox with reduced system capabilities. For GPIO or Physical Computing we need full system privileges. This can be overridden by passing `--privileged` to Docker run.

```
$ docker run --privileged -ti blinkt

^CTraceback (most recent call last):
  File "larson.py", line 28, in <module>
    time.sleep(0.1)
KeyboardInterrupt
```

Now hit Control+C, edit the Dockerfile to run a different example, re-build and run it again.

**Larson Scanner**

The larson.py example is inspired by a futuristic car from an 80s TV show:

* [Knight Rider KITT](https://en.wikipedia.org/wiki/KITT#KITT_.28Knight_Industries_Two_Thousand.29)

The code uses a Sine wave to produce a looping red LED pulse from left to right.

### 3.2 - Controlling the LEDs

We'll now create our own example and rebuild the Dockerfile to run it instead of the Larson Scanner.

* Make a new directory for this example with `mkdir folder_name` then type in `cd folder_name`.

* Create a new example file named pixel.py and copy in the lines below:

The following program will set the first LED to red for 1 second and then turn it off again.

If this file is run from the command-line i.e. `./pixel.py` the below tells our shell how to intepret the file. It's not necessary to add this but it is best practice.

```
#!/usr/bin/env python
```

Now import the blinkt library and the `time` library so we can inject a pause

```
from blinkt import set_clear_on_exit, set_pixel, show
import time
```

Now let's make sure the Blinkt turns off if we hit Control + C.

```
set_clear_on_exit()
```

Now set a pixel to a colour such as red and call `show` so that the LEDs reflect the change:

```
set_pixel(0, 255, 0, 0)
show()
time.sleep(1) # 1 = 1 second
```

Here is the whole file for pixel.py:

```
#!/usr/bin/env python

from blinkt import set_clear_on_exit, set_pixel, show
import time

set_clear_on_exit()

set_pixel(0, 255, 0, 0)
show()
time.sleep(1) # 1 = 1 second
```
*pixel.py*

**Create the Dockerfile**

Because we already have a base image called `blinkt` with everything we need, we can use that as a base to build a new image with our `pixel.py` program:

```
FROM blinkt

WORKDIR /root/
COPY pixel.py .

CMD ["python", "pixel.py"]
```

Now build and run the new image:
```
$ docker build -t pixel .
$ docker run --privileged -ti pixel
```

The first LED will turn red for one second and then turn off. You could try changing the colour before moving onto the next step.

**Blinkt docs**

Checkout the [Blinkt Docs](http://docs.pimoroni.com/blinkt/) for the ordering of parameters and to see how to make different coloured combinations.

This is the signature for `set_pixel`:

```
set_pixel(led_number, red, green, blue)
```

The led_number should be between 0 and 7.


### 3.3 Light up all LEDs

Now see if you can write a loop to light up all of the LEDs with a 0.5 second delay between each.

A for loop in python takes this format:

```
for x in range(0, 8):
    print("This is value " + str(x))

This is value 0
This is value 1
This is value 2
This is value 3
This is value 4
This is value 5
This is value 6
This is value 7
```

### 3.4 Live coding

Sometimes the workflow of `docker build` / `docker run` is quick enough for us to be productive. There is an alternative which allows us to iterate much more quickly without having to rebuild our container after each change.

**Task: make a rainbow**

We want to create a loop in our Python application to cycle through the colours of red, green and blue.

* Loop over each of the colours (R,G,B)
   * Loop over each of the LEDs
      * set the pixel colour
      * update the display
      * wait for 0.5 seconds

Even as a seasoned programmer it is still possible to make mistakes and to get typos, so we'll work with a "live coding" environment. Live coding can help us make rapid changes without rebuilding a Docker image.

Create a new folder for this lab with `mkdir` and `cd` into it.

The `pwd` command shows us the current path on a Linux shell. We will use this when running the live container:

```
$ pwd
/home/pi/dockercon-blinkt/labs/3.4
```

Now we can share that folder into our Blinkt container with a (bind mount) and the `-v` flag:

```
docker run --privileged -v `pwd`:/root/examples -ti blinkt bash
```

**Notes on live coding:**

* On the Raspberry Pi our code will be found in the /root/ directory ready for us to edit
* We won't have any editor in the container, but we can use one on the Raspberry Pi (host) and our changes will reflect
* Open a second `ssh` session to the Raspberry Pi to edit the code

This is the answer to the coding task, it uses a Python feature called *tuples*.

```
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
```

**Task: loop forever**

Can you make it loop forever or until Control + C is hit?

**Task: create a Dockerfile for your code**

Once you have finished your live coding session you may have created new files, make sure any changes you've made are reflected in your Dockerfile. Build a Docker image with your changes.

