import smtplib
from email.mime.text import MIMEText
def sendEmail(text:str,subject:str):
    DEBUGGING=True
    #内容头
    TEXT_HEARDER=True
    #内容尾
    TEXT_FOOTER=True
    #设置服务器所需信息
    #邮箱服务器地址(和自己发邮件的地址是不一样的)
    mail_host = 'smtp.qq.com'  
    #用户名（qq邮箱就是qq号）
    mail_user = '639289690'  
    #密码(qq邮箱为授权码，需打开smtp服务) 
    mail_pass = 'qvzkwaldhmykbbbf'   
    #邮件发送方邮箱地址
    sender = 'thesunspot_robot@qq.com'  
    #邮件接受方邮箱地址，接受数组
    receivers = ["thesunspot_robot@qq.com","3350024@163.com","1092312830@qq.com"]  
    
    if not DEBUGGING:
        mailFile='mails.txt'
        with open(mailFile,'r',encoding="utf-8") as fp:
            for line in fp.readlines():
                line=line.strip()
                if(line.startswith("###")):  continue
                if(len(line)<5):  continue
                receivers.append(line)

    if TEXT_HEARDER:
        hearderMailFile='header.txt'
        headerText=""
        with open(hearderMailFile,'r',encoding="utf-8") as fp:
            for line in fp.readlines():
                #line=line.strip()
                if not line.startswith("###"):
                    headerText=headerText+line
        if headerText != "":
            text=headerText+text

    if TEXT_FOOTER:
        footerMailFile='footer.txt'
        footerText=""
        with open(footerMailFile,'r',encoding="utf-8") as fp:
            for line in fp.readlines():
                #line=line.strip()
                if not line.startswith("###"):
                    footerText=footerText+line
        if footerText != "":
            text=text+footerText
            
    print(receivers)
    #设置email信息
    #邮件内容设置
    message = MIMEText(text,'plain','utf-8')
    #邮件主题       
    message['Subject'] =subject
    
    #发送方信息
    message['From'] = sender 
    #接受方信息     
    message['To'] = receivers[0]  
    
    #登录并发送邮件
    try:
        smtpObj = smtplib.SMTP() 
        #连接到服务器
        smtpObj.connect(mail_host,25)
        #登录到服务器
        smtpObj.login(mail_user,mail_pass) 
        #发送
        smtpObj.sendmail(
            sender,receivers,message.as_string()) 
        #退出
        smtpObj.quit() 
        print('success')
    except smtplib.SMTPException as e:
        print('error',e) #打印错误
    