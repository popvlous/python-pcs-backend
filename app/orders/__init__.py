# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask import Blueprint

blueprint = Blueprint(
    'orders',
    __name__,
    url_prefix='/backend',
    template_folder='templates',
    static_folder='static'
)