# copyright cugb19曹胜华，友友们用完star一下。

# coding=utf-8
import requests    
import datetime
from bs4 import BeautifulSoup
from requests.api import get
from mail import sendEmail

#jwc网址
url='https://jwc.cugb.edu.cn/xszq/'

strhtml=requests.get(url)
strhtml.encoding=strhtml.apparent_encoding

soup=BeautifulSoup(strhtml.text,'lxml')

#如果失效，多半是校网又tnd更新了，可以手动修改这里，里面的格式是选择器。
data = soup.select('#list_detail_box > ul > li > a')
#获取之前的内容，这样可以判断什么是新的消息
filepath="out.txt"
input=open(filepath,"r",encoding="utf-8")
alr=[]
text=input.read().splitlines()
for item in text:
    alr.append(item)


output=open(filepath,"w",encoding="utf-8")
newmsg=[]
bl=False
for item in data:
    temp=item.get_text().split("\n")
    result={
        'text':temp[1],
        'link':'https://jwc.cugb.edu.cn/'+item.get('href'),
        'time':temp[2]
    }
    ss=str(result)
    output.write(ss+"\n")
    if ss not in alr:
        newmsg.append(result)
        bl=True
mail=""
if bl :
    print("有新通知")
    cnt=1
    for i in newmsg:
        mail+= str(cnt)+":\n"
        cnt+=1
        mail+="标题："+i["text"]+"\n"
        mail+="时间："+i["time"]+"\n"
        mail+="链接："+i["link"]+"\n"
        mail+="-----------------------------------\n"

        print("标题："+i["text"])
        print("时间："+i["time"])
        print("链接："+i["link"])
        print("-----------------------------------")

else:
    print("无新通知")
    mail="今日无通知"
sendEmail(mail,'教务处扒取bot每日汇报' + str(datetime.date.today()))