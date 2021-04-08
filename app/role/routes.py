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


@blueprint.route('/authorizelist')
@login_required
def authorizelist():
    menus, menus1, menus_id = getmenus(26)
    authorizes = RolesMenus.query.filter().all()
    return render_template('/roles/authorizelist.html', menu_id=int(menus_id), segment='authorizelist', menus=menus,
                           menus1=menus1, authorizes=authorizes)

@blueprint.route('/roleuserlist')
@login_required
def roleuserlist():
    menus, menus1, menus_id = getmenus(26)
    roleusers = RolesUsers.query.join(User, RolesUsers.user_id == User.id).all()
    return render_template('/roles/roleuserlist.html', menu_id=int(menus_id), segment='roleuserlist', menus=menus,
                           menus1=menus1, roleusers=roleusers)


@blueprint.route('/roleadd', methods=['GET', 'POST'])
@login_required
def roleadd():
    message = None
    menus, menus1, menus_id = getmenus(25)
    roles = Role.query.filter().all()
    if request.method == "POST":  # 如果是以POST的方式才處理
        role_name = None
        role_status = 1
        if 'role_name' in request.form:
            role_name = request.form['role_name']
        role_info = Role(role_name, role_status)
        db.session.add(role_info)
        db.session.commit()
        return render_template('/roles/list.html', menu_id=int(menus_id), segment='rolelist', menus=menus,
                               menus1=menus1,
                               roles=roles)
    else:
        message = '請輸入資料(資料不作驗證)'
    return render_template('/roles/add.html', menu_id=int(menus_id), segment='roleadd', menus=menus, menus1=menus1)
