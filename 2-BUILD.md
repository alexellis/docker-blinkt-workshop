## 2 Build

### 2.1 - Base images for ARM devices.

The two base images we will use for the workshop are:

* `resin/rpi-raspbian:jessie`

This image is produced by the [resin.io](https://resin.io) team who created a managed solution around IoT devices. It is ideal for Raspberry Pis because it is a very minimal version of Raspbian.

You can use commands you may already be used to such as `apt-get install` and `dpkg`.

> Docker base images tend to lack the common utilities we're used to such as `git`, `unzip` and even `man` pages. 

* `armhf/alpine:latest`

The Alpine Linux images became popularized about 18 months ago, this Linux distribution builds against a C library called Musl instead of the standard GNU GLibc library meaning that it can fit a complete container OS inside a 2MB download.

The `armhf` organization on the Docker Hub is maintained by Tianon, a contributor to the Docker project and the official set of images. He produces the `armhf` images through a Continuous Integration (CI) pipeline.

**Auto-building Docker images**

Dockerfiles for regular hardware such as that found in laptops and on the cloud can be built through an automated process in the Docker Hub. Unfortunately there is no support for auto-building Docker ARM images. For this reason be very cautious of running images from untrusted sources.

**Pull the base images**

Please start pulling the base images down from the Docker Hub, this could take a few minutes.

```
$ docker pull resin/rpi-raspbian:jessie
$ docker pull armhf/alpine:latest
```

### 2.1b

If you're unfamiliar with working with a Linux system or how to code on a Raspberry Pi please read this guide:

* [Coding on a Raspberry Pi](https://github.com/alexellis/docker-blinkt-workshop/blob/master/CODING.md)

This helps explain:

* working a text editor on the Pi
* synchronizing files

### 2.2 - Running your first ARM container

Now let's start a container with an interactive shell:

```
$ docker run -p 80:80 --name web -ti armhf/alpine:latest sh
```

If you're running behind a proxy then make sure you head over to the [proxy setup guide](https://github.com/alexellis/docker-blinkt-workshop/blob/master/PROXIES.md):

```
$ docker run -e http_proxy=$http_proxy -e https_proxy=$https_proxy \
  -p 80:80 --name web -ti armhf/alpine:3.5 sh
```

* The `-e` parameter to `docker run` is used to make an environmental variable available inside the container. This is useful way of updating how a program works without changing code. 


Now install and start `nginx`:

```
/ # mkdir -p /run/nginx/

/ # apk add --update nginx

/ # nginx
/ #
```

We've just started an ARM container with Alpine Linux, the `apk add` instruction added a tiny web-server and when we ran the container we passed in `-p` which meant we opened up a port for it.

* The `-ti` command meant we created an interactive connection to the container, where we can type input and read output
* The final part of the command `sh` gives us a shell to type in commands, but this could be anything such as `ls` or `cat /etc/hostname`

Go to your laptop and open http://raspberrypi.local in a web browser or `no_proxy="raspberrypi.local" curl -4 http://raspberrypi.local` from a Terminal.
  
You should now see something like:

```
404 not found

Nginx
```

That message is OK because we've not added any config for a website yet. If you see the text nginx on the page/response then the container is working.

On the Raspberry Pi type in `exit` to close the shell to the container and exit.

```
/ # exit
```

We should now remove the stopped `web` container. Type in:

```
docker rm web
```

If the container is still running, then you can use this shorthand (which does a kill then remove):

```
docker rm -f web
```

### 2.3 Build an ARM Dockerfile

So now let's create a Dockerfile to do all of the above, so that we don't have to type in commands manually.

> You can create a folder with the `mkdir folder_name` command and then use `cd folder_name` to enter into it.

Create a config file for a virtual website under the name `raspberrypi.conf`:

```
server {
        server_name _;         

        listen 80 default_server;
        listen [::]:80 default_server;

        root /var/www/html;
        index index.html index.htm index.nginx-debian.html;

        location / {
                try_files $uri $uri/ =404;
        }
}
```
**raspberrypi.conf**

Now let's build a Dockerfile to automate what we did in the previous step:

```
FROM armhf/alpine:3.5
RUN apk add --update nginx
RUN mkdir -p /run/nginx/
RUN rm /etc/nginx/conf.d/default.conf
RUN mkdir -p /var/www/html/
RUN echo "<html>Welcome to your Raspberry Pi</html>" | tee -a /var/www/html/index.html

COPY raspberrypi.conf /etc/nginx/conf.d/

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```
*Dockerfile*

**Explaining the Dockerfile**

A Dockerfile means we get a repeatable image each time we perform our build. We can share Dockerfiles with other people and normally check them into our source control management system. This means that anyone can build a project with a Dockerfile without having to install any other dependencies.

There are a few differences between using a Dockerfile and running steps in a shell through a container:

* We picked a base image to start off from, any changes we need are laid over the top of this base
* We added several `RUN` instructions which correspond to something we would type into a bash prompt
* We copied in `raspberrypi.conf` from our host into the image so there would be a default website

Finally:
* We added a `CMD` instruction that will by invoked immediately when we type in `docker run`

Build the image like this if you're not using a proxy:
```
$ docker build -t pi-nginx .
```

If you're behind a proxy build the container like this:

```
$ docker build --build-arg http_proxy=$http_proxy --build-arg https_proxy=$https_proxy \
  -t pi-nginx .
```

Now test out the image:

```
$ docker run -p 80:80 -d --name web pi-nginx
$ docker ps
```

In the example `-p 80:80` uses a static port mapping from the container to the host on port 80. Docker allows us to change the port on the host. That means we can run more than one instance of the container. For example we could bind to port 8080 on the host:

```
$ docker run -p 8080:80 -d pi-nginx
```

For scalability we sometimes want to run on any free port with the `-P` flag. After creating a container with the `-P` flag `docker port` or `docker ps` will show you which host port was used.

Here's an example:

```
$ docker run -P -d pi-nginx
7490d74f8bb963727d3b4e6868dd052d89a08da0e1399017f61c212df5043373

$ docker port 7490d
80/tcp -> 0.0.0.0:32768


$ docker run -P -d pi-nginx
882f86c8e213b463c6970d190f412a26701fd595c5b2ad348b291004d31e8643

$ docker port 882f
80/tcp -> 0.0.0.0:32769
```

We can type in the full URL into a web-browser: http://raspberrypi.local:32768 for example.

The following short-cut will remove all the containers in our system leaving the images behind. If a container is still running it will be killed first because of the `-f` flag:

```
$ docker ps -aq | xargs docker rm -f
```

### 2.3b Optimizing a Dockerfile

A new Docker container is used to build each step in a Dockerfile, you will see these temporary containers in the output from `docker build` shortly. This can be slow on the Pi Zero, so ideally we want to reduce the amount of instructions by using fewer `RUN` commands and combining the instructions.

Here is an optimized version of the Dockerfile:

```
FROM armhf/alpine:latest
RUN apk add --update nginx && \
    mkdir -p /run/nginx/ && \
    rm /etc/nginx/conf.d/default.conf && \
    mkdir -p /var/www/html/ && \
    echo "<html>Welcome to your Raspberry Pi</html>" | tee -a /var/www/html/index.html

COPY raspberrypi.conf /etc/nginx/conf.d/

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

Another side-effect of fewer lines in a Dockerfile is that it can take up less space on disk and be quicker to share between environments.

### 2.4 - Get the Blinkt library from Github

The Raspbian Lite image is perfect for a headless server, especially when compared to the Pixel edition which is packed pull of applications and UI utilities. This does mean we need to install essential tools like `git`.

Install `git` on the Pi:

```
$ sudo -E apt-get update && \
  sudo -E apt-get install -qy git
```

**Clone the Blinkt! library**

```
$ git clone http://github.com/pimoroni/blinkt
```

**Build a Blinkt! Docker image**

You can explore the code, or start building a Blinkt! Docker image right way.

```
$ cd blinkt
$ docker build -t blinkt .
```

> If you're using a proxy remember to pass `--build-arg` as demonstrated in 2.3.

This could take up to 5 minutes if you have already downloaded the base image. I measured 7m41 including a download of Resin's image from the Docker Hub.

**Layer caching**

Fortunately Docker has a very effective caching mechanism and if you issued another `docker build` without making further changes then this would only take a few seconds. Each line in the Dockerfile (generally) is split up into separate layers and each of those can be cached separately. I measured 1.4s on the second build.

> For the Pi it's especially important to keep the changing parts such as the application source-code near the end of the file so that only the affected parts need to be re-built each time you change something.

In the meantime spend 5-10 minutes checking out some of the Python examples provided in the repository:

Some of the examples require additional libraries and alterations to the Dockerfiles, so stick to the ones which run out of the box.

* [Blinkt! examples](https://github.com/pimoroni/blinkt/tree/master/examples)

**Question:**

Which example does the Dockerfile invoke by default?
