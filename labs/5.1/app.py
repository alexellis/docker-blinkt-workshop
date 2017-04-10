
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
