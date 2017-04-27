## Working with proxies

If you're on a restrictive network then it may be necessary to make use of a proxy for all of the Docker commands in the workshop.

Certain WiFi networks will prevent you from enabling Internet Connection Sharing, this guide will also help work-around that restriction.

### 1.0 Set up a proxy server on your laptop

Run the following Docker image:

```
$ docker run --name proxy -p 3128:3128 -d alexellis2/squid:latest
```

You can pick up the Dockerfile and rebuild from source from Github: [alexellis2/images/squid](https://github.com/alexellis/images/tree/master/squid).

**Test connectivity**

To test the connectivity run `curl -v -x http://address_of_laptop:3218 https://www.google.com`

**Configure the Pi**

Now on the Raspberry Pi edit ~/.bash_profile and add these two lines:

```
export http_proxy=http://address_of_laptop:3128
export https_proxy=http://address_of_laptop:3218
```

Also run them on the shell or log out and in again.

### 1.1 `docker pull`

To pull images from the Docker Hub you will need to update the systemd unit file on the Raspberry Pi with the IP address or name of your PC or Mac.

Make the following folder:

```
# sudo mkdir -p /etc/systemd/system/docker.service.d/
```

Now create the following file `/etc/systemd/system/docker.service.d/http-proxy.conf`:

```
[Service]
Environment="HTTP_PROXY=http://address_of_laptop:3128"
Environment="HTTPS_PROXY=http://address_of_laptop:3128"
```

Restart the Pi with `sudo reboot`.

### 1.2 `docker build`

For the time being the best way to use a proxy with `docker build` is to pass environmental variables temporarily through `--build-arg`:

```
docker build --build-arg http_proxy=$http_proxy --build-arg https_proxy=$https_proxy -t myimage .
```
