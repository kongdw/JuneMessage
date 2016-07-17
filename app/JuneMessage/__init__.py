import os

from flask import Flask
from flask_mongoengine import MongoEngine
from flask_login import LoginManager
from flask_principal import Principal
from flask_mail import Mail
from flask_oauthlib.provider import OAuth2Provider

from config import config

db = MongoEngine()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'accounts.login'

principals = Principal()

mail = Mail()

oauth = OAuth2Provider()

def create_app(config_name):
    app = Flask(__name__, 
        template_folder=config[config_name].TEMPLATE_PATH, static_folder=config[config_name].STATIC_PATH)
    app.config.from_object(config[config_name])

    config[config_name].init_app(app)

    db.init_app(app)
    login_manager.init_app(app)
    principals.init_app(app)
    mail.init_app(app)
    oauth.init_app(app)

    from main.urls import main as main_blueprint
    from accounts.views import accounts as accounts_blueprint
    from oauth2.urls import oauth as oauth_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(accounts_blueprint, url_prefix='/accounts')
    app.register_blueprint(oauth_blueprint, url_prefix='/oauth')

    return app

app = create_app(os.getenv('config') or 'default')