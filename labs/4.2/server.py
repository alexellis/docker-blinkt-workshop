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
