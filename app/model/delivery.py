# coding:utf-8
from flask_login import UserMixin

from app import db
from datetime import datetime


class Delivery(db.Model, UserMixin):
    __tablename__ = 'delivery'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    create_time = db.Column(db.DateTime, index=True, default=datetime.now)
    modify_time = db.Column(db.DateTime, index=True, default=datetime.now)
    create_by = db.Column(db.String(100))
    order_source = db.Column(db.String(100))
    location = db.Column(db.String(100))
    shipping_first_name = db.Column(db.String(50), nullable=True)
    shipping_last_name = db.Column(db.String(50), nullable=True)
    shipping_company = db.Column(db.String(50), nullable=True)
    shipping_address_1 = db.Column(db.String(500), nullable=True)
    shipping_address_2 = db.Column(db.String(500), nullable=True)
    shipping_city = db.Column(db.String(50), nullable=True)
    shipping_postcode = db.Column(db.String(50), nullable=True)
    shipping_country = db.Column(db.String(50), nullable=True)
    shipping_phone = db.Column(db.String(50), nullable=True)
    shipment_number = db.Column(db.String(50), nullable=True)
    remark = db.Column(db.String(50))

    def __init__(self, user_id, create_by, order_source, shipping_first_name, shipping_last_name, shipping_company,
                 shipping_address_1, shipping_address_2, shipping_city, shipping_postcode, shipping_country,
                 shipping_phone):
        self.user_id = user_id
        self.create_by = create_by
        self.order_source = order_source
        self.create_time = datetime.utcnow()
        self.modify_time = datetime.utcnow()
        self.shipping_first_name = shipping_first_name
        self.shipping_last_name = shipping_last_name
        self.shipping_company = shipping_company
        self.shipping_address_1 = shipping_address_1
        self.shipping_address_2 = shipping_address_2
        self.shipping_city = shipping_city
        self.shipping_postcode = shipping_postcode
        self.shipping_country = shipping_country
        self.shipping_phone = shipping_phone
