from flask import Blueprint

blueprint = Blueprint(
    'delivery',
    __name__,
    url_prefix='/backend',
    template_folder='templates',
    static_folder='static'
)