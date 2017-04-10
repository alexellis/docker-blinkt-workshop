## 5 Hack

In this final part of the workshop we turn things over to you to start hacking. A guide is provided as a starting-point:

### 5.1 Build a status monitor for an API or tool

Now that we've created what is effectively an LED as a Service we can combine that with other information on the Internet to create a meaningful project.

Here are some ideas:

#### Hack on something completely different

You can take the Pi Zero and Blinkt in your own direction, you may want to do this if you already have ideas or are used to programming with Python.

#### 1. Github issue tracker - change colour depending on the number of issues on your repository

Github libraries are available here: https://developer.github.com/libraries/

#### 2. Build monitor - query JenkinsCI to see if the Docker CI builds are working correctly.

If you go down this route, don't try to run Jenkins on the Pi Zero, but on your laptop.

* [Jenkins on Docker tutorial](http://blog.alexellis.io/jenkins-2-0-first-impressions/)

* Python Gist [jobstatus.py](https://gist.github.com/alexellis/55677236693d82b3bdcdccccd23df8fb)

#### 3. Create a web-page to control the Blinkt

You could also create a web-page to control the Blinkt using Python Flask.

Below is an example of a Flask site that plays Internet radio stations using jQuery and Flask view templates: 
* [alexellis/pyPlaylist](https://github.com/alexellis/pyPlaylist).

* [Flask quickstart](http://flask.pocoo.org/docs/0.12/quickstart/)

#### 4. Show the number of people in space as LEDs between 0 and 8

We'll outline the code for this if you would prefer to follow the workshop track.

**Show the number of people in space**

Let's put together a skeleton application for counting astronauts.

If you didn't get around to enhancing the LED server code in the previous example, then you can use the code in the Labs/4.3a folder which allows you to turn on individual LEDs.

*Dockerfile*

```
FROM blinkt
RUN apt-get update -qy && \
    apt-get install -qy python-pip && \
    pip install requests

WORKDIR /root/
COPY app.py .
EXPOSE 5000
CMD ["python", "./app.py"]
```

We can drop the Flask installation here, but we will need the `requests` modules for HTTP/HTTPs calls to an API.

*app.py*

```
import requests
import json
import time
import os

def get_amount():
    output = requests.get("http://api.open-notify.org/astros.json")
    payload = output.json()
    return payload["number"]

def post_colors(host, amount):
    body = {"red": 0, "green": 0,"blue": 0}
    if amount == 6:
        body["red"] = 255
        body["blue"] = 0
        body["green"] = 0

    output = requests.post(host+"/set_color", json=body)
    return output.status_code

while(True):
    host = os.getenv("HOST_URL")
    amount = get_amount()
    status = post_colors(host, amount)
    print(str(status))

    time.sleep(5)
```

Build and run the application:

```
$ docker build -t monitor .
$ docker run -e HOST_URL=http://raspberrypi.local:5000 -ti monitor
```

> If raspberrypi.local gives you an error, then find the IP address of usb0 and use that instead, i.e. `ifconfig usb0`

We have used an environmental variable to configure the URL for the Raspberry Pi's URL, this is useful especially if we have more than one Pi we need to address or if we change the hostname. To pass variables to docker at runtime use `-e key=value` and to pass them at build time use `--build-arg key=value`.

**A note on rate-limiting**

Before you start querying an API over the Internet it's always a good idea to check if rate limiting is enforced. This is where you are limited on how many requests you can make per second, per hour or per day. Sometimes registering for an official account with a service extends the amount of API hits you can request per day.

* [Github rate limiting rules](https://developer.github.com/v3/#rate-limiting)
