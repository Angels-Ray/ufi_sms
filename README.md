# ！！！使用转发前请补全corp_init.py的信息
corp_init.py是企业微信转发的配置信息

# 基于以下项目魔改而来：
SMS_Forward https://github.com/n0raml/SMS-Forward

ufi-message https://gitee.com/jiu-xiao/ufi-message

# 依赖
- Python3
- requests
- cron

# 功能
## 1、添加发送到1234567890的内容为text的短信到暂存区
    python3 msg.py add 861234567890 text

## 2、将所有暂存区的短信发送
    python3 msg.py send

## 3、清除本地所有短信（暂存，已发送，接收）
    python3 msg.py clean

## 4、将所有接收到的短信通过企业微信转发
    python3 msg.py forward


注：

发送成功短信都会写入日志文件sms_log，如不需日志，就注释掉msg.py第38行的“save_log(title,content)”。

发送成功短信都会自动删除。若不想删除就注释掉msg.py第161行“del_msg(i)”

# 记录LOG
在当前目录下 'sms_log' 文件

# 配置定时任务
随身wifi默认的debian并没有配置cron，先安装cron

    apt install cron

配置cron

    vi /var/spool/cron/crontabs/root
填入以下内容（每分钟执行一次发送短信）

    */1 * * * *  python3 /root/app/sms/msg.py forward


