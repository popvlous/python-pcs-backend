# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from flask_mail import Mail
from flask_migrate import Migrate
from os import environ
from sys import exit
from decouple import config
import logging

from flask_moment import Moment

from config import config_dict
from app import create_app, db

# WARNING: Don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

# The configuration
get_config_mode = 'Debug' if DEBUG else 'Production'

try:
    
    # Load the configuration using the default values 
    app_config = config_dict[get_config_mode.capitalize()]

except KeyError:
    exit('Error: Invalid <config_mode>. Expected values [Debug, Production] ')

app = create_app( app_config )
moment = Moment(app)
#mail = Mail(app)
Migrate(app, db)

if DEBUG:
    app.logger.info('DEBUG       = ' + str(DEBUG)      )
    app.logger.info('Environment = ' + get_config_mode )
    app.logger.info('DBMS        = ' + app_config.SQLALCHEMY_DATABASE_URI )


#.ENV檔案中設定測試環境DEBUG=True , 正式環境DEBUG=False
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
