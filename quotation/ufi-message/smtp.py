#!python3

my_sender=''
my_user=''
server_address=''
server_port=25
server_passwd=''


import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import datetime
import time

def mail(text):
    ret=True
    try:
        msg=MIMEText(text,'plain','utf-8')
        msg['From']=formataddr(["随身Wifi",my_sender])
        msg['To']=formataddr([my_user,my_user])
        msg['Subject']="短信转发 日期："+time.strftime("%Y/%m/%d/")+'时间：'+time.strftime("%H:%M:%S")

        server=smtplib.SMTP(server_address,server_port)
        server.login(my_sender,server_passwd)
        server.sendmail(my_sender,[my_user,],msg.as_string())
        server.quit()
    except Exception:
        ret=False
    return ret
