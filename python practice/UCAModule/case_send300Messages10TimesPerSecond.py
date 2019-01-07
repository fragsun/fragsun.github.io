# -*- coding:UTF-8 -*-

#从 UCAModule 模块包中 import 两个模块
from UCAModule import ucaClient,ucaCaseMethod


#创建一个 ucaClient 对象，对象名为 a
a = ucaClient.ucaClient('130.255.3.137','7001')
#a 执行登录动作
a.login()
#a 向某用户发送指定消息，并设置频率
a.send_textMessage('7000', 'Hello World! ', 300, 10)
#a 执行登出动作
a.logout()
