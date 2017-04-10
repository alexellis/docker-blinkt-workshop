FROM blinkt
RUN apt-get update -qy && \
    apt-get install -qy python-pip && \
    pip install requests

WORKDIR /root/
COPY app.py .
EXPOSE 5000
ENV HOST_URL http://raspberrypi.local:5000
ENV no_proxy raspberrypi.local
CMD ["python", "./app.py"]
