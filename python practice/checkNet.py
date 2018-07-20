#-*-coding:utf-8-*-

'''
这个脚本用于检查局域网是否有新设备接入，在发现新设备接入的情况下，将新设备信息以邮件方式发送至邮箱进行提醒。

分为以下几个步骤：
1、登陆路由器的管理页面，获取当前设备信息；
2、将获取到的设备信息逐一和数据库中的设备进行比对，MAC地址作为设备标识；
    若发现设备已存在，检查设备的其它信息是否变化，有变化则将信息更新至数据库；
    若设备不存在，将设备信息插入数据库；
3、将比对结果中需要关注的信息以邮件方式发送至指定邮箱；
4、操作过程中的关键步骤生成log日志进行记录；

可以优化的地方：
1、使用urllib模块登陆路由器时，会在局域网暴露路由器的IP及管理员账号；可以尝试使用nmap进行扫描；
2、没有考虑容错情况，如无法访问路由器，无法访问数据库，邮件发送失败；可以通过try对抛出异常的情况进行处理；
3、据资料，操作数据库的方法存在注入漏洞；
4、sendmail的操作方式较为粗暴;

'''

import os
import re
import urllib.request
import pymysql
import logging
from bs4 import BeautifulSoup

url = "http://x.x.x.x/xxxx.htm"      #路由器管理页面
user = 'username_route'      #路由器账号
pwd = 'password_route'        #路由器密码

#定义logging方法，用于记录相关日志
def def_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logfile = 'log.txt'     #日志文件路径
    logConfig = logging.FileHandler(logfile, mode='a')
    logConfig.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - [line:%(lineno)d] - %(levelname)s: %(message)s')
    logConfig.setFormatter(formatter)
    logger.addHandler(logConfig)
    return logger
logger = def_logger()

#定义方法获取局域网设备信息
def get_device_list(url,user,pwd):
    #使用urllib创建POST报文登陆路由器管理页面
    logger.debug("Try to connect the route.")
    authMsg = urllib.request.HTTPPasswordMgrWithDefaultRealm()
    authMsg.add_password(None,url,user,pwd)
    login = urllib.request.HTTPBasicAuthHandler(authMsg)
    urlOpener = urllib.request.build_opener(login)
    urlOpener.addheaders = [
    ('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'),
    ('Cookie','XSRF_TOKEN=3284348705')
    ]
    getHtm = urlOpener.open(url).read()
    logger.debug("Conent to the route success.")

    allDevice = []
    i = 0
    #使用BeautifulSoup从页面中提取设备信息
    htm = BeautifulSoup(getHtm,"html.parser")
    for ip in htm.find_all("span",attrs={"name":"rule_ip"}):
        device = []
        mac = ip.parent.next_sibling.next_sibling
        device.append(mac.get_text())
        device.append(ip.get_text())
        dev = mac.next_sibling.next_sibling
        device.append(dev.get_text())
        allDevice.append(device)
        # print (device)
        logger.debug("Extract device information success.  %s" %device)
    return allDevice

#定义方法，将获取到的设备信息和数据库中的设备进行比对，并根据结果对数据库进行操作
def compare_with_db(deviceFromRoute):
    logger.debug("Try to connect the database.")
    db = pymysql.connect(host='x.x.x.x',port=3307,user='username_db',passwd='passwd_db',db='db_name')
    cursor = db.cursor()
    i = 0
    logSummary = []
    while i <len(deviceFromRoute) :
        check_sql = '''SELECT * FROM net_device WHERE mac_add='%s';''' %(deviceFromRoute[i][0])
        cursor.execute(check_sql)
        checkResult = cursor.fetchall()
        if len(checkResult) != 0:    #查询到该设备时
            logger.debug('''Device '%s' is find in database, name is '%s', current ip is '%s'.''' %(deviceFromRoute[i][0],checkResult[0][2],deviceFromRoute[i][1]))
            if (deviceFromRoute[i][1] != checkResult[0][1]):    #检查设备ip是否变化
                logIpChange = '''Device '%s' ip is changed, device name is '%s', former ip is '%s', current ip is '%s'.''' %(deviceFromRoute[i][0],checkResult[0][2],checkResult[0][1],deviceFromRoute[i][1])
                logger.info(logIpChange)
                logSummary.append(logIpChange)
                # print (logIpChange)
                updateIp = '''UPDATE net_device SET ip_add='%s' WHERE mac_add='%s';''' %(deviceFromRoute[i][1],deviceFromRoute[i][0])
                cursor.execute(updateIp)
                db.commit()
                logger.info('''Update the device ip. Execute sql command: %s''' %updateIp)
                # print (updateIp)
            if (deviceFromRoute[i][2] != checkResult[0][2]):    #检查设备名称是否变化
                logNameChange = '''Device '%s' name is changed, former name is '%s', current name is '%s'.''' %(deviceFromRoute[i][0],checkResult[0][2],deviceFromRoute[i][2])
                logger.warning(logNameChange)
                logSummary.append(logNameChange)
                # print (logNameChange)
                updateName = '''UPDATE net_device SET dev_name='%s' WHERE mac_add='%s';''' %(deviceFromRoute[i][2],deviceFromRoute[i][0])
                cursor.execute(updateName)
                db.commit()
                logger.info('''Update the device name. Execute sql command: %s''' %updateName)
                # print (updateName)
        else:    #未查询到该设备时
            logUnkownDevice = '''Device '%s' is not exist in database! device will record into datebase.''' %(deviceFromRoute[i][0])
            logger.critical(logUnkownDevice)
            logSummary.append(logUnkownDevice)
            # print (logUnkownDevice)
            insertDevice = '''INSERT INTO net_device (mac_add,ip_add,dev_name) VALUES ('%s','%s','%s');''' %(deviceFromRoute[i][0],deviceFromRoute[i][1],deviceFromRoute[i][2])
            # print (insertDevice)
            cursor.execute(insertDevice)
            db.commit()
            logger.info('''Device '%s' has insert to database. Execute sql command: %s''' %(deviceFromRoute[i][0],insertDevice))
            logSummary.append(insertDevice)
        i += 1
    db.close()
    return logSummary

#定义发送邮件的方法
def mail_log(mailAddress,mailContent):
    logger.debug("Start to send mail.")
    sender = 'admin@mail.com'      #发件人地址
    receiver= mailAddress
    subject = "Log summary of checknet process"
    formatterContent=('''
    The network in home has some changes.Follow log messages as a reference.
    ------process log------
    %s
    '''%mailContent)

    mall = ('''From: %s
    receiver: %s
    subject: %s
    %s
    '''%(sender,receiver,subject,formatterContent))

    os.system('''sendmail -t << EOF\n%s\nEOF\n'''%mall)
    logger.debug("Mail of log summary is send to %s."%mailAddress)

logger.debug("Process is start.")
all_device_info = get_device_list(url,user,pwd)
mailContent = '\n'.join(compare_with_db(all_device_info))
mail_log('user@mail.com',mailContent)       #使用mail_log方法发送邮件，传入收件人参数
logger.debug("Process is end.")
print (mailContent)