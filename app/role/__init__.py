from flask import Blueprint

blueprint = Blueprint(
    'roles',
    __name__,
    url_prefix='/backend',
    template_folder='templates',
    static_folder='static',
    static_url_path='/backend'
)