''' This file initializes the website package and the Flask Web app '''
import smtplib
import cloudinary
from os import path
from dotenv import load_dotenv

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_cors import CORS

from whitenoise import WhiteNoise
from urllib.parse import urljoin

APP_ROOT = path.join(path.dirname(__file__))
dotenv_path = path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)

db = SQLAlchemy()
DB_NAME = "database.db"

mail = Mail()
cors = CORS()

def create_app():
    ''' Configures the web app framework '''

    app = Flask(__name__, static_folder="staticfiles")

    from .config import Config
    app.config.from_object(Config)

    # initialize db, mail, and cors
    db.init_app(app)
    mail.init_app(app)
    cors.init_app(app)

    # configure WhiteNoise
    app.wsgi_app = WhiteNoise(
        app.wsgi_app,
        root=path.join(path.dirname(__file__), "staticfiles"),
        prefix="assets/",
        max_age=app.config["WHITENOISE_MAX_AGE"]
    )

    # configure Cloudinary
    cloudinary.config(
        cloud_name=app.config["CLOUDINARY_CLOUD_NAME"],
        api_key=app.config["CLOUDINARY_API_KEY"],
        api_secret=app.config["CLOUDINARY_API_SECRET"]
    )

    # Blueprint registration
    from .boards import boards
    from .auth import auth
    from .user_account import user_account
    from .handlers import errors

    app.register_blueprint(boards, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(user_account, url_prefix='/')
    app.register_blueprint(errors, url_prefix='/')

    # Jinja filters
    from .filters import humanize_time, get_cloud_file

    app.jinja_env.filters['humanize_time'] = humanize_time
    app.jinja_env.filters['get_cloud_file'] = get_cloud_file

    # Login views and management
    from .models import User

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    # Global jinja template functions
    @app.template_global()
    def static_url(prefix, filename):
        return urljoin(app.config["STATIC_URL"], f"{prefix}/{filename}")

    return app
