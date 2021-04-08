# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_login import UserMixin
from sqlalchemy import LargeBinary, Column, Integer, String
from sqlalchemy.orm import relationship, backref

from app import db, login_manager
from app.base.util import hash_pass
from datetime import datetime

class User(db.Model, UserMixin):

    __tablename__ = 'User'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(LargeBinary)
    BaseCreateTime = Column(db.DateTime, nullable=True)
    BaseCreatorId = Column(db.Integer, nullable=True)
    BaseModifyTime = Column(db.DateTime, nullable=True)
    BaseVersion = Column(db.Integer, nullable=True)
    Salt = Column(db.String(255), nullable=True)
    RealName = Column(db.String(255), nullable=True)
    DepartmentId = Column(db.Integer, nullable=True)
    Gender = Column(db.Integer, nullable=True)
    Birthday = db.Column(db.String(255), nullable=True)
    Portrait = db.Column(db.String(255), nullable=True)
    Mobile = db.Column(db.String(255), nullable=True)
    LoginCount = Column(db.Integer, nullable=True)
    UserStatus = Column(db.Integer, nullable=True)
    IsSystem = Column(db.Integer, nullable=True)
    IsOnline = Column(db.Integer, nullable=True)
    Remark = Column(db.String(255), nullable=True)
    WebToken = Column(db.String(255), nullable=True)
    ApiToken = Column(db.String(255), nullable=True)
    roleusers = relationship('RolesUsers', backref=backref('RolesUsers', order_by=id))

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            if property == 'password':
                value = hash_pass( value ) # we need bytes here (not plain str)
                
            setattr(self, property, value)

    def __repr__(self):
        return str(self.username)

@login_manager.user_loader
def user_loader(id):
    return User.query.filter_by(id=id).first()

@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = User.query.filter_by(username=username).first()
    return user if user else None

class Orders(db.Model):
    __table__name = 'Orders'
    # 設定 primary_key
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer)
    parent_id = db.Column(db.Integer)
    state = db.Column(db.String(50), nullable=True)
    billing_first_name = db.Column(db.String(50), nullable=True)
    billing_last_name = db.Column(db.String(50), nullable=True)
    date_created = db.Column(db.DateTime, nullable=True)
    total = db.Column(db.Integer, nullable=True)
    billing_state = db.Column(db.String(50), nullable=True)
    billing_city = db.Column(db.String(50), nullable=True)
    billing_address_1 = db.Column(db.String(500), nullable=True )

    def __init__(self, order_id, parent_id, state, billing_first_name, billing_last_name):
        self.order_id = order_id
        self.parent_id = parent_id
        self.state = state
        self.billing_first_name = billing_first_name
        self.billing_last_name = billing_last_name

class SysMenu(db.Model):
    __table__name = 'sys_menu'
    # 設定 primary_key
    id = Column(db.Integer, primary_key=True)
    BaseIsDelete = Column(db.Integer, nullable=True)
    BaseCreateTime = Column(db.DateTime, nullable=True)
    BaseCreatorId = Column(db.Integer, nullable=True)
    BaseModifyTime = Column(db.DateTime, nullable=True)
    BaseModifierId = Column(db.Integer, nullable=True)
    BaseVersion = Column(db.Integer, nullable=True)
    MenuName = Column(db.String(50), nullable=True)
    ParentId = Column(db.Integer)
    MenuIcon = Column(db.String(50), nullable=True)
    MenuUrl = Column(db.String(100), nullable=True)
    MenuTarget = Column(db.String(50), nullable=True)
    MenuSort = Column(db.Integer, nullable=True)
    MenuType = Column(db.Integer, nullable=True)
    MenuStatus = Column(db.Integer, nullable=True)
    Authorize = Column(db.String(50), nullable=True)
    Remark = Column(db.String(50), nullable=True)

    def __init__(self, MenuName, ParentId, MenuUrl, MenuSort, MenuType, MenuTarget):
        self.BaseIsDelete = 0
        self.BaseCreateTime = datetime.utcnow()
        self.BaseModifyTime = datetime.utcnow()
        self.MenuName = MenuName
        self.ParentId = ParentId
        self.MenuUrl = MenuUrl
        self.MenuSort = MenuSort
        self.MenuType = MenuType
        self.MenuTarget = MenuTarget
