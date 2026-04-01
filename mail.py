import smtplib
import json
import logging
from email.mime.text import MIMEText


def sendEmail(text: str, subject: str):
    #加载配置（保留邮箱服务器信息）
    with open("config.json", 'r') as load_f:
        cf = json.load(load_f)

    mail_host = cf['mail_host']
    mail_user = cf['mail_user']
    mail_pass = cf['mail_pass']
    sender = cf['sender']

    # 2. 获取接收者列表
    receivers = []
    for key, values in cf['receivers'].items():
        receivers.append(values)

    #这里删除了原来的 header 和 footer 读取逻辑，个人感觉纯属多余，我一个爬虫软件根本不需要通报考研和四六级时间
    mailFile = 'mails.txt'
    try:
        with open(mailFile, 'r', encoding="utf-8") as fp:
            for line in fp.readlines():
                line = line.strip()
                if line.startswith("###") or len(line) < 5:
                    continue
                receivers.append(line)
    except FileNotFoundError:
        print("提醒：未找到 mails.txt，仅发送给 config.json 中的用户")
    # 现在的 text 就是直接传进来的教务处通知内容

    #设置邮件信息
    message = MIMEText(text, 'plain', 'utf-8')
    message['Subject'] = subject
    message['From'] = sender
    message['To'] = receivers[0]

    #登录并发送
    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        smtpObj.quit()
        print('邮件发送成功')
    except smtplib.SMTPException as e:
        print('邮件发送失败', e)