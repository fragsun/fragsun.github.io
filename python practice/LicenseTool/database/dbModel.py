# -*- coding:utf8 -*-

from database.exts import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class RegistLink(db.Model):
    __tablename__ = 'registLink'
    work_id = db.Column(db.String(48), unique=True, nullable=False, primary_key=True)
    email = db.Column(db.String(48), unique=True, nullable=False)
    regist_link = db.Column(db.String(64), unique=True)
    link_create_time = db.Column(db.DateTime)
    link_failure_time = db.Column(db.DateTime)
    regist_if = db.Column(db.Boolean)

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(48), unique=True, nullable=False)
    email = db.Column(db.String(48), db.ForeignKey('registLink.email'), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    regist_time = db.Column(db.DateTime)
    regist_ip = db.Column(db.String(48))
    last_login_time = db.Column(db.DateTime)
    last_login_ip = db.Column(db.String(48))
    user_relation = db.relationship('RegistLink', backref=db.backref('userInfo', lazy='joined'))    

    def __init__(self, username, password, email, regist_ip):
        self.username = username
        self.password = password
        self.email = email
        self.regist_time = datetime.utcnow()
        self.regist_ip = regist_ip
        self.last_login_time = self.regist_time
        self.last_login_ip = self.regist_ip

    def __repr__(self):
        return '<User %r>' % self.username

    @property
    def password(self):
        raise AttributeError('Password is readonly.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def isAdmin(self):
        if self.email == 'qiwei@mail.maipu.com':
            return True
        else:
            return False


class LicenseRecords(db.Model):
    __tablename__ = 'licenseRecords'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(48), nullable=False)
    from_ip = db.Column(db.String(48), nullable=False)
    create_time = db.Column(db.DateTime, nullable=False)
    device_code = db.Column(db.String(25), nullable=False)
    license_path = db.Column(db.String(128), nullable=False)
    download_time = db.Column(db.DateTime)

    def __init__(self, username, from_ip, device_code, license_path):
        self.username = username
        self.from_ip = from_ip
        self.create_time = datetime.utcnow()
        self.device_code = device_code
        self.license_path = license_path

