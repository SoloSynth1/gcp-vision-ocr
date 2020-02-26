import json

from flask import Flask, Request

app = Flask(__name__)


@app.route('/process')
def process_image():
    req = json.load(Request
    return "Hello World!"


if __name__ == '__main__':
    app.run(port=8080)
