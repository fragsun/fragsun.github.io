# -*- coding:UTF-8 -*-

'''
测试对象为基于websocket的IM客户端，服务端基于verto模块，可以实现即使通信功能。
测试目标是确定IM客户端接收大量消息时的性能指标。
测试环境：
    服务端使用verto模块，客户端为Qt框架开发的PC客户端，使用websocket进行通信，内容使用json进行格式化。
    手动操作时，难以模拟出短时间内向指定用户发送大量信息的场景，因此写了python脚本，简单的实现了IM客户端发送信息的功能，用于辅助测试。

该脚本访问服务端的业务端口，建立websocket连接，通过向服务端发送指定格式的json信息，实现登陆、向指定用户发送大量消息等功能。

脚本逻辑：
1、请求登入的信息（服务端ip、用户名、密码、上线状态），确认登入信息无误后，向服务器发送登陆请求；
2、请求任务信息（接受消息的用户，消息内容、消息数量、频率），确认任务信息无误后，向用户发送信息；
3、在登入的时候，脚本会创建一个线程，用于发送ping包进行保活，防止长时间无动作掉线；
4、脚本中定义了一个生成器函数，用于生成json信息中的id值和消息内容后面的序列值；

'''


import time,threading
import socket,websocket,json
import hashlib,decimal

#获取登入使用的信息
def get_loginInfo():
    while True:
        while True:     #获取server的ip地址，并尝试建立websocket连接，确认ip是否有效
            server = raw_input('\nInput the server ip:\n')
            try:
                testConnection = websocket.create_connection('ws://%s:xxxx'%server)
                testConnection.close()
                break
            except Exception as err:
                print(''.join(['\tConnect to server failed! ',str(err)]))
        while True:     #获取登录用户名
            uid = raw_input('\nInput the login account:\n')
            if uid.isdigit():
                break
            else:
                print('\tAccount invalid! Input only accept numbers.')
        while True:     #获取登录密码
            pwd = raw_input('\nInput the login password:\n')
            if pwd != '':
                break
            else:
                print('\tPassword is empty!')
        while True:     #选择登录状态
            status = {'1':'online','2':'busy','3':'stealth','4':'away'}
            sta = str(raw_input('''\nSelect your status.
  1)  online
  2)  busy
  3)  stealth
  4)  away
Input the index number:\n'''))
            if sta in ['1','2','3','4']:
                break
            else:
                print("\tIndex invalid! Input only accept '1','3','4'.")
        print('''
Make sure the information is correct:
  Login as: %s [%s]
  Login stat: %s
  Server ip: %s'''%(uid,pwd,status[sta],server))
        resetGetInfo = raw_input('''Input 's' to reset the data ups, or any other key to set task data.\n''')       #确认信息是否正确
        if resetGetInfo != 's' :
            loginResult = method_login(uid,pwd,server,int(sta))     #调用method_login进行登录
            if loginResult == 'loginFailed':
                continue
            return uid
            break
        else:
            print('\n****** RESET INFORMATION ******')

#获取任务信息
def get_taskInfo():
    while True:
        while True:     #获取接收方账号并确认账号是否有效
            ruid = raw_input('\nInput the recever account:\n')
            if ruid == uid:
                print('\tRecever should not equal with sender.')
            elif ruid.isdigit():
                ifUserExist = search_account(ruid)
                if ifUserExist:
                    break
                else:
                    print('\tAccount is not exist!')
            else:
                print('\tAccount invalid! Input only accept numbers.')
        while True:     #获取消息内容
            msgContent = raw_input('\nInput the message you want send:\n')
            if msgContent != '':
                break
            else:
                print('\tPlease input something!')
        while True:     #获取消息数量
            msgCount = raw_input('\nInput the message count:\n')
            if msgCount.isdigit():
                if 0<int(msgCount) :
                    break
                else:
                    print('\tInvalid value! Count should greater than zero.')
            else:
                print('\tInvalid value! Only integer is accepted.')
        while True:     #获取发送消息的频率
            freque = raw_input('\nSet the frequency (1~10):\n')
            if freque.isdigit():
                if 0<int(freque)<=10 :
                    break
                else:
                    print('\tInvalid value! Out of range.')
            else:
                print('\tInvalid value! Only integer is accepted.')
        print('''
Make sure the task information is correct:
  Recever is: %s
  Message content: %s
  Message count: %s
  Send frequency: %s/s'''%(ruid,msgContent,msgCount,freque))
        resetTaskInfo = raw_input('''Input 's' to reset the data ups, or any other key to start send message.\n''')     #确认任务信息是否正确
        if resetTaskInfo != 's' :
            return [ruid,msgContent,int(msgCount),int(freque)]
            break
        else:
            print('\n****** RESET TASK ******')

#定义生成器
def idGen():
    idValue = 0
    yield idValue
    while True:
        idValue+=1
        yield idValue

#定义登录用户的方法
def method_login(uid,pwd,server,sta=1):
    userInfo = {
        'id':str(next(idseq)),
        'jsonrpc':'2.0',
        'method':'login',
        'params':{
                'ctype':'1',
                'echoParams':'request_params_auth',
                'type':'pc'
                }
    }
    loginRequest = json.dumps(userInfo)     #构造一个请求登录的json信息
    global client
    client = websocket.create_connection('ws://%s:xxxx'%server)     #建立websocket连接
    client.send(loginRequest)       #发送登录请求
    print('Start to connect ippbx ...')
    result = json.loads(client.recv())      #获取服务器的响应，并解析需要的信息
    nonce = str(result['error']['nonce'])
    realm = str(result['error']['realm'])
    URPMd5 = hashlib.md5()      #使用MD5计算认证字段
    URPMd5.update(':'.join([str(uid),realm,str(pwd)]))
    auth = URPMd5.hexdigest()
    URPNMd5 = hashlib.md5()
    URPNMd5.update(':'.join([auth,nonce]))
    auth = URPNMd5.hexdigest()
    method_auth = {
        'id':str(next(idseq)),
        'jsonrpc':'2.0',
        'method':'login',
        'params':{
                   'auth':auth,
                   'echoParams':'request_params_login',
                   'login':str(uid),
                  'st':sta
                }
    }
    authRequest = json.dumps(method_auth)       #构造认证的json信息
    client.send(authRequest)        #发送认证信息
    result = json.loads(client.recv())      #获取服务器的响应
    # print(result)
    if 'error' in result :
        print(result['error']['message']+'!')
        return 'loginFailed'
    elif result['result']['message'] == 'logged in' :
        print(' '.join([str(uid),'Login success.']))
        keepaliveThread = threading.Thread(target=keepalive)        #创建线程，调用keepalive方法用于发送ping进行保活
        keepaliveThread.setDaemon(True)
        keepaliveThread.start()

#定义保活方法
def keepalive():
    while True:
        time.sleep(15)
        client.ping()

#定义搜索用户的方法
def search_account(uid):
    searchAccount = {
        "id":str(next(idseq)),
        "jsonrpc":"2.0",
        "method":"verto.mgm",
        "params":{
                "cmd":"findu",
                "condition":str(uid),
                "echoParams":"request_params_search_users_online",
                "pageNum":"1",
                "pageSize":"20"
        }
    }
    client.send(json.dumps(searchAccount))      #构造并发送搜索用户的json信息
    searchResult = client.recv()        #接收服务器响应并判断是否有此用户
    # print(searchResult)
    if '"uid":"%s"'%str(uid) in searchResult :
        return True
    else :
        return False

#定义发送消息的方法
def send_textMessage(uid,ruid,msg):
    textMessage = {
        "id":str(next(idseq)),
        "jsonrpc":"2.0",
        "method":"verto.info",
        "params":{
                "describe":"online",
                "echoParams":"request_params_send_mix_message",
                "msg":{
                        "body":"[{\"text\": \"%s\"}]"%str('.'.join([msg,str(next(msgId))])),
                        "from":str(uid),
                        "style":"",
                        "to":str(ruid),
                        "type":"mixing"
                }
        }
    }
    client.send(json.dumps(textMessage))        #构造并发送发送消息的json信息
    client.recv()       #接收服务器响应


idseq = idGen()     #调用生成器方法，用于生成json消息的id值
uid = get_loginInfo()       #获取用户信息并登录
while True:
    task = get_taskInfo()       #获取任务信息
    print('\nSending messages.')
    msgId = idGen()     #调用生成器方法，用户生成消息序列
    for sendN in range (task[2]):       #根据消息数量循环执行发送消息的任务
        send_textMessage(uid,task[0],task[1])       #调用发送文本消息的方法
        time.sleep(decimal.Decimal(1)/decimal.Decimal(task[3]))     #根据任务的频率值调整sleep时间
        print('>'),
    print('\nAll messages has send out.\n')
    ifContiune = raw_input("\nInput any key to start a new task, or 'q' to exit:\n")
    if ifContiune == 'q':
        print('Exiting...')
        break
client.close()