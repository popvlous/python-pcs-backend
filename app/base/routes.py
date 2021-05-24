# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask import jsonify, render_template, redirect, request, url_for, flash
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user
)

from app import db, login_manager
from app.base import blueprint
from app.base.forms import LoginForm, CreateAccountForm
from app.base.models import User, Orders, SysMenu, request_loader
from app.model.roles import RolesMenus, Role, RolesUsers
from app.base.sendmail import send_mail

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

#登入後重導向 帶入下一個頁面跟參數
def redirect_dest(fallback):
    dest = request.args.get('next')
    dest_args = request.args.get('mid')
    try:
        dest_url = url_for(dest, mid=dest_args)
    except:
        return redirect(fallback)
    return redirect(dest_url)


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    #menus = SysMenu.query.filter().all()
    #menus1 = SysMenu.query.filter().all()
    #url = menus1[0].menu.MenuUrl
    if 'login' in request.form:
        
        # read form data
        username = request.form['username']
        password = request.form['password']

        # Locate user
        user = User.query.filter_by(username=username).first()

        
        # Check the password
        if user and verify_pass( password, user.password):

            login_user(user)
            return redirect_dest(fallback=url_for('base_blueprint.route_default'))
            #return url_for(url_for('base_blueprint.route_default'))


        # Something (user or pass) is not ok
        return render_template( 'accounts/login.html', msg='Wrong user or password', form=login_form)

    if not current_user.is_authenticated:
        return render_template( 'accounts/login.html',
                                form=login_form)
    if current_user.is_active:
        menus, menus1, menus_id = getmenus(3)
    else:
        menus, menus1, = getmenus_no_id()
    return redirect(url_for('home_blueprint.index', menus=menus, menus1=menus1))




@blueprint.route('/register', methods=['GET', 'POST'])
def register():

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
        user.confirm = 0
        db.session.add(user)
        db.session.commit()

        #增加user跟角色的關係,預設一般用戶為6
        role_info = RolesUsers(user.id, 6)
        db.session.add(role_info)
        db.session.commit()

        #新增帳號啟動信
        token = user.create_confirm_token()
        re_token = token.decode("utf-8").replace("'", '"')
        User.query.filter_by(id=user.id).update(dict(WebToken=token))
        db.session.commit()
        recipients_mail = []
        recipients_mail.append(email)
        send_mail(sender='popvlous007@gmail.com',
                  recipients=recipients_mail,
                  subject='Activate your account',
                  template='accounts/mail/welcome',
                  mailtype='html',
                  user=user,
                  token=re_token)

        return render_template( 'accounts/register.html', 
                                msg='User created please <a href="/backend/login">login</a>',
                                success=True,
                                form=create_account_form)

    else:
        return render_template( 'accounts/register.html', form=create_account_form)

@blueprint.route('/user_confirm/<token>')
def user_confirm(token):
    login_form = LoginForm(request.form)
    if not token:
        return render_template( 'accounts/login.html', msg='token無效', form=login_form)
    user = User.query.filter_by(WebToken=token).first()
    if not user:
        return render_template('accounts/login.html', form=login_form, msg='user無效')
    data = user.validate_confirm_token(token)
    if data:
        user = User.query.filter_by(id=data.get('user_id')).first()
        user.confirm = True
        db.session.add(user)
        db.session.commit()
        flash("激活成功 請重新登入")
        return redirect(url_for('base_blueprint.login'))
    else:
        return redirect(url_for('base_blueprint.login', msg='已失效 請重新註冊'))

@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('base_blueprint.login'))

@blueprint.route('/list')
@login_required
def list():
    menus, menus1, menus_id = getmenus(8)
    users = User.query.filter().all()
    return render_template( 'accounts/list.html', users=users, menu_id=int(menus_id), segment='list', menus=menus, menus1=menus1)

@blueprint.route('/add',methods=['GET', 'POST'])
@login_required
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
    return render_template( 'accounts/add1.html', users=users, menu_id=int(menus_id), segment='add', menus=menus, menus1=menus1)

@blueprint.route('/edit',methods=['GET', 'POST'])
@login_required
def edit():
    menus, menus1, menus_id = getmenus(10)
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
@login_required
def delete():
    message = None
    menus, menus1, menus_id = getmenus(8)
    users = User.query.filter().all()
    user_id = request.args.get('mid')
    if user_id!=None:
        try:
            User.query.filter_by(id=user_id).delete()  #取得id欄位的資料
            db.session.commit()
        except:
            message = "讀取錯誤!"
    usersinfo = User.query.filter().all()
    return render_template( 'accounts/list.html', segment='list', menus=menus, menus1=menus1, users=usersinfo)


@blueprint.before_request
def before_request():
    """
    在使用者登入之後，需做一個帳號是否啟動的驗證，啟動之後才能向下展開相關的應用。
    條件一：需登入
    條件二：未啟動
    條件三：endpoint不等於static，這是避免靜態資源的取用異常，如icon、js、css等..
    :return:
    """
    if (current_user.is_authenticated and
            not current_user.confirm and
            request.endpoint != 'static'):
        #  條件滿足就引導至未啟動說明
        msg = '請激活該帳號'
        login_form = LoginForm(request.form)
        return render_template('accounts/login.html', form=login_form, msg=msg)


## Errors

#尚未登入連結網誌錯誤，
@login_manager.unauthorized_handler
def unauthorized_handler():
    flash("You have to be logged in to access this page.")
    next = url_for(request.endpoint, **request.args)
    #return redirect(url_for('base_blueprint.login', next=next))
    return redirect(url_for('base_blueprint.login', next=request.endpoint, **request.args))
    #return render_template('page-403.html'), 403

@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('page-403.html'), 403

@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('page-404.html'), 404

@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('page-500.html'), 500
