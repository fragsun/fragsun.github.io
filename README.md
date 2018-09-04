## 简介
坐标成都，从事测试工作。

这个repositories主要用于记录我的学习历程，主要学习方向：

#### 1. Linux操作应用；
目前已适应Linux操作系统的工作环境，常用操作系统有ContOS和Debian，对用户/用户组，权限，iptables，crontab，vim较为熟悉。可熟练使用

目标是：
* 掌握Shell编程；
* 熟悉Nginx；
* 熟悉Apache；

#### 2. Python编程；
业余时间学习Python，熟悉常用数据类型，if、for、while等逻辑控制语句，函数和类的定义和使用。常常写一点小脚本，努力将学习到的知识用于工作或日常需求，可进行文件操作、数据库操作，使用过logging、connect、paramiko、telnetlib、MySQLdb、pymysql、command、urllib、socket、bs4、uuid、socket等模块。

Python学习需要大量代码锻炼和积累，工作中几乎用不到，而工作之外又没有太多时间，对学习是很大的制约。

目标是：
* 掌握Python基础模块；
* 掌握Socket、HTTP等相关模块；
* 掌握Json；
* 掌握SMTP；
* 熟悉CUI；
* 熟悉GUI；

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

##### 2. path:[/python practice/Conference_创建会议并批量添加成员号码.py](https://github.com/fragsun/fragsun.github.io/blob/master/python%20practice/%E6%B5%8B%E8%AF%95%E7%BB%83%E6%89%8B_%E5%88%9B%E5%BB%BA%E4%BC%9A%E8%AE%AE%E5%B9%B6%E6%89%B9%E9%87%8F%E6%B7%BB%E5%8A%A0%E6%88%90%E5%91%98%E5%8F%B7%E7%A0%81.py)
在测试工作中，有一项测试任务需要在WEB页面输入大量的数据，因此写了Python脚本，在获取到必要信息的情况下，使用urllib模块构造POST报文，完成测试任务。
