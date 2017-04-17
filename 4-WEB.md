## 4 Web applications

Now we can control our Blinkt from the command-line or put it into an infinite loop, let's move on and create a web application.

### 4.1 Python Flask

Python Flask is a framework that lets you turn your application into a web-server with very little effort. We will use it for the next task.

**Task: Build a temperature server**

**Flask and `pip`**

The easiest way to install Python dependencies and packages is to use `pip`, `pip` can also be used to install `docker-compose` at a later stage.

We won't install these on our Raspberry Pi, but we will add them to our Dockerfile:

```
FROM blinkt

RUN apt-get update -qq && \
    apt-get install -qy python-pip && \
    pip install flask
```

> These steps will take a few minutes when we build our image below, but they will be cached into one layer.

Now create a minimal Flask webserver to return the system temperature as a JSON value:

The temperature is stored in (milli-degrees) Celsius at `/sys/class/thermal/thermal_zone0/temp`, on the Raspberry Pi you can use the `cat` command to view the current temperature.

*server.py*

```
from flask import Flask, request, render_template
import json
app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    file = open("/sys/class/thermal/thermal_zone0/temp")
    data = file.read().rstrip() # remove trailing '\n' newline character.
    file.close()
    payload = json.dumps({ "temperature": data })
    return payload

if __name__ == '__main__':

    app.run(debug=False, host='0.0.0.0')
```

**Set the network port**

A Flask server listens on port 5000 by default, so let's finish our Dockerfile.

* Add the server.py file to the image
* And include the `EXPOSE 5000` command so that Docker is aware of which ports will be needed

```
FROM blinkt
RUN apt-get update -qy && \
    apt-get install -qy python-pip && \
    pip install flask

WORKDIR /root/
COPY server.py .
EXPOSE 5000

CMD ["python", "server.py"]
```

Build your server and try it out:

```
$ docker build -t tempserver .
$ docker run --name web -p 5000:5000 -d tempserver
```

* The `-p` flag makes sure Docker exposes port 5000 on our Raspberry Pi
* `-d` means the code runs in the background (this means we can't use Control + C)

Now try your website with http://raspberrypi.local:5000/ or with `curl`:

```
$ curl http://raspberrypi.local:5000
{"temperature": "42774"}
```

Kill the webserver with `docker rm -f web`

**Task: return a formatted temperature**

* Now update the Python code so that the milli-degrees temperature is returned in Celsius i.e. (42.0).
* Include Fahrenheit in the output. The [conversion from Celsius to Fahrenheit](http://www.rapidtables.com/convert/temperature/celsius-to-fahrenheit.htm) is `(Celsius * 1.8 + 32)`.

Example response:

```
{"temperatureFahrenheit": "107.6", "temperatureCelsius": "42.0"}
```

String formatting can format a number to a set number of decimal places i.e 4 with `"{:.4f}"` or two with `"{:.2f}"` but it does not apply rounding.

Here's an example of formatting a numeric value that will help with the task: `"{:.1f}".format(0.5166784)`

Rounding can be done through the [round](https://docs.python.org/2/library/functions.html#round) function: `round(number, places)`.

Python has a built-in read–eval–print loop REPL which can be used to test out Python code before integrating it into an application. Start up the image we built and force it to load the REPL like this:

```
$ docker run -ti tempserver /usr/bin/python
>>> "{:.4f}".format(0.5166784)
>>> round(0.5166784, 2)
```

When you're finished hit Control + D or type in `quit()`.

Now update the code to return the example response above. You must run `docker build` before `docker run` after every change.

**Task: deploy a Docker Swarm service**

You can run a single-node Docker Swarm (cluster) with your Raspberry Pi. Unfortunately you won't be able to create a Swarm between your Pi and your laptop unless you are using Wi-Fi or Ethernet connected via USB.

> The new PiZeroW has built-in WiFi and costs around twice the price of the original PiZero, this frees up the USB port for an external hard drive or similar.

Before creating a Swarm service we need to initialize Swarm Mode:

```
$ docker swarm init
```

Now create a service and let Docker deploy it:

```
$ docker service create --name web --replicas=1 --publish 5000:5000 tempserver
```

You may see [an error](https://github.com/docker/docker/issues/29205) similar to this:

```
unable to pin image tempserver to digest: errors:
denied: requested access to the resource is denied
unauthorized: authentication required
```

This is just a warning which translated means "we could not find your image on the internet, so we'll use your local image instead".

As you can see the `docker service create` command is similar to `docker run`, but instead of running a one-shot container, a service will be defined. Docker will automatically restart the task if it exits with an error.

Get a list of the services you've created:

```
$ docker service ls
```

Check on a specific service:

```
$ docker service ps web
```

Please remove the service before going onto the next step with:

```
$ docker service rm web
```

**Task: Scale a service**

We will now create a web-server with Docker Swarm that prints out the name of the running container. This will demonstrate the built-in load balancing pattern (round-robin):

```
$ docker service create --name identity --publish 80:80 alexellis2/nginx-helloworld:armhf
```

Now use the curl command several times to see the container name:

```
$ curl -4 localhost:80
c0ca78f3f58e

$ curl -4 localhost:80
c0ca78f3f58e
```

Scale the service to three replicas using `docker service scale identity=3` and run curl again:

```
$ curl -4 localhost:80
c0ca78f3f58e

$ curl -4 localhost:80
53b5667f8f34

$ curl -4 localhost:80
b45d73f0aa1b

$ curl -4 localhost:80
c0ca78f3f58e
```

The built-in load-balancing can reduce the need for an external load-balancer such as NGinx.

### 4.2 Build an IoT LED server

Now we will allow people to trigger our LEDs over the internet by sending a POST request to our Flask server.

Here is the outline of a Python application:

* It receives a HTTP post to /set_color

* Sets all LEDs to a certain color

* Returns a JSON response with the color values

```python
from flask import Flask, request, render_template
import json

from blinkt import set_clear_on_exit, set_pixel, show

set_clear_on_exit()
app = Flask(__name__)

@app.route('/set_color', methods=['POST'])
def set_color():
    data = request.json
    red = data["red"]
    green = data["green"]
    blue = data["blue"]

    for led in range(0, 8):
        set_pixel(led, int(red), int(green), int(blue))
    show()

    return json.dumps({"status": "OK", "r": red, "g": green, "b": blue })

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
```

We can re-use the same Dockerfile from the previous example:

```
FROM blinkt
RUN apt-get update -qy && \
    apt-get install -qy python-pip && \
    pip install flask

WORKDIR /root/
COPY server.py .
EXPOSE 5000

CMD ["python", "./server.py"]
```

**Task: Build and run the image**

```
$ docker build -t ledserver .
$ docker run --privileged --name web -p 5000:5000 -d ledserver
```

To access the LED server either install the Google Chrome extension (Postman) or use `curl`:

*Turn the LEDs red*

```
$ curl -H "Content-type: application/json" -d '{"red": 10, "green":0, "blue":0 }' raspberrypi.local:5000/set_color

{"status": "OK", "r": 10, "b": 0, "g": 0}
```

*Turn the LEDs off*

```
$ curl -H "Content-type: application/json" -d '{"red": 0, "green":0, "blue":0 }' raspberrypi.local:5000/set_color

{"status": "OK", "r": 0, "b": 0, "g": 0}
```

Unfortunately you cannot create a Docker Swarm service for this application because it needs to run in `--privileged` mode.

**Task: Hack the program to change the color of individual LEDs**

To maintain backwards compatibility add a new route for `/set_colors`

The JSON request to change an individual LED should be an array with 8 sets of RGB values:

```
[ {"red": 0, "green": 0, "blue": 0},
 {"red": 0, "green": 0, "blue": 0},
 {"red": 0, "green": 0, "blue": 0},
 {"red": 0, "green": 0, "blue": 0},
 {"red": 0, "green": 0, "blue": 0},
 {"red": 0, "green": 0, "blue": 0},
 {"red": 0, "green": 0, "blue": 0},
 {"red": 0, "green": 0, "blue": 0}]
```

When you've updated the code build and run the new image:

```
$ docker build --build-arg http_proxy=$http_proxy --build-arg https_proxy=$https_proxy \
  -t setcolors .
$ docker run --privileged --name setcolors -d -p 5000:5000 setcolors:latest
```

Now use `curl` to set each LED to different colors:

```
$ export no_proxy="raspberrypi.local"
$ curl http://raspberrypi.local:5000/set_colors -H "Content-type: application/json" -d '
[{"red": 100, "green": 0, "blue": 0},
 {"red": 0, "green": 100, "blue": 0},
 {"red": 0, "green": 0, "blue": 100},
 {"red": 0, "green": 100, "blue": 0},
 {"red": 100, "green": 0, "blue": 0},
 {"red": 0, "green": 100, "blue": 0},
 {"red": 0, "green": 0, "blue": 100},
 {"red": 0, "green": 100, "blue": 0}
]'
```

When you've tried a few different combinations send an "off" signal, then kill the container:

```
$ curl -H "Content-type: application/json" -d '{"red": 0, "green":0, "blue":0 }' raspberrypi.local:5000/set_color

{"status": "OK", "r": 0, "b": 0, "g": 0}

$ docker rm -f setcolors
```

### 4.3 Rolling swarm updates

Docker Swarm allows us to perform a rolling update to a live set of Swarm services. Let's see that in action.

```
$ docker service create --name progressbar \
  --mount type=bind,source=/sys,destination=/sys \
  --mode=global alexellis2/progress-blinkt:red
```

* `--name progressbar` - gives the service an identity we can use with `docker service rm/ps/inspect`
* `--mount` - makes the Pi's GPIO pins accessible within Docker Swarm
* `--mode=global` - makes sure we only ever run one of these tasks per host in the swarm

We start off with a red progress bar animation from the `alexellis2/progress-blinkt:red` image.

Now perform a rolling update with `docker service update`:

`$ docker service update progressbar --image=alexellis2/progress-blinkt:blue`

The Pi will download a 655 KB image and then kill the red container before switching over.

If this was a production deployment and we found a bug in the image, we could type in `docker service update progressbar --rollback`

There is also a green image if you would like to try that: `alexellis2/progress-blinkt:green`

> For more reading checkout the tutorial: [Control GPIO with Docker Swarm
](http://blog.alexellis.io/gpio-on-swarm/)

**Tiny Docker images**

The smallest Docker images either contain a single static binary (like the progress-blinkt image) or they are based upon the Alpine Linux image which normally comes in at around 2-5MB.
