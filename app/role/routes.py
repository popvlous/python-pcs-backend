import datetime

from flask import render_template, request

from app import db
from app.base.models import User, Orders, SysMenu
from flask_login import login_required, current_user
from app.menu.routes import getmenus
from app.role import blueprint
from app.model.roles import Role, RolesMenus, RolesUsers


@blueprint.route('/rolelist')
@login_required
def rolelist():
    menus, menus1, menus_id = getmenus(24)
    roles = Role.query.filter().all()
    return render_template('/roles/list.html', menu_id=int(menus_id), segment='rolelist', menus=menus, menus1=menus1,
                           roles=roles)


@blueprint.route('/roleadd', methods=['GET', 'POST'])
@login_required
def roleadd():
    message = None
    menus, menus1, menus_id = getmenus(29)
    roles = Role.query.filter().all()
    if request.method == "POST":  # 如果是以POST的方式才處理
        role_name = None
        role_status = 1
        if 'role_name' in request.form:
            role_name = request.form['role_name']
        role_info = Role(role_name, role_status)
        db.session.add(role_info)
        db.session.commit()
        roles = Role.query.filter().all()
        return render_template('/roles/list.html', menu_id=int(menus_id), segment='rolelist', menus=menus,
                               menus1=menus1,
                               roles=roles)
    else:
        message = '請輸入資料(資料不作驗證)'
    return render_template('/roles/add.html', menu_id=int(menus_id), segment='roleadd', menus=menus, menus1=menus1)


@blueprint.route('/roleedit', methods=['GET', 'POST'])
@login_required
def roleedit():
    message = None
    menus, menus1, menus_id = getmenus(7)
    m_id = request.args.get('mid')
    role = Role.query.filter(Role.id == int(m_id)).first()
    if request.method == "POST":
        try:
            role_name = None
            if 'role_name' in request.form:
                role_name = request.form['role_name']
            role.role_name = role_name
            db.session.commit()
            #更新對應的roleuser角色role訊息
            roleusers = RolesUsers.query.filter(RolesUsers.role_id == int(role.id)).all()
            #若剩下一組roleuser角色，則切換成一般用戶
            for roleuser in roleusers:
                roleuser.role = role
                db.session.commit()
            #移除rolemenu的關係
            rolemenus = RolesMenus.query.filter(RolesMenus.role_id == int(role.id)).all()
            for rolemenu in rolemenus:
                rolemenu.role = role
                db.session.commit()
        except:
            message = "讀取錯誤!"
    return render_template('/roles/edit.html', menu_id=int(menus_id), segment='rolelist', menus=menus, menus1=menus1,
                           role=role, message=message)



@blueprint.route('/roledelete', methods=['GET', 'POST'])
@login_required
def roledelete():
    message = None
    menus, menus1, menus_id = getmenus(7)
    roles = Role.query.filter().all()
    m_id = request.args.get('mid')
    if int(m_id) == 1 or int(m_id) == 2:
        message = "基本角色不予許刪除!"
        return render_template('/roles/list.html', menu_id=int(menus_id), segment='rolelist', menus=menus,
                               menus1=menus1,
                               roles=roles, message=message)
    if m_id != None:
        try:
            role = Role.query.filter(Role.id == int(m_id)).first()  # 取得id欄位的資料
            #刪除對應的roleuser角色
            roleusers = RolesUsers.query.filter(RolesUsers.role_id == int(role.id)).all()
            roleinfo = Role.query.filter(Role.id == 2).first()
            #若剩下一組roleuser角色，則切換成一般用戶
            for roleuser in roleusers:
                #該USER下面有多少role
                roleusers_counts = RolesUsers.query.filter(RolesUsers.user_id == int(roleuser.user_id)).all()
                if len(roleusers_counts) == 1:
                    roleuser.role_id = 2
                    roleuser.role = roleinfo
                    db.session.commit()
                elif len(roleusers_counts) >= 2:
                    RolesUsers.query.filter(RolesUsers.user_id == int(roleuser.user_id), RolesUsers.role_id == int(roleuser.role_id)).delete()
                    db.session.commit()
            #移除rolemenu的關係
            rolemenus = RolesMenus.query.filter(RolesMenus.role_id == int(role.id)).all()
            for rolemenu in rolemenus:
                RolesMenus.query.filter(RolesMenus.role_id == int(rolemenu.role_id), RolesMenus.menu_id == int(rolemenu.menu_id)).delete()
                db.session.commit()
            Role.query.filter(Role.id == int(m_id)).delete()
            db.session.commit()
            message = "已刪除!"
        except:
            message = "讀取錯誤!"
        roles = Role.query.filter().all()
    return render_template('/roles/list.html', menu_id=int(menus_id), segment='rolelist', menus=menus, menus1=menus1,
                           roles=roles, message=message)

@blueprint.route('/authorizelist')
@login_required
def authorizelist():
    menus, menus1, menus_id = getmenus(26)
    authorizes = RolesMenus.query.filter().all()
    return render_template('/roles/authorizelist.html', menu_id=int(menus_id), segment='authorizelist', menus=menus,
                           menus1=menus1, authorizes=authorizes)


@blueprint.route('/authorizeadd', methods=['GET', 'POST'])
@login_required
def authorizeadd():
    menus, menus1, menus_id = getmenus(26)
    authorizes = RolesMenus.query.filter().all()
    menuinfos = SysMenu.query.filter().all()
    roles = Role.query.filter().all()
    if request.method == "POST":  # 如果是以POST的方式才處理
        menu_id = None
        role_id = None
        if 'menu' in request.form:
            menu_id = request.form['menu']
        if 'role' in request.form:
            role_id = request.form['role']
        roleuserinfo = RolesMenus.query.filter_by(menu_id=menu_id, role_id=role_id).all()
        if not roleuserinfo:
            roleuser = RolesMenus(menu_id, role_id)
            db.session.add(roleuser)
            db.session.commit()
            message = '已添加'
        else:
            message = '已存在對應授權'
        return render_template('/roles/authorizeadd.html', menu_id=int(menus_id), segment='authorizeadd', menus=menus,
                               menus1=menus1, menuinfos=menuinfos,
                               roles=roles, message=message)
    else:
        message = ''
    return render_template('/roles/authorizeadd.html', menu_id=int(menus_id), segment='authorizeadd', menus=menus,
                           menus1=menus1, authorizes=authorizes, menuinfos=menuinfos, roles=roles, message=message)


@blueprint.route('/authorizeedit', methods=['GET', 'POST'])
@login_required
def authorizeedit():
    menus, menus1, menus_id = getmenus(10)
    m_id = request.args.get('mid')
    rolemenuinfo = RolesMenus.query.filter(RolesMenus.id == int(m_id)).first()
    menuinfos = SysMenu.query.filter().all()
    roles = Role.query.filter().all()
    if request.method == "POST":  # 如果是以POST的方式才處理
        menu_id = None
        role_id = None
        if 'menu' in request.form:
            menu_id = request.form['menu']
        if 'role' in request.form:
            role_id = request.form['role']
        rolemenu_check = RolesMenus.query.filter(RolesMenus.menu_id == int(menu_id),
                                                   RolesMenus.role_id == int(role_id)).all()
        if not rolemenu_check:
            rolemenuinfo.menu_id = int(menu_id)
            rolemenuinfo.role_id = int(role_id)
            db.session.commit()
            message = '已添加'
        else:
            message = '已存在對應授權'
        return render_template('/roles/authorizeedit.html', menu_id=int(menus_id), segment='authorizeadd', menus=menus,
                               menus1=menus1,
                               roles=roles, rolemenuinfo=rolemenuinfo, menuinfos=menuinfos, message=message)
    else:
        message = ''
    return render_template('/roles/authorizeedit.html', menu_id=int(menus_id), segment='authorizeadd', menus=menus,
                           menus1=menus1, rolemenuinfo=rolemenuinfo, menuinfos=menuinfos, roles=roles, message=message)

@blueprint.route('/authorizedelete', methods=['GET', 'POST'])
@login_required
def authorizedelete():
    menus, menus1, menus_id = getmenus(12)
    authorizes = RolesMenus.query.filter().all()
    rolemenu_id = request.args.get('mid')
    if rolemenu_id != None:
        try:
            RolesMenus.query.filter(RolesMenus.id == int(rolemenu_id)).delete()  # 取得id欄位的資料
            db.session.commit()
            authorizes = RolesMenus.query.filter().all()
            message = "已刪除!"
        except:
            message = "讀取錯誤!"
    return render_template('/roles/authorizelist.html', menu_id=int(menus_id), segment='authorizelist', menus=menus,
                               menus1=menus1, authorizes=authorizes, message=message)


@blueprint.route('/roleuserlist')
@login_required
def roleuserlist():
    menus, menus1, menus_id = getmenus(26)
    roleusers = RolesUsers.query.join(User, RolesUsers.user_id == User.id).all()

    return render_template('/roles/roleuserlist.html', menu_id=int(menus_id), segment='roleuserlist', menus=menus,
                           menus1=menus1, roleusers=roleusers)

@blueprint.route('/roleuseradd', methods=['GET', 'POST'])
@login_required
def roleuseradd():
    menus, menus1, menus_id = getmenus(36)
    roleusers = RolesUsers.query.all()
    users = User.query.filter().all()
    roles = Role.query.filter().all()
    if request.method == "POST":  # 如果是以POST的方式才處理
        user_id = None
        role_id = None
        if 'user' in request.form:
            user_id = request.form['user']
        if 'role' in request.form:
            role_id = request.form['role']
        roleuserinfo = RolesUsers.query.filter(RolesUsers.user_id == int(user_id),
                                               RolesUsers.role_id == int(role_id)).all()
        if not roleuserinfo:
            role_user = RolesUsers(user_id=user_id, role_id=role_id)
            db.session.add(role_user)
            db.session.commit()
            message = '已添加'
        else:
            message = '已存在對應授權'
        return render_template('/roles/roleuseradd.html', menu_id=int(menus_id), segment='roleuseradd', menus=menus,
                               menus1=menus1,
                               roles=roles, users=users, message=message)
    else:
        message = ''
    return render_template('/roles/roleuseradd.html', menu_id=int(menus_id), segment='roleuseradd', menus=menus,
                           menus1=menus1, roleusers=roleusers, users=users, roles=roles, message=message)


@blueprint.route('/roleuseredit', methods=['GET', 'POST'])
@login_required
def roleuseredit():
    menus, menus1, menus_id = getmenus(26)
    m_id = request.args.get('mid')
    roleusers = RolesUsers.query.filter(RolesUsers.id == int(m_id)).first()
    users = User.query.filter().all()
    roles = Role.query.filter().all()
    if request.method == "POST":  # 如果是以POST的方式才處理
        user_id = None
        role_id = None
        if 'user' in request.form:
            user_id = request.form['user']
        if 'role' in request.form:
            role_id = request.form['role']
        roleuserinfo_check = RolesUsers.query.filter(RolesUsers.user_id == int(user_id),
                                               RolesUsers.role_id == int(role_id)).all()
        if not roleuserinfo_check:
            roleuserinfo = RolesUsers.query.filter(RolesUsers.id == int(m_id)).first()
            roleuserinfo.user_id = int(user_id)
            roleuserinfo.role_id = int(role_id)
            db.session.commit()
            message = '已添加'
        else:
            message = '已存在對應授權'
        return render_template('/roles/roleuseredit.html', menu_id=int(menus_id), segment='authorizeadd', menus=menus,
                               menus1=menus1,
                               roles=roles, roleuserinfo=roleuserinfo, users=users, message=message)
    else:
        message = ''
    return render_template('/roles/roleuseredit.html', menu_id=int(menus_id), segment='authorizeadd', menus=menus,
                           menus1=menus1, roleuserinfo=roleusers, users=users, roles=roles, message=message)


@blueprint.route('/roleuserdelete', methods=['GET', 'POST'])
@login_required
def roleuserdelete():
    menus, menus1, menus_id = getmenus(26)
    roleusers = RolesUsers.query.filter().all()
    roleuser_id = request.args.get('mid')
    if roleuser_id != None:
        try:
            RolesUsers.query.filter(RolesUsers.id == int(roleuser_id)).delete()  # 取得id欄位的資料
            db.session.commit()
            roleusers = RolesUsers.query.filter().all()
        except:
            message = "讀取錯誤!"
    return render_template('/roles/roleuserlist.html', menu_id=int(menus_id), segment='roleuserlist', menus=menus,
                           menus1=menus1, roleusers=roleusers)
