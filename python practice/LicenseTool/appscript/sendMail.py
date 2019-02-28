# -*- coding:utf8 -*-

import smtplib, hashlib
from email.mime.text import MIMEText
from email.header import Header
from datetime import datetime, timedelta


def registLink(work_id, mail):
    serverip = 'http://130.255.3.132:8080/regist/'
    salt = 'ippbx'
    link_ctime = datetime.utcnow()
    link_etime = link_ctime + timedelta(minutes=15)
    print(link_ctime, link_etime)
    md5String = '+'.join([work_id, mail, str(link_ctime), salt])
    md5Encrypted = hashlib.md5(md5String.encode('utf-8')).hexdigest()
    link = ''.join([serverip, md5Encrypted[7:]])

    item = [link, link_ctime, link_etime]

    return item


def sendMail(name, mail, link):
    sender = 'admin@ippbx.com'
    adminMail = 'qiwei@mail.maipu.com'
    receivers = [adminMail, mail]

    msg = '''您好，%s:
    这是您的注册链接，请在15分钟内点击链接进行注册，15分钟后该链接将失效。
    %s'''%(name, link)
    message = MIMEText(msg, 'plain', 'utf-8')
    message['From'] = Header('IPPBX 管理员', 'utf-8')
    message['To'] = Header(name, 'utf-8')
    message['Subject'] = Header('您的注册链接', 'utf-8')
    
    smtpObj = smtplib.SMTP('mail.maipu.com')
    smtpObj.sendmail(sender, receivers, message.as_string())



if __name__ == '__main__' :
    a = registLink('baby','qiwei@mail.maipu.com')
    print (a) 
