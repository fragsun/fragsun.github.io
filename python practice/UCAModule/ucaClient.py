# -*- coding:UTF-8 -*-

import time,threading,os
import websocket,json
import hashlib,decimal


class ucaClient:
    def __init__(self, server, username, passwd=666666, stat=1):
        self.server = server
        self.username = username
        self.passwd = passwd
        self.stat = stat
        self.idseq = self.idGen()


    def idGen(self):
        idValue = 0
        yield idValue
        while True:
            idValue+=1
            yield idValue

    def login(self):
        loginInfo = {
            'id':str(next(self.idseq)),
            'jsonrpc':'2.0',
            'method':'login',
            'params':{
                    'ctype':'1',
                    'echoParams':'request_params_auth',
                    'type':'pc'
                    }
        }
        loginRequest = json.dumps(loginInfo)
        self.client = websocket.create_connection('ws://%s:8081'%self.server)
        self.client.send(loginRequest)
        print('Start to connect ippbx ...')
        result = json.loads(self.client.recv())
        nonce = str(result['error']['nonce'])
        realm = str(result['error']['realm'])
        URPMd5 = hashlib.md5()
        URPMd5.update(':'.join([str(self.username),realm,str(self.passwd)]))
        auth = URPMd5.hexdigest()
        URPNMd5 = hashlib.md5()
        URPNMd5.update(':'.join([auth,nonce]))
        auth = URPNMd5.hexdigest()
        method_auth = {
            'id':str(next(self.idseq)),
            'jsonrpc':'2.0',
            'method':'login',
            'params':{
                       'auth':auth,
                       'echoParams':'request_params_login',
                       'login':str(self.username),
                      'st':self.stat
                    }
        }
        authRequest = json.dumps(method_auth)
        self.client.send(authRequest)
        result = json.loads(self.client.recv())
        if 'error' in result :
            print(result['error']['message']+'!')
            return 'loginFailed'
        elif result['result']['message'] == 'logged in' :
            print(' '.join([str(self.username),'Login success.']))
            self.keepaliveThread = threading.Thread(target=self.keepalive)
            self.keepaliveThread.setDaemon(True)
            self.keepaliveThread.start()
            self.clientLisentThread = threading.Thread(target=self.client_listen)
            self.clientLisentThread.setDaemon(True)
            self.clientLisentThread.start()
            self.logMessageRFlag = False

    def keepalive(self):
        print('Keepalive is enable...')
        while self.client.connected:
            self.client.ping()
            time.sleep(15)

    def client_listen(self):
        print('Client is listening the tcp socket...')
        while self.client.connected:
            messageContent = None
            try:
                socketRecv = self.client.recv()
                socketRecv = json.loads(socketRecv)
                if socketRecv.has_key('method') and socketRecv['method'] == 'verto.info':
                    messageContent = socketRecv['params']['msg']
                else:
                    continue
            except:
                continue
            if messageContent != None:
                messageList = list()
                for message in eval(messageContent['body']):
                    for messageItem in message:
                        messageList.append(message[messageItem])
                messageReadable = unicode(''.join(messageList),'utf-8')
                print('\nMessage from %s: %s'%(messageContent['from'], messageReadable))
                if self.logMessageRFlag:
                    self.log_received_message(messageReadable.encode('utf-8'))

    def logout(self):
        self.client.close()
        print('\n%s Logout success!' %self.username)

    def search_account(self, uid):
        searchAccount = {
            "id":str(next(self.idseq)),
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
        self.client.send(json.dumps(searchAccount))
        searchResult = json.loads(self.client.recv())
        if searchResult['result']['totalCount'] == 0:
            return [False]
        else:
            searchResultList = list()
            for user in searchResult['result']['users']:
                searchResultList.append(str(user['uid']))
            return [True,searchResultList]

    def send_textMessage(self, ruid, msg, count=1, frequency=1):
        self.msgId = self.idGen()
        print('\nSending message: ')
        for x in range(count):
            messageContent = str('.'.join([msg,str(next(self.msgId))]))
            textMessage = {
                "id":str(next(self.idseq)),
                "jsonrpc":"2.0",
                "method":"verto.info",
                "params":{
                        "describe":"online",
                        "echoParams":"request_params_send_mix_message",
                        "msg":{
                                "body":"[{\"text\": \"%s\"}]"%messageContent,
                                "from":str(self.username),
                                "style":"",
                                "to":str(ruid),
                                "type":"mixing"
                        }
                }
            }
            self.client.send(json.dumps(textMessage))
            print('>'),
            time.sleep(decimal.Decimal(1)/decimal.Decimal(frequency))
        print('\nAll message has sent.')

    def message_from_file(self, sourceFilePath):
        self.sourceFilePath = sourceFilePath
        print('\nRead lines from %s'%self.sourceFilePath)
        with open(self.sourceFilePath,'r') as sf:
            msg = sf.next()
            yield msg
            while True:
                msg = sf.next()
                yield msg

    def send_textMessage_from_file(self, ruid, sourceFilePath, frequency=1):
        nextMessage = self.message_from_file(sourceFilePath)
        print('\nSending message:')
        while True:
            try:
                messageContent = str(nextMessage.next().rstrip('\n'))
                textMessage = {
                    "id":str(next(self.idseq)),
                    "jsonrpc":"2.0",
                    "method":"verto.info",
                    "params":{
                            "describe":"online",
                            "echoParams":"request_params_send_mix_message",
                            "msg":{
                                    "body":"[{\"text\": \"%s\"}]"%messageContent,
                                    "from":str(self.username),
                                    "style":"",
                                    "to":str(ruid),
                                    "type":"mixing"
                            }
                    }
                }
                self.client.send(json.dumps(textMessage))
                print('>:%s\n'%messageContent),
                time.sleep(decimal.Decimal(1)/decimal.Decimal(frequency))
            except StopIteration:
                print('All lines in the file has send off!')
                break

    # def send_imageMessage(self):
    #     pass

    def log_received_message(self, logMessage):
        self.file = open(self.filePathTemp,'a+')
        self.file.write(logMessage+'\n')
        self.file.close()

    def log_received_message_start(self):
        fileTimestrp = time.strftime('%Y%m%d-%H%M.%S',time.localtime())
        self.file = open('received_message_%s_temp.txt'%fileTimestrp,'a+')
        self.file.close()
        self.filePathTemp = '\\'.join([os.getcwd(),'received_message_%s_temp.txt'%fileTimestrp])
        self.logMessageRFlag = True
        print('\nStart recording incoming messages. File path is %s'%self.filePathTemp)

    def log_received_message_stop(self):
        self.logMessageRFlag = False
        self.logFilePath = self.filePathTemp.replace('_temp.txt','.txt')
        os.rename(self.filePathTemp, self.logFilePath)
        print('\nStop recording incoming messages. File rename to %s'%self.logFilePath)




if __name__=='__main__':
    a = ucaClient('130.255.3.137','7001')
    a.login()
    # a.send_textMessage('7000','你好!',100,5)
    # a.send_textMessage('7000','你好!',100,7)
    a.send_textMessage_from_file('7000','F:\\python\\test\\ippbx\\UCA\\received_message_20181024-1358.56.txt',5)
    # a.log_received_message_start()
    # time.sleep(120)
    # a.log_received_message_stop()
    a.logout()
