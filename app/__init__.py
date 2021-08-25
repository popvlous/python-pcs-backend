# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import logging
from logging.handlers import TimedRotatingFileHandler

from flask import Flask, url_for
from flask_login import LoginManager
#from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from importlib import import_module

from logging import basicConfig, DEBUG, getLogger, StreamHandler
from os import path


db = SQLAlchemy()
login_manager: LoginManager = LoginManager()

def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)

def register_blueprints(app):
    for module_name in ('base', 'home', 'menu', 'orders', 'role', 'inventory', 'delivery', 'ecpay'):
        module = import_module('app.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)

def configure_database(app):

    @app.before_first_request
    def initialize_database():
        db.create_all()

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()

def create_app(config):
    app = Flask(__name__, static_folder='base/static')
    app.config.from_object(config)
    register_extensions(app)
    register_blueprints(app)
    configure_database(app)
    formatter = logging.Formatter(
        "[%(asctime)s][%(module)s:%(lineno)d][%(levelname)s][%(thread)d] - %(message)s")
    handler = TimedRotatingFileHandler(
        "logs/flask.log", when="D", interval=1, backupCount=15,
        encoding="UTF-8", delay=False, utc=True)
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    return app
