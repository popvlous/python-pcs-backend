# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask import jsonify, render_template, redirect, request, url_for
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user
)

from app import db, login_manager
from app.base import blueprint
from app.base.forms import LoginForm, CreateAccountForm
from app.base.models import User, Orders, SysMenu

from app.base.util import verify_pass, hash_pass
from app.menu.routes import getmenus_no_id, getmenus


@blueprint.route('/')
def route_default():
    return redirect(url_for('base_blueprint.login'))

# def getmenus(Path=None):
#     menus = SysMenu.query.filter().all()
#     menus1 = SysMenu.query.filter().all()
#     menus2 = SysMenu.query.filter_by(MenuUrl=Path).first()
#     menus_id = menus2.ParentId
#     return menus, menus1, menus_id

## Login & Registration

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    #menus, menus1 = getmenus()
    menus = SysMenu.query.filter().all()
    menus1 = SysMenu.query.filter().all()
    url = menus1[0].MenuUrl
    if 'login' in request.form:
        
        # read form data
        username = request.form['username']
        password = request.form['password']

        # Locate user
        user = User.query.filter_by(username=username).first()
        order = Orders.query.filter_by(order_id=1702).first()

        
        # Check the password
        if user and verify_pass( password, user.password):

            login_user(user)
            return redirect(url_for('base_blueprint.route_default'))

        # Something (user or pass) is not ok
        return render_template( 'accounts/login.html', msg='Wrong user or password', form=login_form)

    if not current_user.is_authenticated:
        return render_template( 'accounts/login.html',
                                form=login_form)
    return redirect(url_for('home_blueprint.index', menus=menus, menus1=menus1))

@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    login_form = LoginForm(request.form)
    create_account_form = CreateAccountForm(request.form)
    if 'register' in request.form:

        username  = request.form['username']
        email     = request.form['email'   ]

        # Check usename exists
        user = User.query.filter_by(username=username).first()
        if user:
            return render_template( 'accounts/register.html', 
                                    msg='Username already registered',
                                    success=False,
                                    form=create_account_form)

        # Check email exists
        user = User.query.filter_by(email=email).first()
        if user:
            return render_template( 'accounts/register.html', 
                                    msg='Email already registered', 
                                    success=False,
                                    form=create_account_form)

        # else we can create the user
        user = User(**request.form)
        db.session.add(user)
        db.session.commit()

        return render_template( 'accounts/register.html', 
                                msg='User created please <a href="/login">login</a>', 
                                success=True,
                                form=create_account_form)

    else:
        return render_template( 'accounts/register.html', form=create_account_form)

@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('base_blueprint.login'))

@blueprint.route('/list')
def list():
    menus, menus1, menus_id = getmenus(8)
    users = User.query.filter().all()
    return render_template( 'accounts/list.html', users=users, menu_id=int(menus_id), segment='list', menus=menus, menus1=menus1)

@blueprint.route('/add',methods=['GET', 'POST'])
def add():
    menus, menus1, menus_id = getmenus(10)
    users = User.query.filter().all()
    if request.method == "POST":
        username = None
        email = None
        password = None
        if 'username' in request.form:
            username = request.form['username']
        if 'email' in request.form:
            email = request.form['email']
        if 'password' in request.form:
            password = request.form['password']
        user = User(**request.form)
        db.session.add(user)
        db.session.commit()
        newusers = User.query.filter().all()
        return render_template('accounts/list.html', users=newusers, segment='list', menus=menus, menus1=menus1)
    return render_template( 'accounts/add1.html', users=users, menu_id=int(menus_id), segment='list', menus=menus, menus1=menus1)

@blueprint.route('/edit',methods=['GET', 'POST'])
def edit():
    menus, menus1 = getmenus_no_id()
    users = User.query.filter().all()
    user_id = request.args.get('mid')
    userinfo = User.query.filter_by(id=user_id).first()
    if request.method == "POST": # 如果是以POST的方式才處理
        username = None
        email = None
        if 'username' in request.form:
            username = request.form['username']
        if 'email' in request.form:
            email = request.form['email']
        User.query.filter_by(id=user_id).update(dict(username=username, email=email))
        db.session.commit()
        newusers = User.query.filter().all()
        return render_template('accounts/list.html', users=newusers, segment='list', menus=menus, menus1=menus1,
                               user=userinfo)
    return render_template( 'accounts/edit.html', users=users, segment='edit', menus=menus, menus1=menus1, user=userinfo)

@blueprint.route('/delete',methods=['GET', 'POST'])
def delete():
    message = None
    menus, menus1 = getmenus_no_id()
    users = User.query.filter().all()
    user_id = request.args.get('mid')
    if user_id!=None:
        try:
            User.query.filter_by(id=user_id).delete()  #取得id欄位的資料
            db.session.commit()
        except:
            message = "讀取錯誤!"
    return render_template( 'accounts/list.html', segment='list', menus=menus, menus1=menus1, users=users)

## Errors

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('page-403.html'), 403

@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('page-403.html'), 403

@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('page-404.html'), 404

@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('page-500.html'), 500
