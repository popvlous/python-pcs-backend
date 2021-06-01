from datetime import datetime

from flask import render_template, request
from sqlalchemy import desc

from app import db
from app.base.models import User, Orders, SysMenu
from flask_login import login_required, current_user

from app.inventory.routes import lineNotifyMessage
from app.menu.routes import getmenus
from app.delivery import blueprint
from app.model.delivery import Delivery


@blueprint.route('/deliverylist')
@login_required
def deliverylist():
    menus, menus1, menus_id = getmenus(34)
    delivery_id = request.args.get('mid')
    if delivery_id:
        deliveries = Delivery.query.filter_by(id=delivery_id).order_by(desc(Delivery.id)).all()
    else:
        deliveries = Delivery.query.filter().order_by(desc(Delivery.id)).all()
    now = datetime.utcnow()
    return render_template('/deliveries/list.html', menu_id=int(menus_id), segment='deliverylist', menus=menus, menus1=menus1, deliveries=deliveries, now=now)

@blueprint.route('/deliveryadddo', methods=['GET', 'POST'])
@login_required
def deliveryadddo():
    message = None
    menus, menus1, menus_id = getmenus(34)
    deliveries = Delivery.query.filter().all()
    delivery_id = request.args.get('mid')
    delivery = Delivery.query.filter_by(id=delivery_id).one()
    if request.method == "POST":  # 如果是以POST的方式才處理
        shipment_number = None
        if 'shipment_number' in request.form:
            shipment_number = request.form['shipment_number']
        (shipment_number)
        delivery.shipment_number = shipment_number
        db.session.commit()
        return render_template('/deliveries/list.html', menu_id=int(menus_id), segment='deliverylist', menus=menus,
                               menus1=menus1,
                               deliveries=deliveries)
    else:
        message = '請輸入物流單號'
    return render_template('/deliveries/adddo.html', menu_id=int(menus_id), segment='', menus=menus, menus1=menus1,
                           delivery=delivery)


@blueprint.route('/deliverynotify', methods=['GET', 'POST'])
@login_required
def deliverynotify():
    message = None
    menus, menus1, menus_id = getmenus(31)
    delivery_id = request.args.get('mid')
    deliverires = Delivery.query.filter().all()
    token = 'M5g5yVHMV2gc6iRvs1xu5Bsb9OEj0Wux8pQcKknldMo'
    msg = '請登入平台，輸入物流單號 https://storeapi.pyrarc.com/backend/deliverylist?mid=' + str(delivery_id)
    lineNotifyMessage(token, msg)
    return render_template('/deliveries/list.html', menu_id=int(menus_id), segment='deliverylist', menus=menus,
                           menus1=menus1,
                           deliverires=deliverires)