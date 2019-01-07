# UCAModule简介
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
