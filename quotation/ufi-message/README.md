# 原地址 https://gitee.com/jiu-xiao/ufi-message

# 使用转发前请补全smtp.py开头的smtp信息

    python3 msg.py add 861234567890 text
添加发送到1234567890的内容为text的短信到暂存区

    python3 msg.py send
将所有暂存区的短信发送

    python3 msg.py clean
清除本地所有短信（暂存，已发送，接收）

    python3 msg.py forward
将所有接收到的短信通过smtp邮件转发