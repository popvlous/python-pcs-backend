# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from app.home import blueprint
from flask import render_template, redirect, url_for, request
from flask_login import login_required, current_user
from app import login_manager
from jinja2 import TemplateNotFound
from app.base.models import User, Orders, SysMenu
from app.menu.routes import getmenus


@blueprint.route('/index')
@login_required
def index():
    #menus = SysMenu.query.filter().all()
    #menus1 = SysMenu.query.filter().all()
    menus, menus1, menus_id = getmenus(12)
    orders = Orders.query.filter().all()
    return render_template('/orders/list.html', menu_id=int(menus_id), segment='orderlist', menus=menus, menus1=menus1, orders=orders)

@blueprint.route('/<template>')
@login_required
def route_template(template):
    menus = SysMenu.query.filter().all()
    menus1 = SysMenu.query.filter().all()
    try:

        if not template.endswith( '.html' ):
            template += '.html'

        # Detect the current page
        segment = get_segment( request )

        # Serve the file (if exists) from app/templates/FILE.html
        return render_template( template, segment=segment , menus=menus, menus1=menus1)

    except TemplateNotFound:
        return render_template('page-404.html'), 404
    
    except:
        return render_template('page-500.html'), 500

# Helper - Extract current page name from request 
def get_segment( request ): 

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment    

    except:
        return None  
