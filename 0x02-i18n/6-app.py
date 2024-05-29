#!/usr/bin/env python3
"""5-app.py"""
from flask import Flask, render_template, request, g
from flask_babel import Babel


app = Flask(__name__)
babel = Babel(app)


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


class Config:
    """Configuration class for Flask app."""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app.config.from_object(Config)


@babel.localeselector
def get_locale():
    """Determine the best match for the supported languages."""
    locale = request.args.get('locale', None)
    if locale in app.config['LANGUAGES']:
        return locale

    user = get_user()
    if user and user['locale'] in app.config['LANGUAGES']:
        return user['locale']

    headers = request.headers.get('Accept-Language', None)
    if headers:
        languages = [lang.split(';')[0] for lang in headers.split(',')]
        for language in languages:
            if language in app.config['LANGUAGES']:
                return language

    return app.config['BABEL_DEFAULT_LOCALE']


def get_user():
    """Get the user dictionary or None if not found."""
    user_id = request.args.get('login_as', None)
    if user_id and int(user_id) in users:
        return users[int(user_id)]
    return None


@app.before_request
def before_request():
    """Set the user as a global on flask.g.user."""
    g.user = get_user()


@app.route('/', strict_slashes=False)
def index():
    """Render the 5-index.html template."""
    return render_template('5-index.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
