from flask import Flask
from flask import render_template
import random, threading, webbrowser
import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, request, redirect, url_for, send_from_directory

app = Flask(__name__, static_url_path='')
static_folder_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")

@app.route('/static/<path:filename>')
def serve_static(filename):
    """
    Would serve all the static files.

    """
    app.logger.warning('URL is '+filename)
    root_dir = os.path.dirname(os.getcwd())
    app.logger.warning('Input to send_from_directory - ' + str(os.path.join(root_dir, 'WordFreq','static')))
    return send_from_directory(os.path.join(root_dir, 'WordFreq','static'), filename)


@app.route('/')
def hello_world():
    return render_template('d3WordCount.html')


if __name__ == '__main__':
    port = 8888
    handler = RotatingFileHandler('foo.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run(port=port)
    webbrowser.open('http://localhost:'+port)
