import json

from flask import render_template,request,session
from ..models import *
from . import main
from .. import db
from ..forms import *
from flask_login import login_user,login_required,logout_user
from sqlalchemy import or_
from functools import wraps
import time

#访问首页
@main.route('/')
def index_views():
    # 以下是单点餐品
    # 10以上餐品
    menus_01=Optionalfood.query.filter(Optionalfood.cprice<10,Optionalfood.type=='单点餐品').all()
    # 10-20元餐品
    menus_02=Optionalfood.query.filter(Optionalfood.cprice>10,Optionalfood.cprice<20,Optionalfood.type=='单点餐品').all()
    # # 20-50元餐品
    menus_03=Optionalfood.query.filter(Optionalfood.cprice>20,Optionalfood.cprice<50,Optionalfood.type=='单点餐品').all()
    # # 50元以上餐品
    menus_04=Optionalfood.query.filter(Optionalfood.cprice>=50,Optionalfood.type=='单点餐品').all()
    return render_template('index.html',params=locals())

#订单查询
@main.route('/orderquery')
@login_required
def DDancx_views():
    return render_template('orderquery.html')

#收到客户端菜品种类的请求,返回对应表以及对应菜品的信息
@main.route('/type_menus')
def table_type():
    type=request.args['type']
    if not type:
        print('未收到请求信息')
    table_list=[Optionalfood,Fixedpackage]
    for table in table_list:
        resList = db.session.query(table.type).group_by(table.type).all()
        for res in resList:
            if res[0]==type:
                menus=table.query.filter(table.type==type).all()
                list=[]
                for menu in menus:
                    list.append(menu.to_dict())
                return json.dumps(list)

#点餐车post请求数据提交至此
@main.route('/dingcan_post',methods=['POST'])
def diangcan_post_views():
    #将前端传来的json字符串转换成字典
    data=json.loads(request.get_data().decode('utf-8'))
    userOrder=data['userOrder']
    for order in userOrder:
        if order['mealmeans']=='自选订餐':
            cname=order['cname']
            stock=db.session.query(Optionalfood.stock).filter_by(cname=cname).first()[0]
            if stock>=float(order['number']):
                return json.dumps('OK')

#点餐提交成功
@main.route('/dingcan_startorder')
def startorder_views():
    return render_template('startorder.html')


@main.route('/test')
def test_views():

    return render_template('test.html',params=locals())




@main.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    user = User.query.filter_by(username=form.username.data).first()
    if user is not None and user.verify_password(form.password.data):
        #登录成功后存入session中
        session['user_id'] = user.id
        print('kangzi1')
        login_user(user,form.remember_me.data)
        flash('%s,登录成功' % user)
        time.sleep(0.1)
        return redirect(url_for('main.index_views'))
    return render_template('login.html',form=form)


@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('你已经退出登录')
    return redirect(url_for('main.index_views'))

@main.route('/register',methods=['GET','POST'])
def Register():
    form=RegistForm()
    print(form.validate_on_submit())
    if form.validate_on_submit():
        password = form.password_hash.data
        user = User(username=form.username.data,
                    name=form.name.data,
                    phone=form.phone.data,
                    email=form.email.data)
        user.password(password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('main.login'))
    return render_template('register.html',form=form)


#会员中心
@main.route('/query')
@login_required
def query_views():
    user_id = session.get('user_id')
    user = User.query.filter(User.id==user_id).first()
    return render_template('vip_center.html',user=user)

#修改信息
@main.route('/update',methods=['GET','POST'])
@login_required
def update_view():
    user_id = session.get('user_id')
    if request.method == 'GET':
        user = User.query.filter(User.id == user_id).first()
        return render_template('toChangeInformation.html',user=user)
    else:
        user = User.query.filter(User.id == user_id).first()

        uname = request.form['name']
        uphone = request.form['phone']
        opwd = request.form['ouserpwd']
        npwd = request.form['nuserpwd']
        uemail = request.form['email']

        if user.verify_password(opwd):
            # return u'密码着呢改期'
            user1 = User.query.filter(User.email == uemail).first()
            # 找到了
            if user1:
                if user1.id != user_id:
                    return u'邮箱已被使用，请重新输入！'
                else:
                    user2 = User.query.filter(User.phone == uphone).first()
                    if user2:
                            if user2.id != user_id:
                                return u'手机被使用，请重新输入！'
                            else:
                                user.name = uname
                                user.phone = uphone
                                user.email = uemail
                                # user.password_hash = user.password(npwd)
                                user.password(npwd)
                                db.session.add(user)
                                db.session.commit()
                                return redirect('/query')
            else:
                user2 = User.query.filter(User.phone == uphone).first()
                if user2:
                    if user2.id == user_id:
                        user.name = uname
                        user.phone = uphone
                        user.email = uemail
                        # user.password_hash = user.password(npwd)
                        user.password(npwd)
                        db.session.add(user)
                        db.session.commit()
                        return redirect('/query')

                    else:
                        return u'手机已被使用，请重新输入！'

                else:
                    user.name = uname
                    user.phone = uphone
                    user.email = uemail
                    # user.password_hash = user.password(npwd)
                    user.password(npwd)
                    db.session.add(user)
                    db.session.commit()
                    return redirect('/query')
        else:
            return u'原始密码不正确，请重新输入!'





        #判断输入的手机及邮箱是否已被使用
        #如果已经被使用且使用者是当前登录用户的话就通过
        #信息查找到的user
        # user1 = User.query.filter(User.email == uemail).first()
        # if user1:
        #     if user1.id != user_id:
        #         return u'邮箱已被使用，请重新输入！'
        #     else:
        #         user2 = User.query.filter(User.phone == uphone).first()
        #         if user2:
        #             if user2.id != user_id:
        #                 return u'手机已被使用，请重新输入！'
        #             else:
        #         user.name = uname
        #         user.phone = uphone
        #         user.email = uemail
        #         user.password_hash = npwd
        #         db.session.add(user)
        #         db.session.commit()
        #         return redirect('/query')
        # else:
        #     user.name = uname
        #     user.phone = uphone
        #     user.email = uemail
        #     user.password_hash = nupassword
        #     db.session.add(user)
        #     db.session.commit()
        #     return redirect('/query')
        #
        # user2 = User.query.filter(User.phone == uphone).first()
        # if user2:
        #     if user2.id != user_id:
        #         return u'该手机已被使用，请重新输入！'
        #     else:
        #         user.name = uname
        #         user.phone = uphone
        #         user.email = uemail
        #         user.password_hash = nupassword
        #         db.session.add(user)
        #         db.session.commit()
        #         return redirect('/query')
        # else:
        #     user.name = uname
        #     user.phone = uphone
        #     user.email = uemail
        #     user.password_hash = nupassword
        #     db.session.add(user)
        #     db.session.commit()
        #     return redirect('/query')
        #
        # else:
        # # def verify_password(self, password):
        # #     # 定义比较密码的方法：传入用户输入的密码，返回bool值
        # #     return check_password_hash(self.password_hash, password)
        #     if user and user.verify_password(opwd):
        #         user.name = uname
        #         user.phone = uphone
        #         user.email = uemail
        #         user.password_hash = nupassword
        #         db.session.add(user)
        #         return redirect('/query')
        #     else:
        #         return u'原始密码不正确，请重新输入!'

#切换头部导航栏状态
@main.context_processor
def my_context_processor():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            return {'user':user}
    return {}

