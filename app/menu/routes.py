from flask import Flask, render_template, request
from app.menu import blueprint
from app.base.models import User, Orders, SysMenu
from app import db


def getparentid(ParentId=None, Path=None):
    menus = SysMenu.query.filter().all()
    menus1 = SysMenu.query.filter().all()
    menus2 = SysMenu.query.filter(ParentId=ParentId, MenuUrl=Path).first()
    menus_id = menus2.ParentId
    return menus, menus1, menus_id


def getmenus(menu_id=None):
    menus = SysMenu.query.filter().order_by(SysMenu.MenuSort.asc())
    menus1 = SysMenu.query.filter().order_by(SysMenu.MenuSort.asc())
    menus2 = SysMenu.query.filter_by(id=menu_id).first()
    menus_id = menus2.ParentId
    return menus, menus1, menus_id

def getmenus_no_id():
    menus = SysMenu.query.filter().order_by(SysMenu.MenuSort.asc())
    menus1 = SysMenu.query.filter().order_by(SysMenu.MenuSort.asc())
    return menus, menus1


@blueprint.route('/menuindex')
def menuindex():
    menus = SysMenu.query.filter().all()
    menus1 = SysMenu.query.filter().all()
    return render_template('index2.html', segment='index.html', menus=menus, menus1=menus1)


@blueprint.route('/menulist')
def menulist():
    menus, menus1, menus_id = getmenus(2)
    return render_template('list.html', menu_id=int(menus_id), segment='menulist', menus=menus, menus1=menus1)


@blueprint.route('/menuadd', methods=['GET', 'POST'])
def menuadd():
    message = None
    menus, menus1, menus_id = getmenus(3)
    menutops = SysMenu.query.filter_by(MenuType=1).all()
    if request.method == "POST" and int(request.form['menu_type']) != 0:  # 如果是以POST的方式才處理
        menu_type = None
        menu_name = None
        menu_url = None
        menu_sort = None
        menu_target = None
        menu_bp =None
        parent_id = None
        if 'menu_type' in request.form:
            menu_type = request.form['menu_type']
        if 'menu_name' in request.form:
            menu_name = request.form['menu_name']
        if 'menu_url' in request.form:
            menu_url = request.form['menu_url']
        if 'menu_sort' in request.form:
            menu_sort = request.form['menu_sort']
        if 'menu_bp' in request.form:
            menu_bp = request.form['menu_bp']

        if (int(menu_type) == 1):
            parent_id = 0
            menu_target = menu_bp
            menu_url = '#'
        elif (int(menu_type) == 2):
            menu_top = request.form['menu_top']
            parent_menu = SysMenu.query.filter_by(id=menu_top).first()
            menu_target = parent_menu.MenuTarget
            parent_id = parent_menu.id
        menus_info = SysMenu(menu_name, parent_id, menu_url, int(menu_sort), int(menu_type), menu_target)
        db.session.add(menus_info)
        db.session.commit()
    else:
        message = '請輸入資料(資料不作驗證)'
    return render_template('add1.html', menu_id=int(menus_id), segment='menuadd', menus=menus, menus1=menus1,
                           menutops=menutops)
@blueprint.route('/menuedit', methods=['GET', 'POST'])
def menuedit():
    message = None
    menus, menus1 = getmenus_no_id()
    menu_id = request.args.get('mid')
    menu_info = SysMenu.query.filter_by(id=menu_id).first()
    menu_parent_id = menu_info.ParentId
    menutops = SysMenu.query.filter_by(MenuType=1).all()
    if request.method == "POST" and int(request.form['menu_type']) != 0:  # 如果是以POST的方式才處理
        menu_type = None
        menu_name = request.form['menu_name']
        menu_url = request.form['menu_url']
        menu_sort = request.form['menu_sort']
        menu_target = None
        parent_id = None
        if 'menu_type' in request.form:
            menu_type = request.form['menu_type']
        if 'menu_name' in request.form:
            menu_name = request.form['menu_name']
        if 'menu_url' in request.form:
            menu_url = request.form['menu_url']
        if 'menu_sort' in request.form:
            menu_sort = request.form['menu_sort']

        if (int(menu_type) == 1):
            parent_id = 0
            menu_url = '#'
        elif (int(menu_type) == 2):
            menu_top = request.form['menu_top']
            parent_menu = SysMenu.query.filter_by(id=menu_top).first()
            menu_target = parent_menu.MenuTarget
            parent_id = parent_menu.id
        menus_info = SysMenu(menu_name, parent_id, menu_url, int(menu_sort), int(menu_type), menu_target)
        db.session.add(menus_info)
        db.session.commit()
    else:
        message = '請輸入資料(資料不作驗證)'
    return render_template('edit.html', menu_id=int(menu_parent_id), segment='menuedit', menus=menus, menus1=menus1,
                           menuinfo=menu_info, menutops=menutops)

@blueprint.route('/menudel', methods=['GET', 'POST'])
def menudel():
    message = None
    menus, menus1 = getmenus_no_id()
    menu_id = request.args.get('mid')
    if menu_id!=None:
        try:
            SysMenu.query.filter_by(id=menu_id).delete()  #取得id欄位的資料
            db.session.commit()
        except:
            message = "讀取錯誤!"
    return render_template('list.html', segment='menulist', menus=menus, menus1=menus1)