# Docker and IoT

**Get into physical computing with the Pimoroni Blinkt! add-on**

* The Raspberry Pi is a low-energy microcomputer the size of a credit-card and has sold over 10 million units educating children and inspiring makers alike.

* With the Pi, you'll be building, shipping and running Docker containers in no time and learning how to interact with physical hardware to create your own IoT devices.

* You will also get a chance to play with Docker Swarm on your Pi to deploy a micro-service. And, you will take home a free Raspberry Pi Zero kit, including a super bright Pimoroni Blinkt! 8-LED RGB add-on.

### Pre-requisites

* Install a text editor

If you don't usually work with code then please install one of the following cross-platform text-editors:

* [Visual Studio Code](https://code.visualstudio.com)
* [Atom](https://atom.io)

**For Windows users**

* Install Git for Windows

Please go ahead and install Git for Windows so that you have access to `ssh`, `scp`, `sftp` and a terminal:

https://git-scm.com/downloads

* Install Bonjour networking service

The Raspberry Pi uses Apple's Bonjour/Avahi service to advertise its IP address. You will need to install Bonjour which is packaged in the following download. If you have iTunes installed you should already have the Bonjour service installed and started.

* [Bonjour Print Services for Windows](https://support.apple.com/kb/DL999?locale=en_US)

> If you struggle to setup Internet Connection Sharing because you're on Linux or a picky WiFi network then please follow the guide for configuring a [Proxy server](https://github.com/alexellis/docker-blinkt-workshop/blob/master/PROXIES.md).

### Workshop format

This is a self-paced workshop designed for Dockercon. It starts with Part 1 which involves setting up the Pi and Blinkt then moves onto building Docker images and programming the Blinkt.

The final part involves putting everything together to create an application. You can do this individually or pair up.

**Dockercon notes:**

> We will have TAs on-hand to help out. Please let us know if you need help or if things aren't working right.

### [Part 1 - Setup](https://github.com/alexellis/docker-blinkt-workshop/blob/master/1-SETUP.md)

Flash Raspbian, configure OTG networking and Internet Connection Sharing, then install Docker.

### [Part 2 - Build](https://github.com/alexellis/docker-blinkt-workshop/blob/master/2-BUILD.md)

Run your first ARM Docker container, learn about base image differences and prepare to work with GPIO. 

### [Part 3 - Blinkt](https://github.com/alexellis/docker-blinkt-workshop/blob/master/3-BLINKT.md)

Get familiar with the Blinkt and start hacking

### [Part 4 - Web applications](https://github.com/alexellis/docker-blinkt-workshop/blob/master/4-WEB.md)

Understand how to create a Web application in Python and an IoT LED server

### [Part 5 - Hack](https://github.com/alexellis/docker-blinkt-workshop/blob/master/5-HACK.md)

Put everything you've learnt into practice on a larger application.

### [Conclusion](https://github.com/alexellis/docker-blinkt-workshop/blob/master/CONCLUSION.md)

Find out how to use your Pi Zero at home and where to find more great content. 
