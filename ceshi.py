# _*_ coding:utf-8 _*_ 
import urllib
import urllib2
import cookielib
import re
 
#山东大学绩点运算
class SDU:
 
    def __init__(self):
        self.loginUrl = 'http://cityjw.dlut.edu.cn:7001/XK_Login.jsp'
        self.cookies = cookielib.CookieJar()
        self.postdata = urllib.urlencode({
            'WebUserNO':'201312',
            'Password':'quzhiyu'
         })
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookies))
 
    def getPage(self):
        request  = urllib2.Request(
            url = self.loginUrl,
            data = self.postdata)
        result = self.opener.open(request)
        #打印登录内容
        print result.read().decode('gbk')
 
sdu = SDU()
sdu.getPage()

