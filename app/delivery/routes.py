from flask import render_template
from app.base.models import User, Orders, SysMenu
from flask_login import login_required, current_user
from app.menu.routes import getmenus
from app.delivery import blueprint
from app.model.delivery import Delivery


@blueprint.route('/deliverylist')
@login_required
def deliverylist():
    menus, menus1, menus_id = getmenus(34)
    deliveries = Delivery.query.filter().all()
    return render_template('/deliveries/list.html', menu_id=int(menus_id), segment='deliverylist', menus=menus, menus1=menus1, deliveries=deliveries)