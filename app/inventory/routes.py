import requests
from flask import render_template, request

from app import db
from app.base.models import User, Orders, SysMenu
from flask_login import login_required, current_user

from app.base.util import getCustomerNameById
from app.menu.routes import getmenus
from app.model.inventory import Inventory
from app.inventory import blueprint
from app.model.roles import Role, RolesMenus, RolesUsers


def lineNotifyMessage(token, msg):
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    payload = {'message': msg}
    r = requests.post("https://notify-api.line.me/api/notify", headers=headers, params=payload)
    return r.status_code


@blueprint.route('/inventorylist')
@login_required
def inventorylist():
    user_id = None
    menus, menus1, menus_id = getmenus(31)
    inventory_id = request.args.get('mid')
    if inventory_id:
        inventories = Inventory.query.filter_by(id=inventory_id).all()
    else:
        inventories = Inventory.query.filter().all()
    for invertory in inventories:
        order_info = Orders.query.filter_by(customer_id=invertory.user_id).limit(1).all()
        if order_info:
            invertory.username = order_info[0].billing_last_name + order_info[0].billing_first_name
        else:
            invertory.username = 'N/A'
        # invertory.username = order_info[0].billing_last_name + order_info[0].billing_first_name
    return render_template('/inventories/list.html', menu_id=int(menus_id), segment='inventorylist', menus=menus,
                           menus1=menus1,
                           inventories=inventories)


@blueprint.route('/inventoryadddo', methods=['GET', 'POST'])
@login_required
def inventoryadddo():
    message = None
    menus, menus1, menus_id = getmenus(31)
    inventories = Inventory.query.filter().all()
    inventory_id = request.args.get('mid')
    inventory = Inventory.query.filter_by(id=inventory_id).one()
    if request.method == "POST":  # 如果是以POST的方式才處理
        shipment_number = None
        if 'shipment_number' in request.form:
            shipment_number = request.form['shipment_number']
        (shipment_number)
        inventory.shipment_number = shipment_number
        db.session.commit()
        return render_template('/inventories/list.html', menu_id=int(menus_id), segment='inventorylist', menus=menus,
                               menus1=menus1,
                               inventories=inventories)
    else:
        message = '請輸入物流單號'
    return render_template('/inventories/adddo.html', menu_id=int(menus_id), segment='', menus=menus, menus1=menus1,
                           inventory=inventory)


@blueprint.route('/inventorynotify', methods=['GET', 'POST'])
@login_required
def inventorynotify():
    message = None
    menus, menus1, menus_id = getmenus(31)
    inventory_id = request.args.get('mid')
    inventory = Inventory.query.filter_by(id=inventory_id).all()
    inventories = Inventory.query.filter().all()
    token = 'M5g5yVHMV2gc6iRvs1xu5Bsb9OEj0Wux8pQcKknldMo'
    msg = '請登入平台，輸入物流單號 https://storeapi.pyrarc.com/backend/inventorylist?mid=' + str(inventory_id)
    lineNotifyMessage(token, msg)
    return render_template('/inventories/list.html', menu_id=int(menus_id), segment='inventorylist', menus=menus,
                           menus1=menus1,
                           inventories=inventories)
