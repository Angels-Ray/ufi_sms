#!python3
import os
import sys
import re
import json
from urllib import response
import requests
from corp_init import Corpid, Agentid, Corpsecret, Touser, Media_id

unknow = []
sent = []
recv = []

#save_log(title,content)
def save_log(title,content):
    oldrss=open('sms_log',mode='a+',errors='ignore')
    oldrss.writelines([title,' - '+content,'\n'])
    oldrss.close

def wecom_app(title: str, content: str) -> None:
    """
    通过 企业微信 APP 推送消息。
    """
    if not Corpid:
        print("corp_init.py 未设置!!\n取消推送")
        return
    print("企业微信 APP 服务启动")
    wx = WeCom(Corpid, Corpsecret, Agentid)
    if not Media_id:
        # 如果没有配置 Media_id 默认就以 text 方式发送
        message = title + "\n" + content
        response = wx.send_text(message, Touser)
    else:
        response = wx.send_mpnews(title, content, Media_id, Touser)

    if response == "ok":
        print("企业微信推送成功！")
        save_log(title,content)
    else:
        print("企业微信推送失败！错误信息如下：\n", response)
    return response


class WeCom:
    def __init__(self, corpid, corpsecret, agentid):
        self.CORPID = corpid
        self.CORPSECRET = corpsecret
        self.AGENTID = agentid

    def get_access_token(self):
        url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"
        values = {
            "corpid": self.CORPID,
            "corpsecret": self.CORPSECRET,
        }
        req = requests.post(url, params=values)
        data = json.loads(req.text)
        return data["access_token"]

    def send_text(self, message, touser="@all"):
        send_url = (
            "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token="
            + self.get_access_token()
        )
        send_values = {
            "touser": touser,
            "msgtype": "text",
            "agentid": self.AGENTID,
            "text": {"content": message},
            "safe": "0",
        }
        send_msges = bytes(json.dumps(send_values), "utf-8")
        respone = requests.post(send_url, send_msges)
        respone = respone.json()
        return respone["errmsg"]

    def send_mpnews(self, title, message, media_id, touser="@all"):
        send_url = (
            "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token="
            + self.get_access_token()
        )
        send_values = {
            "touser": touser,
            "msgtype": "mpnews",
            "agentid": self.AGENTID,
            "mpnews": {
                "articles": [
                    {
                        "title": title,
                        "thumb_media_id": media_id,
                        "author": "Author",
                        "content_source_url": "",
                        "content": message.replace("\n", "<br/>"),
                        "digest": message,
                    }
                ]
            },
        }
        send_msges = bytes(json.dumps(send_values), "utf-8")
        respone = requests.post(send_url, send_msges)
        respone = respone.json()
        return respone["errmsg"]

def get_msg_num(line):
    return int(line.rstrip(' (sent)\n').rstrip(' (received)\n').rstrip(' (unknown)\n')[::-1].split('/',1)[0])

def send_msg(num):
    os.system("sudo mmcli -s "+str(num)+" --send")

def del_msg(num):
    os.system("sudo mmcli -m 0 --messaging-delete-sms="+str(num))

def scan_local_msg():
    p=os.popen('mmcli -m 0 --messaging-list-sms') 
    for line in p.readlines():
        if line.endswith(' (unknown)\n'):
            num = get_msg_num(line)
            unknow.append(num)
        if line.endswith(' (sent)\n'):
            num = get_msg_num(line)
            sent.append(num)
        if line.endswith(' (received)\n'):
            num = get_msg_num(line)
            recv.append(num)    
    print('未发送：',unknow,'已发送：',sent,'接收：',recv)

def add_msg(number,text):
    os.system("sudo mmcli -m 0 --messaging-create-sms=\"text=\'"+text+"\',number=\'+"+number+"\'\"")

def clean_sent():
    for i in sent:
        del_msg(i)
        
def clean_unknow():
    for i in unknow:
        del_msg(i)
        
def clean_recv():
    for i in recv:
        del_msg(i)

def send_all():
    for i in unknow:
        send_msg(i)

def forward_msg():
    for i in recv:
        p=os.popen('mmcli -m 0 -s '+str(i))
        #delete '\s|\t|\n|-' 删除特殊字符
        sms=re.sub('\s|\t|\n|-','',p.read())
        #get number 查找并输出
        number=sms[sms.find('number:')+7:sms.find('|text')]
        #get text 查找并输出
        text=sms[sms.find('text:')+5:sms.find('Properties|')]
        #get time 查找并输出再替换
        time=sms[sms.find('timestamp:')+10:sms.find('timestamp:')+27].replace('T',' - ')
        
        response = wecom_app(number+'\n',text+'\n\n'+time)

        if response == "ok":
            del_msg(i)
            pass

cmd = sys.argv
cmd_len = len(cmd)

if cmd[1] == 'help':
    print('随身wifi短信转发')
    print('Command: help add send clean forward')
elif cmd[1] == 'add':
    add_msg(cmd[2],cmd[3])
elif cmd[1] == 'send':
    scan_local_msg()
    send_all()
elif cmd[1] == 'clean':
    scan_local_msg()
    clean_sent()
    clean_unknow()
    clean_recv()
elif cmd[1] == 'forward':
    scan_local_msg()
    forward_msg()
else:
    print('Command error.')
