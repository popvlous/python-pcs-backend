# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os
import pymysql
pymysql.install_as_MySQLdb()
from decouple import config

class Config(object):

    basedir    = os.path.abspath(os.path.dirname(__file__))

    # Set up the App SECRET_KEY
    SECRET_KEY = config('SECRET_KEY', default='S#perS3crEt_007')

    # This will create a file in <app> FOLDER
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')
    SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}?autocommit=true'.format(
        config( 'DB_ENGINE'   , default='mysql'    ),
        config( 'DB_USERNAME' , default='pcs'       ),
        config( 'DB_PASS'     , default='Foxconn@890'          ),
        config( 'DB_HOST'     , default='192.168.100.14'     ),
        config( 'DB_PORT'     , default=3309            ),
        config( 'DB_NAME'     , default='pcs' )
    )

    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
    }

    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    DEBUG = False

    # Security
    SESSION_COOKIE_HTTPONLY  = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = 3600

    # PostgreSQL database
    SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}?autocommit=true'.format(
        config( 'DB_ENGINE'   , default='mysql'    ),
        config( 'DB_USERNAME' , default='pyrarcdev'       ),
        config( 'DB_PASS'     , default='dev2021api0322'          ),
        config( 'DB_HOST'     , default='192.168.110.18'     ),
        config( 'DB_PORT'     , default=3306            ),
        config( 'DB_NAME'     , default='pcs' )
    )

    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
    }

class DebugConfig(Config):
    DEBUG = True

# Load all possible configurations
config_dict = {
    'Production': ProductionConfig,
    'Debug'     : DebugConfig
}
