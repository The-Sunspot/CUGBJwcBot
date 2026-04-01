# copyright cugb19曹胜华，友友们用完star一下。
import sys
import time
import requests
import logging
import datetime
from bs4 import BeautifulSoup


class bot_log:
    def __init__(self):
        # 以时间命名日志文件
        self.log_name = str(time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())) + str('.log')
        sys.stderr = open(self.log_name, 'a')
        logging.basicConfig(filename=self.log_name, filemode="w",
                            format="%(asctime)s %(name)s:%(levelname)s:%(message)s",
                            datefmt="%d-%M-%Y %H:%M:%S", level=logging.DEBUG)

    @staticmethod
    def debug(text):
        logging.debug(text)

    @staticmethod
    def error(text):
        logging.error(text)


# 初始化日志对象
log_ = bot_log()


def get_jwc_notifications():
    """
    核心爬虫逻辑：访问教务处并对比 out.txt 判断是否有新通知
    返回: (has_new: bool, mail_content: str)
    """
    url = 'https://jwc.cugb.edu.cn/xszq/'

    try:
        strhtml = requests.get(url, timeout=10)
        if strhtml.status_code != 200:
            log_.error('网站状态异常，为' + str(strhtml.status_code))
            return False, "网站连接失败"

        strhtml.encoding = strhtml.apparent_encoding
        soup = BeautifulSoup(strhtml.text, 'lxml')

        # 使用选择器提取通知列表
        data = soup.select('#list_detail_box > ul > li > a')

        # 读取历史记录
        filepath = "out.txt"
        alr = []
        try:
            with open(filepath, "r", encoding="utf-8") as f_input:
                alr = f_input.read().splitlines()
        except FileNotFoundError:
            log_.debug("未找到out.txt，将创建新文件")

        newmessage = []
        bl = False

        # 写入当前抓取到的所有内容，并筛选出新通知
        with open(filepath, "w", encoding="utf-8") as f_output:
            for item in data:
                temp = item.get_text().split("\n")
                result = {
                    'text': temp[1],
                    'link': 'https://jwc.cugb.edu.cn/' + item.get('href'),
                    'time': temp[2]
                }
                ss = str(result)
                f_output.write(ss + "\n")
                if ss not in alr:
                    newmessage.append(result)
                    bl = True

        # 构建邮件文本内容
        mail_text = ""
        if bl:
            cnt = 1
            for i in newmessage:
                mail_text += f"{cnt}:\n标题：{i['text']}\n时间：{i['time']}\n链接：{i['link']}\n"
                mail_text += "-----------------------------------\n"
                cnt += 1
        else:
            mail_text = "今日无新通知。"

        return bl, mail_text

    except Exception as e:
        log_.error(f"爬取过程发生错误: {e}")
        return False, f"错误详情: {e}"