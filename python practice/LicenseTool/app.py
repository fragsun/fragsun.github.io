# -*- coding:UTF-8 -*-


import sys, os, logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
from flask import Flask, render_template, redirect, request, url_for, send_from_directory, g
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from appscript import formsModel
from appscript.sendMail import registLink, sendMail
from appscript import createLicense as CL
from database.exts import db
from database import dbModel


app = Flask(__name__)
app.config.from_object("config.Config")
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)


@login_manager.user_loader
def load_user(userid):
    return dbModel.User.query.get(int(userid))


@app.route('/')
def root():
    return redirect(url_for('login'))


@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('licenseGen'))
    else:
        forms = formsModel.login_form()
        if forms.validate_on_submit():
            user = dbModel.User.query.filter_by(username=forms.username.data).first()
            if user is not None and user.verify_password(forms.password.data):
                login_user(user)
                user.last_login_time = datetime.utcnow()
                user.last_login_ip = request.remote_addr
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('licenseGen'))
            else:
                return render_template('login.html', form=forms, errorReason='auth_failure')
        return render_template('login.html', form=forms)


@app.route('/regist', methods=['POST', 'GET'])
def regist():
    if current_user.is_authenticated:
        return redirect(url_for('login'))
    else:
        forms = formsModel.regist_link()
        if forms.validate_on_submit():
            work_id = dbModel.RegistLink.query.filter_by(work_id=forms.work_id.data, email=forms.email.data.lower()).first()
            if work_id is not None:
                if work_id.regist_if:
                    return render_template('message.html', msg='already_regist')
                else:
                    newRegist = registLink(forms.work_id.data, forms.email.data.lower())
                    print(newRegist)
                    work_id.regist_link = newRegist[0]
                    work_id.link_create_time = newRegist[1]
                    work_id.link_failure_time = newRegist[2]
                    db.session.add(work_id)
                    db.session.commit()
                    sendMail(forms.work_id.data, forms.email.data, newRegist[0])
                    return render_template('message.html', msg='link_send')
            else:
                return render_template('message.html', msg='not_permit')
        return render_template('regist.html', form=forms)


@app.route('/regist/<md5>', methods=['POST', 'GET'])
def regist_form(md5):
    if current_user.is_authenticated:
        return render_template('message.html', msg='logout_required')
    if request.method == 'GET':
        url = request.url
        link_check = dbModel.RegistLink.query.filter_by(regist_link=url).first()
        if link_check is not None and not link_check.regist_if:
            now = datetime.utcnow()
            if now > link_check.link_failure_time:
                return render_template('message.html', msg='link_timeout')
            else:
                forms = formsModel.regist_form()
                forms.email.data=link_check.email
                return render_template('regist_form.html', form=forms, md5=md5)
        else:
            return render_template('message.html', msg='link_invalid')
    elif request.method == 'POST':
        forms = formsModel.regist_form()
        if forms.validate_on_submit():
            if dbModel.User.query.filter_by(username=forms.username.data.lower())[:]:
                forms.username.errors = ['用户名被占用']
                return render_template('regist_form.html', form=forms, md5=md5)
            else:
                user = dbModel.User(username=forms.username.data, password=forms.password.data, email=forms.email.data.lower(), regist_ip=request.remote_addr)
                user_link = dbModel.RegistLink.query.filter_by(email=forms.email.data.lower(), regist_link=request.url).first()
                user_link.regist_if = True
                db.session.add_all([user,user_link])
                db.session.commit()
                return render_template('message.html', msg='regist_success')
        return render_template('regist_form.html', form=forms, md5=md5)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/add_member', methods=['POST', 'GET'])
@login_required
def add_member():
    forms = formsModel.regist_link()
    if forms.validate_on_submit():
        if dbModel.RegistLink.query.filter_by(email=forms.email.data.lower())[:] or dbModel.RegistLink.query.filter_by(work_id=forms.work_id.data)[:]:
            return render_template('add_member.html', form=forms, result='added', work_id=forms.work_id.data, email=forms.email.data.lower())
        else:
            add_id = dbModel.RegistLink(work_id=forms.work_id.data, email=forms.email.data.lower())
            db.session.add(add_id)
            db.session.commit()
            return render_template('add_member.html', form=forms, result='success', work_id=forms.work_id.data, email=forms.email.data.lower())
    return render_template('add_member.html', form=forms)


@app.route('/license/<licenseFile>')
@login_required
def download(licenseFile):
    path = '/'.join(['licensefiles', licenseFile.split('_')[0]])
    app.logger.info('\nLicense file is download: %s\n'%licenseFile)
    return send_from_directory(path, licenseFile, as_attachment=True)


@app.route('/licenseGen', methods=['POST','GET'])
@login_required
def licenseGen():
    g.isAdmin = current_user.isAdmin()
    forms = formsModel.createLicense_form()
    if forms.validate_on_submit():
        formData = dict()
        formData.update(forms.data)
        del formData['csrf_token']
        del formData['submit']
        app.logger.info('\nGet a license create requests:\n From: %s\n Agent: %s\n Cookies: %s\n Forms: %s\n'%(request.remote_addr, request.user_agent, request.cookies, formData))
        licenseFile = CL.createLicense(formData)
        app.logger.info('\nLicense file Path: %s\nLicense Detail:\n%s'%(licenseFile[0], licenseFile[1]))
        licenseFileName = licenseFile[0].split('/')[-1]
        return render_template('license_generator.html', title='授权工具', display_value='block', licenseLink=licenseFileName, forms=forms)
    else:
        return render_template('license_generator.html', title='授权工具', display_value='none', forms=forms)




if __name__ == '__main__':

    cwd = '/'.join(sys.argv[0].split('/')[:-1])
    log_path = cwd+'/log'
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    log_file = log_path+'/app.log'

    handler = RotatingFileHandler(log_file, maxBytes=1024*1024)
    fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(message)s'
    formatter = logging.Formatter(fmt)
    handler.setFormatter(formatter)

    app.logger.addHandler(handler)
    app.logger.setLevel(logging.DEBUG)
    app.run(host='130.255.3.132', port=8080, debug=True)

