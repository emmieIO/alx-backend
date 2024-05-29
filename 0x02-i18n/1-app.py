#!/usr/bin/env python3
"""0-app.py server creation"""
from flask import Flask, render_template
from flask_babel import Babel
from config import Config


app = Flask(__name__)
app.config.from_object(Config)


babel = Babel(app)


@app.route("/")
def index():
    """This route renders a Hello Word"""
    return render_template('1-index.html')
