from flask import Flask,render_template,request,session,redirect,url_for
from sqlalchemy import or_
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:123456@localhost:3306/Restaurant'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)

#创建实体类
class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer,primary_key=True)
    #用户名／昵称
    username = db.Column(db.String(20),unique=True,index=True)
    #手机号
    phone = db.Column(db.String(20),unique=True,index=True)
    #邮箱地址
    email = db.Column(db.String(254),unique=True,index=True)
    #密码
    password_hash = db.Column(db.String(128))#这里传入的是加密后的密码
    #真实姓名
    name = db.Column(db.String(30))

db.create_all()

# 初始化
@app.route('/')
def func():
    # print(db)
    # return "程序访问成功！"
    return render_template('index.html')

#创建用户
@app.route('/adduser')
def add_user():
    user = Users()
    user.username = 's1790090265'
    user.phone = '13631665057'
    user.email = '790090265@qq.com'
    user.password_hash = 'qq785632587'
    user.name = "张三"
    db.session.add(user)
    return "创建用户成功"

#查询会员信息
@app.route('/query')
def query_views():
    #从session中获取用户名保存在selected_user中
    #selected_user = session['user']
    # phone = '13631665057'
    username = 's1790090265'
    user = Users.query.filter(Users.username==username).first()
    return render_template('vip_center.html',user=user)

#修改会员信息
@app.route('/update',methods=['GET','POST'])
def update_view():
    #从登录状态中获得用户名
    # selected_user = session['uname']
    username = 's1790090265'
    if request.method == 'GET':
        user = Users.query.filter(Users.username == username).first()
        return render_template('toChangeInformation.html',user=user)
    else:
        uname = request.form['name']
        uphone = request.form['phone']
        opassword = request.form['ouserpwd']
        nupassword = request.form['nuserpwd']
        uemail = request.form['email']

        # selected_user = session['uname']
        #判断输入的手机及邮箱是否已被使用
        user = Users.query.filter(or_(Users.email == uemail,Users.phone == uphone)).first()
        if user:
            return u'邮箱或手机已被使用，请重新输入！'

        user = Users.query.filter(Users.username == username).first()
        if user.password_hash != opassword:
            return u'原始密码不正确，请重新输入!'
        else:
            user.name = uname
            user.phone = uphone
            user.email = uemail
            user.password_hash = nupassword
            db.session.add(user)
            return redirect('/query')

if __name__ == '__main__':
    app.run(debug=True)
