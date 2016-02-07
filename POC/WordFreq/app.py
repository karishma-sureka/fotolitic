from flask import Flask
from flask import render_template
import random, threading, webbrowser

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('wordFreq.html')


if __name__ == '__main__':
    port = 8888
    app.run(port=port)
    webbrowser.open('http://localhost:'+port)
