#!/usr/bin/env python3
"""2-app.py"""
from flask import Flask, render_template, request
from flask_babel import Babel


class Config(object):
    """Configuration class for Flask app.
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


# configure the flask app
app = Flask(__name__)
app.config.from_object(Config)
app.url_map.strict_slashes = False
babel = Babel(app)


@babel.localeselector
def get_locale():
    """Get_local class """
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/', strict_slashes=False)
def index():
    """his route renders a Hello Word
    """
    return render_template('2-index.html')


if __name__ == '__main__':
    app.run(port="5000", host="0.0.0.0", debug=True)
