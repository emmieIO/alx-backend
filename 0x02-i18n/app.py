#!/usr/bin/env python3
"""5-app.py"""
from flask import Flask, render_template, request, g
from flask_babel import Babel, gettext as _
import pytz
from pytz.exceptions import UnknownTimeZoneError
from datetime import datetime


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


@babel.timezoneselector
def get_timezone():
    """Determine the best match for the supported timezones."""
    timezone = request.args.get('timezone', None)
    if timezone:
        try:
            return pytz.timezone(timezone).zone
        except UnknownTimeZoneError:
            pass

    user = get_user()
    if user:
        user_timezone = user.get('timezone', None)
        if user_timezone:
            try:
                return pytz.timezone(user_timezone).zone
            except UnknownTimeZoneError:
                pass

    return app.config['BABEL_DEFAULT_TIMEZONE']


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
    # Get the current time based on the inferred timezone
    current_time = datetime.now(pytz.timezone(get_timezone()))
    formatted_time = current_time.strftime('%c')
    # Translate the message
    time_msg = _("current_time_is", current_time=formatted_time)
    return render_template('index.html', current_time_message=time_msg)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
