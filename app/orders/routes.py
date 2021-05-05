import json

from flask import render_template, request
from app.base.models import User, Orders, SysMenu
from flask_login import login_required, current_user

from app.base.util import queryBlockChainOrder, historyBlockChainOrder
from app.menu.routes import getmenus
from app.orders import blueprint


@blueprint.route('/orderlist')
@login_required
def orderlist():
    menus, menus1, menus_id = getmenus(12)
    orders = Orders.query.filter().all()
    # 確認區塊鏈是否存在
    # for order in orders:
    #     check_info = queryBlockChainOrder(order.order_id)
    #     if len(check_info) == 0:
    #         order.checkinfo = False
    #     else:
    #         order.checkinfo = True
    return render_template('/orders/list.html', menu_id=int(menus_id), segment='orderlist', menus=menus, menus1=menus1,
                           orders=orders)


@blueprint.route('/ordercheck')
@login_required
def ordercheck():
    menus, menus1, menus_id = getmenus(12)
    orders = Orders.query.filter().all()
    check_info_json = None
    historylists = []
    message = None
    order_id = request.args.get('mid')
    check_info = queryBlockChainOrder(order_id)
    history_infos = historyBlockChainOrder(order_id)
    if len(check_info) == 0:
        message = "data is not exist"
    else:
        check_info_json = json.loads(check_info.decode("utf-8").replace("'", '"'))
        check_info_json['isblockchain'] = True
    if len(history_infos) == 0:
        message = "data is not exist"
    else:
        historylists = json.loads(history_infos.decode("utf-8").replace("'", '"'))
    return render_template('/orders/check.html', menu_id=int(menus_id), segment='orderlist', menus=menus, menus1=menus1,
                           historylists=historylists, checkinfo=check_info_json, message=message)
