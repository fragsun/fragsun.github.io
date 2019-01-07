## UCAModule简介
UCAModule是一个使用python编写的模块包，通过和IPPBX建立websocket连接，模拟发送UCA的消息报文，实现一些简单的UCA功能。

## UCAModule设计思路：
UCAModule模块包，使用一个ucaClient.ucaClient()方法来创建一个模拟的UCA对象，然后通过封装的其它方法，对该UCA对象进行各种操作。UCAModule模块包无法直接运行，需要import到其它的python脚本中进行调用。
相比函数式脚本，这种方式复用性高，可以根据用例的需要灵活的组合，实现比较丰富的功能。
也可以结合RobotFramework自动化测试框架使用，辅助用例实现一些测试动作。

## UCAModule运行环境：
UCAModule解压后结构如下：
<pre><code>
anyPath
|——UCAModule
|       |——__init__.py
|       |——ucaClient.py
|       |——ucaJson.py
|       |——ucaCaseMethod.py
|
|——testcase.py

__init__.py：模块包声明文件；
ucaClient.py：用于封装UCA客户端的功能；
ucaCaseMethod.py：封装UCA客户端原生功能以外，用于测试用例的功能；
ucaJson.py：用于封装UCA客户端的json消息格式（目前json消息直接写在ucaClient.py中，如果模块继续添加功能，计划单独封装，易于维护）；
</pre></code>

## UCAModule实现的功能：
目前UCAModule能够实现UCA登录、登出、保活、发送消息、监听消息、记录消息等功能，目前来看功能还是较为简单。

## UCAModule实现的功能：
#### 实例1：向某用户连续发送300条消息，每秒发送10条；
<pre><code>
# -*- coding:UTF-8 -*-

from UCAModule import ucaClient,ucaCaseMethod

#创建一个 ucaClient 对象，对象名为 a
a = ucaClient.ucaClient('130.255.3.137','7001')
#a 执行登录动作
a.login()
#a 向某用户发送指定消息，并设置频率
a.send_textMessage('7000', 'Hello World! ', 300, 10)
#a 执行登出动作
a.logout()
</pre></code>

#### 实例2：脚本实现“将监听端口收到的UCA信息进行记录，并和指定文件做对比”的功能，RobotFramework调用脚本，并接收到一个返回值判断对比结果；
<pre><code>
# -*- coding:UTF-8 -*-

from UCAModule import ucaClient,ucaCaseMethod
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
</pre></code>
