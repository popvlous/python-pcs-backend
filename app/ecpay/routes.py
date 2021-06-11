import collections
import hashlib
import json
from datetime import datetime
from urllib.parse import quote_plus

import requests
from flask import render_template, request, jsonify, Response, redirect, url_for
from sqlalchemy import desc

from flask_login import login_required, current_user

from app.inventory.routes import lineNotifyMessage
from app.menu.routes import getmenus
from app.ecpay import blueprint
from app.model.delivery import Delivery
from woocommerce import API

# -*- coding: utf-8 -*-

# woocommerce api
wcapi = API(
    url="https://store.pyrarc.com",
    consumer_key="ck_ab98c184df28b6bc3298710a139177b00564a302",
    consumer_secret="cs_9de359730bb8aa8d4faf3395541c503e90997294",
    version="wc/v3"
)

user_name = "pyrarc.app"
user_passwd = "dOidZQSGR09BnHROt4ss#NT3"
end_point_url_posts = "https://store.pyrarc.com/wp-json/jwt-auth/v1/token"

payload = {
    "username": user_name,
    "password": user_passwd
}

# 付款參數

import importlib.util

spec = importlib.util.spec_from_file_location(
    "ecpay_payment_sdk",
    "app/ecpay/sdk/ecpay_payment_sdk.py"
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
from datetime import datetime


# 環境參數
class Params:
    def __init__(self):
        web_type = 'test'
        if web_type == 'offical':
            # 正式環境
            self.params = {
                'MerchantID': '隱藏',
                'HashKey': '隱藏',
                'HashIV': '隱藏',
                'action_url':
                    'https://payment.ecpay.com.tw/Cashier/AioCheckOut/V5'
            }
        else:
            # 測試環境
            self.params = {
                'MerchantID':
                    '2000132',
                'HashKey':
                    '5294y06JbISpM5x9',
                'HashIV':
                    'v77hoKGq4kWxNNIS',
                'action_url':
                    'https://payment-stage.ecpay.com.tw/Cashier/AioCheckOut/V5'
            }

    @classmethod
    def get_params(cls):
        return cls().params

    # 驗證綠界傳送的 check_mac_value 值是否正確
    @classmethod
    def get_mac_value(cls, get_request_form):

        params = dict(get_request_form)
        if params.get('CheckMacValue'):
            params.pop('CheckMacValue')

        ordered_params = collections.OrderedDict(
            sorted(params.items(), key=lambda k: k[0].lower()))

        HahKy = cls().params['HashKey']
        HashIV = cls().params['HashIV']

        encoding_lst = []
        encoding_lst.append('HashKey=%s&' % HahKy)
        encoding_lst.append(''.join([
            '{}={}&'.format(key, value)
            for key, value in ordered_params.items()
        ]))
        encoding_lst.append('HashIV=%s' % HashIV)

        safe_characters = '-_.!*()'

        encoding_str = ''.join(encoding_lst)
        encoding_str = quote_plus(str(encoding_str),
                                  safe=safe_characters).lower()

        check_mac_value = ''
        check_mac_value = hashlib.sha256(
            encoding_str.encode('utf-8')).hexdigest().upper()

        return check_mac_value


@blueprint.route('/ecpay')
def payment_info():
    # menus, menus1, menus_id = getmenus(34)
    # 獲取訂單訊息
    order_id = request.args.get('oid')
    orderid = 'orders/' + str(order_id)
    # 無jwt調用方式
    # order_details = wcapi.get(orderid).json()
    r = requests.post(end_point_url_posts, data=payload)
    jwt_info = r.content.decode("utf-8").replace("'", '"')
    data = json.loads(jwt_info)
    my_headers = {'Authorization': "Bearer " + data['token']}
    res_order_details = requests.get('https://store.pyrarc.com/wp-json/wc/v3/orders/' + str(order_id), data=payload,
                                     headers=my_headers)
    order_details = json.loads(res_order_details.content.decode("utf-8").replace("'", '"'))

    order_details_total = order_details['total']
    line_items = order_details['line_items']
    total_product_name = ''
    for line_item in line_items:
        if line_item:
            line_items_name = line_item['name']
            total_product_name += line_items_name + '#'
    # 取得環境參數
    params = Params.get_params()

    host_url = 'https://storeapi.pyrarc.com'

    order_params = {
        'MerchantTradeNo': str(order_id) + datetime.now().strftime("NO%Y%m%d%H%M%S"),
        'StoreID': '',
        'MerchantTradeDate': datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
        'PaymentType': 'aio',
        'TotalAmount': int(order_details_total),
        'TradeDesc': 'PyrarcTest',
        'ItemName': total_product_name,
        'ReturnURL': host_url+'/backend/ecpay/receive',
        'ChoosePayment': 'ALL',
        'ClientBackURL': 'https://store.pyrarc.com',
        'ItemURL': 'https://www.ecpay.com.tw/item_url.php',
        'Remark': '交易備註',
        'ChooseSubPayment': '',
        'OrderResultURL': host_url+'/backend/ecpay/result',
        'NeedExtraPaidInfo': 'Y',
        'DeviceSource': '',
        'IgnorePayment': '',
        'PlatformID': '',
        'InvoiceMark': 'N',
        'CustomField1': '',
        'CustomField2': '',
        'CustomField3': '',
        'CustomField4': '',
        'EncryptType': 1,
    }

    extend_params_1 = {
        'ExpireDate': 7,
        'PaymentInfoURL': 'https://www.ecpay.com.tw/payment_info_url.php',
        'ClientRedirectURL': '',
    }

    extend_params_2 = {
        'StoreExpireDate': 15,
        'Desc_1': '',
        'Desc_2': '',
        'Desc_3': '',
        'Desc_4': '',
        'PaymentInfoURL': 'https://www.ecpay.com.tw/payment_info_url.php',
        'ClientRedirectURL': '',
    }

    extend_params_3 = {
        'BindingCard': 0,
        'MerchantMemberID': '',
    }

    extend_params_4 = {
        'Redeem': 'N',
        'UnionPay': 0,
    }

    inv_params = {
        # 'RelateNumber': 'Tea0001', # 特店自訂編號
        # 'CustomerID': 'TEA_0000001', # 客戶編號
        # 'CustomerIdentifier': '53348111', # 統一編號
        # 'CustomerName': '客戶名稱',
        # 'CustomerAddr': '客戶地址',
        # 'CustomerPhone': '0912345678', # 客戶手機號碼
        # 'CustomerEmail': 'abc@ecpay.com.tw',
        # 'ClearanceMark': '2', # 通關方式
        # 'TaxType': '1', # 課稅類別
        # 'CarruerType': '', # 載具類別
        # 'CarruerNum': '', # 載具編號
        # 'Donation': '1', # 捐贈註記
        # 'LoveCode': '168001', # 捐贈碼
        # 'Print': '1',
        # 'InvoiceItemName': '測試商品1|測試商品2',
        # 'InvoiceItemCount': '2|3',
        # 'InvoiceItemWord': '個|包',
        # 'InvoiceItemPrice': '35|10',
        # 'InvoiceItemTaxType': '1|1',
        # 'InvoiceRemark': '測試商品1的說明|測試商品2的說明',
        # 'DelayDay': '0', # 延遲天數
        # 'InvType': '07', # 字軌類別
    }

    # 建立實體
    ecpay_payment_sdk = module.ECPayPaymentSdk(MerchantID=params['MerchantID'],
                                               HashKey=params['HashKey'],
                                               HashIV=params['HashIV'])

    if order_id:
        try:

            # 合併延伸參數
            order_params.update(extend_params_1)
            order_params.update(extend_params_2)
            order_params.update(extend_params_3)
            order_params.update(extend_params_4)
            # 合併發票參數
            order_params.update(inv_params)
            # 產生綠界訂單所需參數
            final_order_params = ecpay_payment_sdk.create_order(order_params)

            # 產生 html 的 form 格式
            action_url = 'https://payment-stage.ecpay.com.tw/Cashier/AioCheckOut/V5'  # 測試環境
            # action_url = 'https://payment.ecpay.com.tw/Cashier/AioCheckOut/V5' # 正式環境
            html = ecpay_payment_sdk.gen_html_post_form(action_url, final_order_params)
            print(html)
            return html
        except Exception as error:
            print('An exception happened: ' + str(error))
    return render_template('ecpay/payment.html')


@blueprint.route('/ecpay/receive', methods=['GET', 'POST'])
def payment_receive():
    result = request.form['RtnMsg']
    tid = request.form['CustomField1']
    if not result:
        return jsonify({
            'success': False
        })
    return '1|OK'


@blueprint.route('/ecpay/result', methods=['GET', 'POST'])
def payment_end():
    if request.method == 'GET':
        return render_template('ecpay/success.html')

    if request.method == 'POST':
        check_mac_value = Params.get_mac_value(request.form)

        if request.form['CheckMacValue'] != check_mac_value:
            return '請聯繫管理員'

        # 接收 ECpay 刷卡回傳資訊
        result = request.form['RtnMsg']
        tid = request.form['CustomField1']

        # # 取得交易使用者資訊
        # uid = trade_detail.uid
        #
        # trade_client_detail = {
        #     'name': trade_detail.trade_name,
        #     'phone': trade_detail.trade_phone,
        #     'county': trade_detail.trade_county,
        #     'district': trade_detail.trade_district,
        #     'zipcode': trade_detail.trade_zipcode,
        #     'trade_address': trade_detail.trade_address
        # }

        # 判斷成功
        if result == 'Succeeded':
            # trade_detail.status = '待處理'
            # commit_list = []
            #
            # # 移除 AddToCar (狀態：Y 修改成 N)
            # carts = sql.AddToCar.query.filter_by(uid=uid, state='Y')
            # for cart in carts:
            #     price = cart.product.price
            #     quan = cart.quantity
            #     cart.state = 'N'
            #     # 新增 Transaction_detail 訂單細項資料
            #     Td = sql.Transaction_detail(tid, cart.product.pid, quan, price)
            #     commit_list.append(Td)
            #     commit_list.append(cart)
            #
            # db.session.add_all(commit_list)
            # db.session.commit()
            #
            # # 讀取訂單細項資料
            # trade_detail_items = sql.Transaction_detail.query.filter_by(
            #     tid=tid)
            result = request.form['MerchantTradeNo']
            order_id = result[:4]
            r = requests.post(end_point_url_posts, data=payload)
            jwt_info = r.content.decode("utf-8").replace("'", '"')
            data = json.loads(jwt_info)
            my_headers = {'Authorization': "Bearer " + data['token']}
            # res_order_details = requests.get('https://store.pyrarc.com/wp-json/wc/v3/orders/' + str(order_id),
            #                                  data=payload,
            #                                  headers=my_headers)
            # order_details = json.loads(res_order_details.content.decode("utf-8").replace("'", '"'))

            # 修改訂單狀態
            order_payload = {
                "status": "completed"
            }
            r_order = requests.put('https://store.pyrarc.com/wp-json/wc/v3/orders/' + str(order_id), data=order_payload,
                                   headers=my_headers)
            #return render_template('ecpay/success.html')
            return redirect(url_for('ecpay.payment_success', result='success'))

        # 判斷失敗
        else:

            return render_template('ecpay/fail.html')

@blueprint.route('/ecpay/result', methods=['GET', 'POST'])
def payment_success():
    return render_template('ecpay/success.html')