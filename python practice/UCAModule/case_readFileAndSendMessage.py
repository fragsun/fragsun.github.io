# -*- coding:UTF-8 -*-

from UCAModule import ucaClient,ucaCaseMethod
import time


def read_file_and_send_message(serverip, uid, ruid, path, frequency=1):
    a = ucaClient.ucaClient(serverip,uid)
    a.login()
    a.send_textMessage_from_file(ruid,path,frequency)
    a.logout()



if __name__ == '__main__':
    read_file_and_send_message('130.255.3.137', '7001', '7002', 'F:\\python\\test\\ippbx\\UCA\\received_message_20181024-1358.56.txt', 6)
