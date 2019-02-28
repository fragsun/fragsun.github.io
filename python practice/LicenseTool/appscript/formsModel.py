# -*- coding:utf8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,IntegerField,RadioField,SelectField,BooleanField,SubmitField
from wtforms.validators import Length,DataRequired,Email,EqualTo,Optional,NoneOf


class createLicense_form(FlaskForm):
    device_code = StringField('机器码：', validators=[Length(min=25,max=25,message='机器码必须为25位。'),DataRequired(message='机器码不能为空。')])
    user_regist = IntegerField('用户授权数量:', validators=[Optional()])
    user_type = SelectField('用户授权类型:', choices=[('SIP', 'SIP'), ('UCA', 'UCA')])
    record_count = IntegerField('录音业务授权数:', validators=[Optional()])
    confer_count = IntegerField('会议业务授权数:', validators=[Optional()])
    expire = IntegerField('授权时长:', validators=[Optional()])
    soap_mod = BooleanField()
    submit = SubmitField('生成授权文件')

class login_form(FlaskForm):
    username = StringField('用户名：', validators=[DataRequired(message='用户名不得为空')])
    password = PasswordField('密码：', validators=[DataRequired(message='密码不得为空')])
    submit = SubmitField()

class regist_form(FlaskForm):
    username = StringField('用户名：', validators=[DataRequired(message='用户名不得为空')])
    email = StringField('邮箱：')
    password = PasswordField('密码：', validators=[DataRequired(message='密码不得为空')])
    pwd_confirm = PasswordField('确认密码：', validators=[DataRequired(message='再次输入密码'), EqualTo('password', message='密码不一致')])
    submit = SubmitField()

class regist_link(FlaskForm):
    work_id = StringField('工号：', validators=[DataRequired(message='工号不得为空')])
    email = StringField('邮箱：', validators=[DataRequired(message='邮箱不得为空'), Email(message='邮箱格式不正确')])
    submit = SubmitField()

class add_member(FlaskForm):
    work_id = StringField('工号：', validators=[DataRequired(message='工号不得为空')])
    email = StringField('邮箱：', validators=[DataRequired(message='邮箱不得为空'), Email(message='邮箱格式不正确')])
    submit = SubmitField()
