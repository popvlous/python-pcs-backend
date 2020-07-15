from flask import Blueprint

blueprint = Blueprint(
    'inventory',
    __name__,
    url_prefix='/backend',
    template_folder='templates',
    static_folder='static'
)