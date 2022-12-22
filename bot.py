# copyright cugb19曹胜华，友友们用完star一下。
import sys
import time
# coding=utf-8
import requests
import logging
import datetime
from bs4 import BeautifulSoup
from requests.api import get
from mail import sendEmail
from getFooter import getFooterTxt


class bot_log:
    def __init__(self):
        self.log_name = str(time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())) + str('.log')
        sys.stderr = open(self.log_name, 'a')
        __stderr__ = sys.stderr
        logging.basicConfig(filename=self.log_name, filemode="w",
                            format="%(asctime)s %(name)s:%(levelname)s:%(message)s",
                            datefmt="%d-%M-%Y %H:%M:%S", level=logging.DEBUG)

    @staticmethod
    def debug(text):
        logging.debug(text)

    @staticmethod
    def error(text):
        logging.error(text)


#
log_ = bot_log()
getFooterTxt()

# jwc网址
url = 'https://jwc.cugb.edu.cn/xszq/'

strhtml = requests.get(url)
if strhtml.status_code != 200:
    log_.error('网站状态异常，为'+str(strhtml.status_code))
strhtml.encoding = strhtml.apparent_encoding

soup = BeautifulSoup(strhtml.text, 'lxml')

# 如果失效，多半是校网又tnd更新了，可以手动修改这里，里面的格式是选择器。
data = soup.select('#list_detail_box > ul > li > a')
try:
    # 获取之前的内容，这样可以判断什么是新的消息
    filepath = "out.txt"
    input = open(filepath, "r", encoding="utf-8")
    alr = []
    text = input.read().splitlines()
    if not text:
        log_.error('抓取内容出错！')
    for item in text:
        alr.append(item)
    output = open(filepath, "w", encoding="utf-8")
    newmsg = []
    bl = False
    for item in data:
        temp = item.get_text().split("\n")
        result = {
            'text': temp[1],
            'link': 'https://jwc.cugb.edu.cn/' + item.get('href'),
            'time': temp[2]
        }
        ss = str(result)
        output.write(ss + "\n")
        if ss not in alr:
            newmsg.append(result)
            bl = True
    mail = ""
    if bl:
        print("有新通知")
        cnt = 1
        for i in newmsg:
            mail += str(cnt) + ":\n"
            cnt += 1
            mail += "标题：" + i["text"] + "\n"
            mail += "时间：" + i["time"] + "\n"
            mail += "链接：" + i["link"] + "\n"
            mail += "-----------------------------------\n"

            print("标题：" + i["text"])
            print("时间：" + i["time"])
            print("链接：" + i["link"])
            print("-----------------------------------")

    else:
        print("无新通知")
        mail = "今日无通知"
    log_.debug('已捕获通知')
    sendEmail(mail, '教务处扒取bot每日汇报' + str(datetime.date.today()))
except FileNotFoundError as e:
    log_.error(e)
