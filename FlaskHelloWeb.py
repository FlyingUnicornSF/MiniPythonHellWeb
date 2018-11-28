''' $ export FLASK_APP=FlaskHelloWeb.py
    $ flask run'''
from flask import Flask, url_for, request, render_template
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def root():
    return render_template('index.html')
