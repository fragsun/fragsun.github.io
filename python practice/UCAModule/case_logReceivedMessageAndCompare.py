# -*- coding:UTF-8 -*-

#从 UCAModule 模块包中 import 两个模块
from UCAModule import ucaClient,ucaCaseMethod
#设置监听时长需要 time 模块，import 该模块
import time

#定义一个方法，该方法的参数取决与方法内部语句需要什么参数
def log_received_message_and_compare(serverip, uid, sourceFilePath, sleepTime=60):
    #创建一个 ucaClient 对象，对象名为 a
    a = ucaClient.ucaClient(serverip,uid)
    #a 执行登录动作
    a.login()
    #a 开始记录监听到的UCA消息
    a.log_received_message_start()
    #a 设置监听时长
    time.sleep(sleepTime)
    #a 停止记录监听到的UCA消息，a 会生成一个 a.logFilePath 的属性，其值为记录文件的保存路径
    a.log_received_message_stop()
    #a 执行登出动作
    a.logout()
    #使用指定的源文件，和记录的 UCA 消息文件进行比对，将返回值保存到 compareResult 变量
    compareResult = ucaCaseMethod.compare_file(sourceFilePath,a.logFilePath)
    #返回 compareResult 变量
    return compareResult

#脚本测试语句
if __name__ == '__main__':
    results = log_received_message_and_compare('130.255.3.137', '7002', 'F:\\python\\test\\ippbx\\UCA\\received_message_20181024-1358.56.txt')