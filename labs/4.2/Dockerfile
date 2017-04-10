FROM blinkt
RUN apt-get update -qy && \
    apt-get install -qy python-pip && \
    pip install flask

WORKDIR /root/
COPY server.py .
EXPOSE 5000

CMD ["python", "./server.py"]
