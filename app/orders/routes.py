from flask import render_template
from app.base.models import User, Orders, SysMenu
from app.menu.routes import getmenus
from app.orders import blueprint


@blueprint.route('/orderlist')
def orderlist():
    menus, menus1, menus_id = getmenus(12)
    orders = Orders.query.filter().all()
    return render_template('/orders/list.html', menu_id=int(menus_id), segment='orderlist', menus=menus, menus1=menus1, orders=orders)

