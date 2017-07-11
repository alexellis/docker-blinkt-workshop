## 1 - Setup

### The Pimoroni Blinkt! kit

The Dockercon workshop kit was designed in conjunction with Pimoroni, a maker and educator from Sheffield in the UK.

Contents:

* Presentation box and stickers
* Raspberry Pi Zero with soldered 40-pin header
* MicroSD Card and SD card adapter
* 50cm red micro-USB cable
* Blinkt

> The kit is yours to take home and keep. The Pi can also be powered by a phone charger with a USB WiFi or Ethernet dongle.

### 1.1 Download the Raspbian ISO

> Note: if you are following this material at a conference we may make alternative arrangements to make downloading the ISO quicker such as exchanging USB keys or a local mirror.

We will be using the Pi's official Operating System which comes in two flavours - Pixel (with full UI, games and utilities) and Lite (ideal for Docker and headless use).

Head over to [Raspberry Pi Downloads page](https://www.raspberrypi.org/downloads/raspbian/) and click "RASPBIAN JESSIE LITE".

If you're on a Mac then the file will be uncompressed when the download completes, on Windows or Linux you will need to decompress the archive.

You can use [Etcher.io](https://etcher.io) flashing tool on Windows/Mac and Linux to flash your SD card. Etcher.io will perform a checksum after writing the card to make sure it is valid.

You will be asked for your password on MacOS after clicking the Flash button. 

![Etcher](https://pbs.twimg.com/media/C29Ex0WXUAERiXw.jpg)

> If you don't have an SD-card slot in your laptop then we will provide an external USB device.

### 1.2 Don't boot yet

Before booting up the Pi we need to make some changes on the `boot` partition to reduce the RAM allocated to the GPU and to enable the Pi to work over a USB cable rather than with a WiFi or Ethernet adapter.

Eject the SD card and re-insert if the `boot` partition is not visible.

**GPU RAM split**

Edit `config.txt` in the boot partition. On a Mac this will be mounted under `/Volumes/boot`. On Windows this will show up as a drive called `boot`.

Add these two lines at the end of the file:

```
dtoverlay=dwc2
gpu_mem=16
```

**Enable OTG**

Edit the `cmdline.txt` file. 

**Make sure everything is kept on one line, do not split the line or it will break the system.**

* Find the part of the line that says `rootwait`. 
* Add a (space) after `rootwait` then the following: `modules-load=dwc2,g_ether`

**Enable SSH**

The Raspberry Pi foundation took the decision to disable SSH on their Operating System by default, but this can be overridden by creating a file with any contents in the boot partition called `ssh` with no extension.

If you're on a Mac, type in `touch /Volumes/boot/ssh` to create the file. On Windows make sure that you don't end up creating a file called ssh.txt (with an extension).

### 1.3 Plug in and boot up

* Now you can eject your SD card from your laptop.
* Before powering, slot the Blinkt onto the 40-pin header making sure its curved edges match those of the Pi
* Plug the SD card into your Pi
* The USB cable goes into the port labelled "usb" on the Pi Zero and then the other end goes into your laptop.

*Do not plug the cable into the power socket*

![Raspberry Pi Zero](https://pbs.twimg.com/media/C3e_27aWQAELXDd.jpg)


The activity LED will start flashing showing the Pi is booting - this could take up to 90s for the initial boot.

You will be able to connect to the Pi with SSH through the hostname `raspberrypi.local`

* Username: pi
* Password: raspberry

```
$ ssh pi@raspberrypi.local
```

*If you're on Windows use Git bash to get access to the `ssh` command.*

You won't have any internet access yet, so we will need to enable internet connection sharing on your laptop.

> If you are working behind a restrictive or corporate network you will need to consult the [proxy guide](https://github.com/alexellis/docker-blinkt-workshop/blob/master/PROXIES.md). Skip section 1.4.

> Pro tip: if you don't like typing passwords in type in `ssh-keygen` (accepting defaults) followed by `ssh-copy-id pi@raspberrypi.local`

### 1.4 Enable Internet Connection Sharing (ICS)

On a Mac open the "Preferences" App then click "Sharing" followed by  "Share the connection" from "WiFi" to "RNDIS/Ethernet Gadget".

![](http://blog.alexellis.io/content/images/2016/12/Screen-Shot-2016-12-20-at-8-48-43-PM.png)

Restart the Raspberry Pi by typing in `sudo reboot` and try to connect again with `ssh` after about 30-60 seconds. You will find the IP address changes to something like `192.168.2.2` but the `raspberrypi.local` address will still work.

If you're on Windows then open Control Panel and look for Network Connections and Internet Connection Sharing.

> On Ubuntu Linux Internet Connection Sharing can be enabled through Network Manager, but if you can't enable sharing for whatever reason then installing a Squid Proxy server should enable you to get connected.

If you've configured ICS correctly then you should be able to type in `ping -c 1 google.com` and get a response back.

Depending on the output you may want to manually edit `/etc/resolv.conf` and enter in `nameserver 8.8.8.8` on a new line. This file can be overwritten automatically, so if that starts happening make it read-only with this command: `sudo chattr +i /etc/resolv.conf`.

### 1.5 Install Docker

From your SSH session type in `curl -sSL https://get.docker.com | sudo -E sh`, this will setup Docker on your Pi.

![Docker installation](http://blog.alexellis.io/content/images/2016/12/Screen-Shot-2016-12-20-at-8-51-25-PM.png)

Now let the Pi user have access to the Docker daemon and reboot by typing in: 

```
$ sudo usermod -aG docker pi
$ sudo reboot
```

To check everything worked you can list the running containers (which should come back empty)

```
$ docker ps
```

**Useful commands for containers and images:**

|Command           | Description |
-------------------|---------------
| `docker images`  | show the images in our library |
| `docker search`  | find an image on the public Hub |
| `docker run -ti` | start running a container with a keyboard attached|
| `docker run -d`  | start running a container in the background (detached)|
| `docker kill`    | stop a running container |
| `docker rm -f`   | stop and remove a container |


**Useful diagnostics:**

|Command           | Description |
-------------------|---------------
| `docker stats`   | show the RAM/CPU/network I/O usage of running containers |
| `docker version` | essential for when reporting bugs, shows the Docker client/version and system architecture |
| `docker info`    | a deep diagnostics page for the Docker engine |
