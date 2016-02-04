# -*- coding:utf-8 -*-
import urllib
import urllib2
import re

class Tool:
    removeImg = re.compile('<img.*?>| {7}|')
    removeAddr = re.compile('<a.*?>|</a>')
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    replaceTD= re.compile('<td>')
    replacePara = re.compile('<p.*?>')
    replaceBR = re.compile('<br><br>|<br>')
    removeExtraTag = re.compile('<.*?>')
    def replace(self,x):
        x = re.sub(self.removeImg,"",x)
        x = re.sub(self.removeAddr,"",x)
        x = re.sub(self.replaceLine,"\n",x)
        x = re.sub(self.replaceTD,"\t",x)
        x = re.sub(self.replacePara,"\n    ",x)
        x = re.sub(self.replaceBR,"\n",x)
        x = re.sub(self.removeExtraTag,"",x)
        return x.strip()

class BDTB:

    def __init__(self,baseUrl,seeLZ):
        self.baseURL = baseUrl
        self.seeLZ = '?see_lz='+str(seeLZ)
        self.tool  = Tool()

    def getPage(self,pageNum):
        try:
            url = self.baseURL+ self.seeLZ + '&pn=' + str(pageNum)
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
#            print response.read()
            return response.read().decode('utf-8')
        except urllib2.URLError, e:
            if hasattr(e,"reason"):
                print u"连接百度贴吧失败,错误原因",e.reason
                return None

    def getTitle(self,page):
        pattern = re.compile('<h3 class="core_title_txt.*?>(.*?)</h3>',re.S)
        result  = re.search(pattern,page)
        if result:
            print result.group(1).strip()
        else:
            print "erorr getting title"

    def getPageNum(self,page):
        pattern = re.compile('<li class="l_reply_num.*?</span>.*?<span.*?>(.*?)</span>',re.S)
        result  = re.search(pattern,page)
        if result:
            return result.group(1).strip()
        else:
            print "error getting pagenum"

    def getContent(self,page):
        pattern = re.compile('<div id="post_content.*?>(.*?)</div>',re.S)
        items   = re.findall(pattern,page)
        for item in items:
            print self.tool.replace(item)



#baseURL = 'http://tieba.baidu.com/p/3138733512'
baseURL = 'http://tieba.baidu.com/p/4309419688'
bdtb = BDTB(baseURL,1)
indexPage=bdtb.getPage(1)
#print type(indexPage)
bdtb.getTitle(indexPage)
PN=int(bdtb.getPageNum(indexPage))
for current_page in range(1,(PN+1)):
    print "current page num is "+ str(current_page)
    print "----------------------------------------------------------------------------------------"
    indexPage = bdtb.getPage(current_page)
    bdtb.getContent(indexPage)
