from flask import Flask, Response, request, render_template
import pyaudio

app = Flask(__name__, static_url_path='')

@app.route('/')
def index():
    return render_template('public/index.html')

@app.route('/api/list/devices', methods=['GET'])
def list_devices():
    p = pyaudio.PyAudio()
    devices = []
    for i in range(p.get_device_count()):
        device = p.get_device_info_by_index(i)
        devices.append(device)
    return {"devices": devices}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port='8080')