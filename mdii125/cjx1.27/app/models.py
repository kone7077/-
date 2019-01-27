from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager

class Optionalfood(db.Model):
    __tablename__="optionalfood"
    id=db.Column(db.Integer,primary_key=True)
    # 菜名
    cname=db.Column(db.String(30),nullable=False)
    # 单价
    cprice=db.Column(db.Float,nullable=False)
    # 积分
    points=db.Column(db.Integer,nullable=False)
    # 主料
    ingredients=db.Column(db.String(50))
    # 口味
    taste=db.Column(db.String(50))
    # 分类
    type=db.Column(db.String(50),nullable=False)
    # 库存
    stock=db.Column(db.Integer,nullable=False,default=0)
    # 图片
    images=db.Column(db.Text,nullable=False)
    #订餐方式
    mealmeans=db.Column(db.String(200),nullable=False)
    def to_dict(self):
        dic={
            'id': self.id,
            'cname':self.cname,
            'cprice':self.cprice,
            'points':self.points,
            'ingredients':self.ingredients,
            'taste':self.taste,
            'type':self.type,
            'stock':self.stock,
            'images':self.images,
            'mealmeans':self.mealmeans
        }
        return dic

class Fixedpackage(db.Model):
    __tablename__ = "fixedpackage"
    id = db.Column(db.Integer, primary_key=True)
    # 菜名
    cname = db.Column(db.String(30), nullable=False)
    # 单价
    cprice = db.Column(db.Float, nullable=False)
    # 积分
    points = db.Column(db.Integer, nullable=False)
    # 配菜
    peicai = db.Column(db.String(200))
    # 分类
    type = db.Column(db.String(50), nullable=False)
    # 库存
    stock = db.Column(db.Integer, nullable=False, default=0)
    # 图片
    images = db.Column(db.Text, nullable=False)
    # 订餐方式
    mealmeans = db.Column(db.String(200), nullable=False)
    def to_dict(self):
        dic = {
            'id': self.id,
            'cname': self.cname,
            'cprice': self.cprice,
            'points': self.points,
            'peicai': self.peicai,
            'type': self.type,
            'stock': self.stock,
            'images': self.images,
            'mealmeans':self.mealmeans
        }
        return dic

#订单记录
class Orderrecord(db.Model):
    __tablename__ = "orderrecord"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    cname = db.Column(db.String)
    cprice = db.Column(db.Integer)
    type =db.Column(db.String)
    mealmeans = db.Column(db.String)
    ordertime = db.Column(db.DateTime)


# 积分换赠物品信息
class Goodsreplace(db.Model):
    __tablename__ = "goodsreplace"
    id = db.Column(db.Integer, primary_key=True)
    goodsname = db.Column(db.String, nullable=False)
    points_price = db.Column(db.Integer, nullable=False)
    images = db.Column(db.Text, nullable=False)



class User(db.Model,UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer,primary_key=True)
    #用户名／昵称
    username = db.Column(db.String(20),unique=True,index=True)
    #手机号
    # phone = db.Column(db.Integer,unique=True,index=True)
    phone = db.Column(db.String(13), unique=True, index=True)
    #邮箱地址
    email = db.Column(db.String(254),unique=True,index=True)
    #密码
    password_hash = db.Column(db.String(200))#这里传入的是加密后的密码
    #真实姓名
    name = db.Column(db.String(30))
    #头像
    # photoer = db.Column(db.Text)

    # @property
    # def password(self):
    #     raise AttributeError('password is not a readable attribute')

    # @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):
        #定义比较密码的方法：传入用户输入的密码，返回bool值
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return '<User %r>'%self.username

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
