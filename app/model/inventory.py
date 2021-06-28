# coding:utf-8
from flask_login import UserMixin
from sqlalchemy.orm import relationship, backref

from app import db
from datetime import datetime


# 角色资源关联表
# role_resource_table = db.Table('SYROLE_SYRESOURCE', db.metadata,
#                               db.Column('SYROLE_ID', db.String, db.ForeignKey('SYROLE.ID')),
#                               db.Column('SYRESOURCE_ID', db.String, db.ForeignKey('SYRESOURCE.ID')))

class Inventory(db.Model, UserMixin):
    __tablename__ = 'inventory'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    beging_inventory = db.Column(db.Integer)
    ending_inventory = db.Column(db.Integer)
    adj_amount = db.Column(db.String(50))
    create_time = db.Column(db.DateTime, index=True, default=datetime.now)
    modify_time = db.Column(db.DateTime, index=True, default=datetime.now)
    transaction_id = db.Column(db.String(100))
    order_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)
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
    tx_id = db.Column(db.String(200), nullable=True)

    def __init__(self, user_id, beging_inventory, ending_inventory, adj_amount, order_id, product_id, create_by,
                 order_source):
        self.user_id = user_id
        self.beging_inventory = beging_inventory
        self.ending_inventory = ending_inventory
        self.adj_amount = adj_amount
        self.order_id = order_id
        self.product_id = product_id
        self.create_by = create_by
        self.order_source = order_source
        self.create_time = datetime.utcnow()
        self.modify_time = datetime.utcnow()


class InventoryMeta(db.Model, UserMixin):
    __tablename__ = 'inventorymeta'
    id = db.Column(db.Integer, primary_key=True)
    inventory_id = db.Column(db.Integer)
    purchase_type = db.Column(db.Integer)
    vaild_time = db.Column(db.DateTime, index=True, default=datetime.now)
    remark = db.Column(db.String(50))

    def __init__(self, role_name, role_status):
        self.role_name = role_name
        self.role_status = role_status
        self.base_create_time = datetime.utcnow()
        self.base_modify_time = datetime.utcnow()
