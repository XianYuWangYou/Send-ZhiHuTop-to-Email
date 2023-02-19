# -*-coding=utf-8-*-
#知乎热榜发送邮箱
#By:咸鱼网友

import smtplib
from email.mime.text import MIMEText
import time
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from pyquery import PyQuery

'''获取热榜内容，并返回标题title、简介content、链接link'''
def getinfo():    #获取热榜内容
    url = "https://www.zhihu.com/hot"
    Mycookie = {"cookie": "*"}    #请将此处cookie修改为自己的
    r = requests.get(url,headers={"user-agent" : UserAgent().random},cookies=Mycookie,timeout=30)
    r.encoding = r.apparent_encoding
    r.raise_for_status()    # 如果连接失败，弹出报错
    print("成功访问知乎热榜！")
    '''分析网页'''
    soup = BeautifulSoup(r.text,"html.parser")
    HotLists = soup.find_all("section")    # 提取热榜模块
    title,content,link = [],[],[]    # 定义内容列表
    for hotnews in HotLists:
        title.append(hotnews.h2.text)    # 获取标题添加至列表
        try:
            content.append(hotnews.p.string)    # 内容添加到内容列表
        except AttributeError:
            content.append("")
        link.append(hotnews.a["href"])    # 获取问题链接
    print("热榜分析完成，已提取内容")
    return title,content,link

'''生成标题并返回该标题'''
def getname():
    now = time.strftime("%Y-%m-%d %H:%M",time.localtime())
    filename = "知乎热榜 {}".format(now) + " TOP" + str(num)
    return filename

'''生成网页并返回html文本'''
def gethtml(num):
    html = PyQuery(filename="index.html", encoding="UTF-8")
    title,content,link = getinfo()
    filename = getname()
    html(".header h1").text(filename)   #添加标题
    article = html("body")    #添加内容
    for i in range(num):
        h3 = ' <article><h3 class="title">%s</h3>' % "{}.{}".format(i+1,title[i])
        p = '<p class="content">%s</p>' % content[i]
        a = '<a href=%s target="_blank" class="link">查看详情→</a></article>' % link[i]
        article.append("{}{}{}".format(h3,p,a))
    print("内容已填充至网页，html文本生成成功！")
    return html

'''发送文件至邮箱,括号内参数为新闻条数'''
def sendmail(num):
    html = str(PyQuery(gethtml(num)))    #获取待发送主体内容
    title = getname()    #获取邮件标题
    receiver = open("setting.txt").readlines()[1]    #读取收件人地址
    '''初始化邮箱'''
    print("邮箱初始化...")
    smtphost = ["username","password","host","port"]    #请在此处定义你的发件邮箱参数(用户名、授权码、服务器地址、端口)
    username, password, host, port = smtphost[0], smtphost[1], smtphost[2], smtphost[3]
    smtp = smtplib.SMTP_SSL(host)
    smtp.connect(host,port)
    smtp.login(username,password)
    print("已登录邮箱")
    '''装填内容'''
    msg = MIMEText(html,"html","UTF-8")
    msg["From"] = username
    msg["To"] = receiver
    msg["Subject"] = title
    print("邮件内容装填完成")
    '''发送邮件'''
    smtp.sendmail(username,receiver,msg.as_string())
    print("已发送【{}】至{}".format(title,receiver))
    smtp.quit()
    print("成功退出邮箱！")

if __name__ == '__main__':
    num = int(open("setting.txt").readlines()[3])
    sendmail(num)