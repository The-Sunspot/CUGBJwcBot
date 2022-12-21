import smtplib
import json
import logging
from email.mime.text import MIMEText



def sendEmail(text: str, subject: str):
    with open("config.json", 'r') as load_f:
        cf = json.load(load_f)
    DEBUGGING = cf['DEBUGGING']
    # 内容头
    TEXT_HEARDER = cf['TEXT_HEARDER']
    # 内容尾
    TEXT_FOOTER = cf['TEXT_FOOTER']
    # 设置服务器所需信息
    # 邮箱服务器地址(和自己发邮件的地址是不一样的)
    mail_host = cf['mail_host']
    # 用户名（qq邮箱就是qq号）
    mail_user = cf['mail_user']
    # 密码(qq邮箱为授权码，需打开smtp服务)
    mail_pass = cf['mail_pass']
    # 邮件发送方邮箱地址
    sender = cf['sender']
    receivers = []
    for key, values in cf['receivers'].items():
        receivers.append(values)
    # 邮件接受方邮箱地址，接受数组

    if not DEBUGGING:
        mailFile = 'mails.txt'
        with open(mailFile, 'r', encoding="utf-8") as fp:
            for line in fp.readlines():
                line = line.strip()
                if (line.startswith("###")):  continue
                if (len(line) < 5):  continue
                receivers.append(line)

    if TEXT_HEARDER:
        hearderMailFile = 'header.txt'
        headerText = ""
        with open(hearderMailFile, 'r', encoding="utf-8") as fp:
            for line in fp.readlines():
                # line=line.strip()
                if not line.startswith("###"):
                    headerText = headerText + line
        if headerText != "":
            text = headerText + text

    if TEXT_FOOTER:
        footerMailFile = 'footer.txt'
        footerText = ""
        with open(footerMailFile, 'r', encoding="utf-8") as fp:
            for line in fp.readlines():
                # line=line.strip()
                if not line.startswith("###"):
                    footerText = footerText + line
        if footerText != "":
            text = text + footerText

    print(receivers)
    logging.debug(receivers)
    # 设置email信息
    # 邮件内容设置
    message = MIMEText(text, 'plain', 'utf-8')
    # 邮件主题
    message['Subject'] = subject

    # 发送方信息
    message['From'] = sender
    # 接受方信息
    message['To'] = receivers[0]
    # 登录并发送邮件
    try:
        smtpObj = smtplib.SMTP()
        # 连接到服务器
        smtpObj.connect(mail_host, 25)
        # 登录到服务器
        smtpObj.login(mail_user, mail_pass)
        # 发送
        smtpObj.sendmail(
            sender, receivers, message.as_string())
        # 退出
        smtpObj.quit()
        logging.debug('success')
        print('success')
    except smtplib.SMTPException as e:
        logging.error(e)
        print('error', e)  # 打印错误
