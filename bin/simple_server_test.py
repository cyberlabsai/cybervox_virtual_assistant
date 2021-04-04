from flask import Flask, Response, request

app = Flask(__name__)

@app.route('/<data>', methods=['GET'])
def server(data):
    print('From virtual assistant', data)
    return {}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port='8080')