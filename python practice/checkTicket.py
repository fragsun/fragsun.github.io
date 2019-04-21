# -*-coding:utf-8 -*-

import requests, json, re, time, logging
import boto3


logging.basicConfig(level=logging.DEBUG,
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filename="checkTicket.log",
    filemode='a+'
    )


# rs = requests.get("https://kyfw.12306.cn/otn/resources/js/framework/favorite_name.js")
# stations = rs.text.split('@')[1:]
# stations = [i.split('|') for i in stations]
# print(stations)


def getTicketList(date, from_station, to_station):
    s = requests.Session()
    s.headers.update({"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"})
    logging.debug('create requests session.')
    while True:
        logging.info('requests api: %s %s %s'%(date, from_station, to_station))
        r = s.get("https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=%s&leftTicketDTO.from_station=%s&leftTicketDTO.to_station=%s&purpose_codes=ADULT"%(date, from_station, to_station))
        logging.debug('requests status code is [%d]'%r.status_code)
        if r.status_code != 200:
            logging.warning('requests api failed.')
            time.sleep(120)
            continue
        elif r.status_code == 200:
            logging.info("requests api success.")
            rj = json.loads(r.text, encoding='utf-8')
            tickets = rj["data"]["result"]
            # print(tickets)
            maps = rj["data"]["map"]
            # print(maps)
            allList = list()
            gdcList = list()
            gdcBrief = list()
            for i in tickets:
                iList = i.split('|')
                if iList[11] == "Y":
                    allList.append(i)
                    if re.match(r'[DGC]\d*', iList[3]):
                        gdcList.append(i)
                        d = {
                            "车次":iList[3],
                            "始发站":iList[4],
                            "终点站":iList[5],
                            "出发":maps[iList[6]],
                            "抵达":maps[iList[7]],
                            "日期":date,
                            "出发时间":iList[8],
                            "抵达时间":iList[9],
                            "路程时间":iList[10],
                            "特等座":iList[32],
                            "一等座":iList[31],
                            "二等座":iList[14],
                            "无座":iList[26]
                            }
                        keys = list()
                        for key in d:
                            if d[key]=='' or d[key]=='无':
                                keys.append(key)
                        for key in keys:
                            d.pop(key)
                        gdcBrief.append(d)
            ticketLists = {"gdcList":gdcList, "gdcBrief":gdcBrief}
            for l in ticketLists["gdcBrief"]:
                logging.debug('G\\D\\C tripes information:')
                logging.debug(json.dumps(l, ensure_ascii=False, sort_keys=True, indent=4))
            return ticketLists


def createMessage(ticketDict, noset=False):
    messages = list()
    for t in ticketDict:
        # dji = json.dumps(t , ensure_ascii=False, sort_keys=True, indent=4)
        # print(dji)
        message = "%s %s车次现在有票，%s从%s出发，于%s抵达%s，"%(t["日期"], t["车次"], t["出发时间"], t["出发"], t["抵达时间"], t["抵达"])
        if "特等座" in t:
            message = message+"特等座余%s张，"%t["特等座"]
        if "一等座" in t:
            message = message+"一等座余%s张，"%t["一等座"]
        if "二等座" in t:
            message = message+"二等座余%s张，"%t["二等座"]
        if noset and "无座" in t:
            message = message+"无座余%s张，"%t["无座"]
        message = message.replace("有张", "多张")[:-1]+"。"
        messages.append(message)
        logging.info(message)
    return messages


def sendSMS(phones, message):
    client = boto3.client(
        "sns",
        aws_access_key_id = "your_aws_access_key_id",
        aws_secret_access_key = "your_aws_secret_access_key",
        region_name = "your_region_name"
        )

    if isinstance(phones, list):
        for phone in phones:
            phone = '+86%s'%str(phone)
            client.publish(
                PhoneNumber = phone,
                Message = message
                )
            logging.info('send notify to %s: %s'%(phone, message))

    if isinstance(phones, str) or isinstance(phones, int):
        phone = '+86%s'%str(phones)
        client.publish(
            PhoneNumber = phone,
            Message = message
            )
        logging.info('send notify to %s: %s'%(phone, message))




if __name__ == "__main__":
    date = '2019-05-01'
    from_station = 'BJP'
    to_station = 'CDW'
    phones = ["186xxxxxxxx", "199xxxxxxxx"]

    while True:
        gdcTicket = getTicketList(date, from_station, to_station)["gdcBrief"]
        if len(gdcTicket) > 0:
            logging.info('find available trpes.')
            messageList = createMessage(gdcTicket)
            for m in messageList:
                sendSMS(phones, m)
            time.sleep(3600)
        else:
            logging.info("no available tripes.")
            time.sleep(5)