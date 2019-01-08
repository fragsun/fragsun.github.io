## 简介
坐标成都，从事测试工作。

这个repositories主要用于记录我的学习历程，主要学习方向：

#### 1. Linux操作应用；
目前已适应Linux操作系统的工作环境，常用操作系统有ContOS和Debian，对用户/用户组，权限，iptables，crontab，vim较为熟悉,可熟练使用。

目标是：
* 掌握MySQL应用；
* 掌握Shell编程；
* 熟悉Nginx；
* 熟悉Apache；

#### 2. Python编程；
业余时间学习Python，熟悉常用数据类型，if、for、while等逻辑控制语句，函数和类的定义和使用。常常写一点小脚本，努力将学习到的知识用于工作或日常需求，可进行文件操作、数据库操作，使用过logging、connect、paramiko、telnetlib、MySQLdb、pymysql、command、urllib、socket、bs4、uuid、socket等模块。

Python学习需要大量代码锻炼和积累，工作中几乎用不到，而工作之外又没有太多时间，对学习是很大的制约。

目标是：
* 掌握Python基础模块；
* 掌握websocket,requests等相关模块；
* 掌握Json使用；
* 掌握SMTP使用；
* 熟悉GUI；
* 熟悉Flask框架;
* 熟悉Django框架；

#### 3. 自动化测试；
有过RobotFramework框架下，Selenium自动化测试经历，测试对象为WEB服务端。由于项目中测试的自动化覆盖率不高，未深入使用，对环境搭建、基础库、元素定位比较熟悉（曾自学过HTML和CSS）。

目标是：
* 深入Selenium；
* 掌握Appium；
* 熟悉QTP；
* 熟悉Loadrunner；

## Python练习记录：

##### 1. path:[/python practice/checkNet.py](https://github.com/fragsun/fragsun.github.io/blob/master/python%20practice/checkNet.py)
学以致用，写个脚本用于检查局域网是否有新设备接入，在发现新设备接入的情况下，将新设备信息以邮件方式发送至邮箱进行提醒。脚本放在家用NAS的Linux虚拟机中，使用crontab定时运行。

##### 2. path:[/python practice/测试练手_创建会议并批量添加成员号码.py](https://github.com/fragsun/fragsun.github.io/blob/master/python%20practice/%E6%B5%8B%E8%AF%95%E7%BB%83%E6%89%8B_%E5%88%9B%E5%BB%BA%E4%BC%9A%E8%AE%AE%E5%B9%B6%E6%89%B9%E9%87%8F%E6%B7%BB%E5%8A%A0%E6%88%90%E5%91%98%E5%8F%B7%E7%A0%81.py)
在测试工作中，有一项测试任务需要在WEB页面输入大量的数据，因此写了Python脚本，在获取到必要信息的情况下，使用urllib模块构造POST报文，完成测试任务。

##### 3. path:[/python practice/测试练手_发送即时消息 1to1.py](https://github.com/fragsun/fragsun.github.io/blob/master/python%20practice/%E6%B5%8B%E8%AF%95%E7%BB%83%E6%89%8B_%E5%8F%91%E9%80%81%E5%8D%B3%E6%97%B6%E6%B6%88%E6%81%AF%201to1.py)
在测试工作中，有一项测试任务需要确定IM客户端接收大量消息时的性能指标。服务端使用verto模块，客户端为Qt框架开发的PC客户端，使用websocket进行通信，内容使用json进行格式化。该脚本访问服务端的业务端口，建立websocket连接，通过向服务端发送指定格式的json信息，实现登陆、向指定用户发送大量消息等功能。

脚本中使用到websocket和json模块用于和服务端进行交互，使用了生成器用于生成交互信息中的id，使用threading模块创建子线程和服务端进行保活。

##### 4. path:[/python practice/UCAModule](https://github.com/fragsun/fragsun.github.io/tree/master/python%20practice/UCAModule)
在上一个练习中，为了测试IM客户端的一些性能指标，使用py脚本模拟客户端和服务器建立连接。后来为了实现更多功能设计了UCAModule模块，使用一个ucaClient.ucaClient()方法来创建一个模拟的UCA对象，然后通过封装的其它方法，对该UCA对象进行各种操作。

目前ucaClient.ucaClient()对象有登录、登出、保活、发送消息、监听端口等方法，可以模拟一个基本的客户端，更多的方法可以根据需要进行扩展添加。通过该模块可以对服务器进行接口测试、性能测试，也可以作为辅助工具进行客户端测试，也可以作为其他框架RobotFramework、Appium的辅助工具。
