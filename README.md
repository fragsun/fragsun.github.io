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
业余时间学习Python，常常写一点小脚本，努力将学习到的知识用于工作或日常需求，可进行文件操作、数据库操作，使用过logging、connect、paramiko、telnetlib、MySQLdb、pymysql、command、urllib、socket、bs4、uuid、websocket等模块。


自动化测试学习目标是：
* 掌握Python基础模块；
* 掌握websocket,requests等相关模块；
* 掌握Json使用；
* 掌握SMTP使用；
* 熟悉GUI；
* 熟悉Flask框架;
* 熟悉Django框架；

#### 3. 自动化测试；
有过RobotFramework框架下，Selenium自动化测试经历，测试对象为WEB服务端，设计过数百条自动化用例。

RobotFramework框架使用感言：对于不会代码的测试人员来说，是比较好的自动化方向切入点，可以快速实现自动化测试。内建的关键字可以方便的实现页面元素检查和断言。但是深入使用也会发现局限性比较大，web开发和测试的逻辑未必相同，所以在进行一些数据处理时，怎样将页面数据、数据库数据、服务器文件中的数据处理成可以使用的数据类型就比较重要，这时候RobotFramework以下特性的不方便就会凸显：
+ 数据类型不好理解；
+ 对中文字符支持不友好；
+ evaluate只支持单行python语言；
+ 不支持多重循环和判断分支；
+ 循环和判断分支中变量定义不方便；

自动化测试的学习目标是：
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

##### 5. path:[/python practice/LicenseTool](https://github.com/fragsun/fragsun.github.io/tree/master/python%20practice/LicenseTool)
近期学习了Flask，于是用Flask框架写了一个web版本的license生成工具，方便在测试活动中生成license文件。考虑到lincense的敏感性，需要来访者注册、登录后才能访问lincense工具。主要流程是：管理员添加授权工号和邮箱 --> 来访者通过填写工号和邮箱获取注册链接 --> 通过访问注册链接完成用户注册 --> 登录后使用license工具 --> 日志记录每次生成的lincense信息用于追溯。

这个web使用了flask_wtf提供表单创建和验证，flask_login提供用户管理，flask_sqlalchemy提供数据库ORM模型，smtplib提供邮件发送功能。
