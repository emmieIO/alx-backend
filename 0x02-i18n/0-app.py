#!/usr/bin/env python3
"""0-app.py server creation"""
from flask import Flask
from flask import render_template


app = Flask(__name__)


@app.route("/")
def index():
    """This route renders a Hello Word"""
    return render_template('0-index.html')
