from flask import render_template, request

from app import db
from app.base.models import User, Orders, SysMenu
from flask_login import login_required, current_user

from app.base.util import getCustomerNameById
from app.menu.routes import getmenus
from app.model.inventory import Inventory
from app.inventory import blueprint
from app.model.roles import Role, RolesMenus, RolesUsers


@blueprint.route('/inventorylist')
@login_required
def inventorylist():
    user_id = None
    menus, menus1, menus_id = getmenus(31)
    inventories = Inventory.query.filter().all()
    for invertory in inventories:
        order_info = Orders.query.filter_by(customer_id=invertory.user_id).limit(1).all()
        if order_info:
            invertory.username = order_info[0].billing_last_name + order_info[0].billing_first_name
        else:
            invertory.username = 'N/A'
        #invertory.username = order_info[0].billing_last_name + order_info[0].billing_first_name
    return render_template('/inventories/list.html', menu_id=int(menus_id), segment='inventorylist', menus=menus,
                           menus1=menus1,
                           inventories=inventories)
