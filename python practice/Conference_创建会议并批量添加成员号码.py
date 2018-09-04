# -*- coding:UTF-8 -*-

import os,time,datetime,re
import urllib,urllib2,cookielib
from bs4 import BeautifulSoup

'''
测试对象为基于SIP协议的VOIP服务器，业务功能是实现多个VOIP终端的会议通话。
测试目标是确定会议是否能达到规格中要求的指定人数同时参会。
测试环境：
    使用sipp模拟多个VOIP终端，当会议开始时，sipserver呼叫sipp，sipp响应呼叫，实现大量人数同时参会。
    创建会议需要通过sipserver的WEB管理页面，在页面上输入大量的参会号码操作起来较为困难、繁琐，因此做了python脚本实现创建有大量参会人员的会议。

第一版脚本的方案是首先通过sipserver的WEB管理页面创建一个普通会议，获取到会议号码后，向数据库中插入需要的sipp终端号码。由于操作繁琐，短时间内需要操作WEB、python脚本，sipp脚本，因此做了第二版脚本。
第二版脚本即本脚本，方案是再python脚本中输入相关信息（包括sipp脚本的起始号码及参会人数），然后通过urllib模块直接访问sipserver的WEB管理页面提交创建会议的POST请求，完成会议创建。

脚本逻辑是：
1、请求不需要重复输入的基本信息，如sipserver地址，sipp脚本的首个号码；
2、请求需要每次输入的单个任务信息，如会议人数；
3、访问创建会议的页面，获取需要的参数，然后根据1、2步骤的数据构建POST报文并提交完成会议创建；
4、在1、2步使用while循环，用于确认数据是否正确，和不退出循环使用；
'''


#定义个获取有效数字的方法，供其它函数调用
def get_aNumber(promptMsg,dictName,dictKey):
    while True:
        number = raw_input(promptMsg)
        if number.isdigit():
            dictName[dictKey] = int(number)
            break
        else:
            print('\n*** ERROR. input is invalid. ***')

 #获取基本信息：服务器IP、监听号码、sipp脚本的起始号码
def get_basic():
    global basicInfo        #创建一个字典，用于保存创建会议时需要的参数
    basicInfo = dict()
    while True:
        basicInfo['ip'] = raw_input('\nInput the server ip:\n')     #获取sipserver的ip地址
        print('Try to connect the server,please wait...')
        try:        #登陆sipserver的WEB页面（验证ip的有效性）
            loginForm = {
                'username':'admin',
                'password':'YWRtaW4=',
                'user_language':'zh-cn'}
            urlLogin = '/'.join(['http:/',basicInfo['ip'],'index.php'])
            cookie = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
            urllib2.install_opener(opener)
            loginPost = urllib.urlencode(loginForm).encode('utf-8')
            loginRequest = urllib2.Request(urlLogin,loginPost)
            urllib2.urlopen(loginRequest)
            print('Login WEB success.')
            break
        except:
            print('\n*** ERROR. login to WEB fialed, check the ip address! ***')
    get_aNumber('\nInput your phone number as monitor:\n',basicInfo,'monitor')      #获取监听号码，作为每次会议的固定参会号码，会议开始时邀请该号码参会，用于监听会议
    get_aNumber('\nInput the first phone number:\n',basicInfo,'numberStart')        #获取sipp脚本的起始号码，作为每次创建会议任务邀请的首个号码，后续获取到会议成员数量后，会议成员的号码在该号码上做自增

#获取任务信息：会议成员数量
def get_task():
    global taskInfo
    taskInfo = dict()
    get_aNumber('\nInput count of member:\n',taskInfo,'count')      #获取参会人数
    taskInfo['numberEnd'] = int(basicInfo['numberStart'])+int(taskInfo['count'])-1
    taskInfo['maxCount'] = int(taskInfo['count'])+10        #在会议成员数量上加10，作为最大参会人数

#通过向WEB服务器发送构建的POST来创建会议
def create_conference():
    conferForm = {
        'member_cnt':taskInfo['maxCount'],
        'password':'1',
        'password_member':'2',
        'moderator_mode_set':'0',
        'tele_name':'',
        'tele_view':'',
        'tele_description':'',
        'member_list':'',
        'verto_group_uuid':'',
        'conf_group_account':'',
        'old_account_num':'',
        'add_extension_name':'',
        'del_extension_number':'',
        'del_extension_name':'',
        'extension_number':'',
        'extension_name':''}        #创建一个字典，内容为POST提交表格中的参数，并在下文中对相应值做修改
    urlEditConfer = '/'.join(['http:/',basicInfo['ip'],'app/teleconference/teleconference_confctrl_edit.php?menu_uuid=65uuid74-9087-tl6w-7745-ecfbde5657d6'])
    clickAddRequest = urllib2.urlopen(urlEditConfer)
    clickAddSoup = BeautifulSoup(clickAddRequest.read(),'html.parser')      #获取创建会议的页面，在下文中解析相关参数，并修改conferForm字典
    # print(clickAddSoup)
    uuidElement = clickAddSoup.find_all(id='add_uuid')
    # print(uuidElement)
    addUuid = re.findall(r"value=\"(.+?)\"",str(uuidElement))[0]
    conferForm['member_list'] = addUuid
    startElement = clickAddSoup.find_all(attrs={"name":"start_time"})
    start_time = re.findall(r"value=\"(.+?)\"",str(startElement))[0]
    start_time = datetime.datetime.strptime(start_time,"%Y-%m-%d %H:%M")+datetime.timedelta(minutes=2)
    start_timeStr = datetime.datetime.strftime(start_time,"%Y-%m-%d %H:%M")
    conferForm['start_time'] = start_timeStr
    end_time = start_time+datetime.timedelta(days=1)
    end_timeStr = datetime.datetime.strftime(end_time,"%Y-%m-%d %H:%M")
    conferForm['end_time'] = end_timeStr
    phoneList = []      #定义列表，用于存储sipp脚本的参会号码
    for i in range (basicInfo['numberStart'],taskInfo['numberEnd']+1):
        phoneList.append(str(i))
    if str(basicInfo['monitor']) not in phoneList:
        phoneList.append(str(basicInfo['monitor']))
    phoneList = ','.join(phoneList)
    conferForm['add_extension_number'] = phoneList
    conferForm = urllib.urlencode(conferForm).encode('utf-8')
    addConferRequest = urllib2.Request(urlEditConfer,conferForm)        #提交POST，完成创建会议
    addConferResponse = urllib2.urlopen(addConferRequest)       #获取提交后的页面，判断是否创建成功，并解析出会议号码
    addConferSoup = BeautifulSoup(addConferResponse.read(),'html.parser')
    if len(re.findall(r"会议组号(.+?)添加完成",str(addConferSoup))) > 0:
        conferId = re.findall(r"会议组号(.+?)添加完成",str(addConferSoup))[0]
        print('''\n\nConference %s create SUCCESS! and start at 2 minutes later. '''%conferId)
    elif re.findall(r"会议总方数必须小于或者等于现在可利用方数",str(addConferSoup)):
        print('\n*** FAILD. license is not enough! ***')

#定义用到的提示信息
infoBasic = '''
Basic information:
--Server ip: %s
--Your phone number: %s
--Member start with: %s'''
infoTask = '''
Task information:
--Member end by: %s
--Member count: %s
--Max member count: %s'''
msgBasic = '''Press 's' to reset the data ups, or any other key to set task data.\n'''
msgTask = '''Press 's' to reset this conference, or any other key to start create conference.\n\n'''
msgNext = '''Start to create a new conference.'''

#主程序
while True:
    get_basic()     #获取基本信息：服务器IP、监听号码、sipp脚本的起始号码
    print(infoBasic%(basicInfo['ip'],basicInfo['monitor'],basicInfo['numberStart']))        #打印基本信息
    changeBasic = raw_input(msgBasic)       #通过输入判断是否需要修改基本信息，或是继续执行
    if changeBasic =='s':
        continue
    while True:
        get_task()      #获取任务信息：会议成员数量
        print(infoTask%(taskInfo['numberEnd'],taskInfo['count'],taskInfo['maxCount']))      #打印任务信息
        changeTask = raw_input(msgTask)       #通过输入判断是否需要修改基本信息，或是继续执行
        if changeTask == 's':
            continue
        create_conference()     #通过向WEB服务器发送构建的POST来创建会议
        print(infoBasic%(basicInfo['ip'],basicInfo['monitor'],basicInfo['numberStart']))        #打印基本信息
        print(msgNext)
