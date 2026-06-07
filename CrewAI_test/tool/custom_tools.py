from crewai.tools import tool
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import json

@tool("store_poesy_to_txt")
def store_poesy_to_txt(context:str) -> str:
    """
    将编辑的文件存起来
    :param context:
    :return:
    """
    try:
        filename = "情书.txt"
        # 将文本写入txt文档中,如果文件不存在w模式下会自动创建
        with open(filename ,'w',encoding="UTF-8") as file:
            file.write(context)

            return f"文件已经写到{filename}中"
    except Exception as e:
        return f"文件写入失败，原因{e}"

class FileTools:

    @tool("Write File with content")
    def write_file(data: str):
        """这个工具用于将指定内容写入到特定路径的文件中。
输入格式应该是一个由竖线 (|) 分隔的字符串，包含两部分：文件的完整路径（例如：./lore/...）和你想要写入文件的具体内容。
        """
        try:
            global path
            path, content = data.split("|")
            path = path.replace("\n", "").replace(" ", "").replace("`", "").replace('./lore/', '')

            with open(path, "w") as f:
                f.write(content)
            return f"File written to {path}."
        except Exception:
            return "Error with the input format for the tool."


# TODO 2 此处添加自定义工具:功能发送书信到指定邮箱
@tool("send_email")
def send_email():
    """
    将编辑后的书信文本内容自动发送到指定邮箱
    """
    # 邮箱配置
    sender_email = "*********@qq.com" # 发送方任意邮箱都可以
    sender_password = "***********"       # 找到自己邮箱平台的授权码，每个人都私有的不要给别人
    receiver_email = "*********@qq.com" # 接收方任意邮箱都可以
    # 设置标题
    subject = "书信❤"
    # 获取邮件内容
    with open('情书.txt','r', encoding="utf-8") as f:
        body = f.read()
    # 设置邮件格式 MIMEMultipart代表构建复杂的邮件格式
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    try:
        # 连接smtp服务器并发送邮件
        # 创建一个安全的ssl连接
        smtp_server = smtplib.SMTP_SSL('smtp.qq.com', 465) 
        # 建立连接
        smtp_server.connect('smtp.qq.com', 465)
        # 登录邮箱(传入发送人的邮箱名和授权码)
        smtp_server.login(sender_email, sender_password)
        # 发送邮件
        smtp_server.sendmail(sender_email, receiver_email, msg.as_string())
        print("邮件发送成功!!!")
    except Exception as e:
        print("邮件发送失败!!!", e)
    finally:
        smtp_server.quit()

#UEsfGXJssSQ4Hpmf