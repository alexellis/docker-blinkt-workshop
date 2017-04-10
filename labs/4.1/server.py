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
