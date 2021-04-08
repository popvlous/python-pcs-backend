# coding:utf-8
from flask_login import UserMixin
from sqlalchemy.orm import relationship, backref

from app import db
from datetime import datetime

#角色资源关联表
#role_resource_table = db.Table('SYROLE_SYRESOURCE', db.metadata,
#                               db.Column('SYROLE_ID', db.String, db.ForeignKey('SYROLE.ID')),
#                               db.Column('SYRESOURCE_ID', db.String, db.ForeignKey('SYRESOURCE.ID')))

class Role(db.Model, UserMixin):
    __tablename__ = 'sys_role'
    id = db.Column(db.Integer, primary_key=True)
    base_create_time = db.Column(db.DateTime, index=True, default=datetime.now)
    base_modify_time = db.Column(db.DateTime, index=True, default=datetime.now)
    base_create_id = db.Column(db.Integer)
    role_name = db.Column(db.String(50))
    role_status = db.Column(db.Integer)
    remark = db.Column(db.String(50))

    def __init__(self, role_name, role_status):
        self.role_name = role_name
        self.role_status = role_status
        self.base_create_time = datetime.utcnow()
        self.base_modify_time = datetime.utcnow()

class RolesMenus(db.Model, UserMixin):
    __tablename__ = 'sys_roles_menus'
    id = db.Column(db.Integer, primary_key=True)
    base_create_time = db.Column(db.DateTime, index=True, default=datetime.now)
    base_modify_time = db.Column(db.DateTime, index=True, default=datetime.now)
    base_create_id = db.Column(db.Integer)
    menu_id = db.Column(db.Integer, db.ForeignKey('sys_menu.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('sys_role.id'))
    role_type = db.Column(db.Integer)
    remark = db.Column(db.String(50))
    role = relationship('Role', backref=backref('sys_role', order_by=id))
    menu = relationship('SysMenu', backref=backref('sys_menu', order_by=id))

    def __init__(self, menu_id, role_id):
        self.menu_id = menu_id
        self.role_id = role_id
        self.base_create_time = datetime.utcnow()
        self.base_modify_time = datetime.utcnow()

class RolesUsers(db.Model, UserMixin):
    __tablename__ = 'sys_roles_users'
    id = db.Column(db.Integer, primary_key=True)
    base_create_time = db.Column(db.DateTime, index=True, default=datetime.now)
    base_modify_time = db.Column(db.DateTime, index=True, default=datetime.now)
    base_create_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('sys_role.id'))
    role_type = db.Column(db.Integer)
    remark = db.Column(db.String(50))
    role = relationship('Role', backref=backref('Role', order_by=id))
    user = relationship('User', backref=backref('User', order_by=id))

    def __init__(self, user_id, role_id):
        self.user_id = user_id
        self.role_id = role_id
        self.base_create_time = datetime.utcnow()
        self.base_modify_time = datetime.utcnow()