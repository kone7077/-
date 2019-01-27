# /usr/bin/env/python
# coding=utf-8
from flask import *
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import *
from .models import User



#用户注册表单
class RegistForm(FlaskForm):
    #设置用户名
    username = StringField('username',render_kw={'placeholder':'任何字符组成的3-6位用户名'},validators=[DataRequired(),Length
    (3,12)])
    name = StringField('name',validators=[DataRequired()],render_kw={'placeholder':'填写你的真实名字'})
    phone = StringField('phone',validators=[DataRequired(),Length(10,12)],render_kw={'placeholder':'填写由11位数字组成的手机号'})
    email = StringField('email',validators=[DataRequired(),Length(6,254)],render_kw={'placeholder':'请填写您的邮箱地址'})
    #设置新密码
    password_hash = PasswordField('Passwd',validators=[DataRequired()])
    #设置确认密码
    password_again = PasswordField('passwd1',validators=[DataRequired()])
    #立即注册
    register = SubmitField('     立即注册     ')

    def validate_email(self,field):
    #定义方法完成与数据库交互，用来判断邮箱是否存在
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(u'邮箱已存在')

    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            flash(u'用户名已存在')

    def validate_phone(self,field):
        if User.query.filter_by(email=field.data).first():
            flash(u'手机号已注册')
#登录表单
class LoginForm(FlaskForm):
    username = StringField('username',validators=[DataRequired()],render_kw={'placeholder':'请填写你的用户名'})
    password = PasswordField('passwd',validators=[DataRequired()],render_kw={'placeholder':'请填写密码！'})
    remember_me = BooleanField()
    login = SubmitField('　　　　　登录　　　　　')

