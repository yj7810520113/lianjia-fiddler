# 稠州论坛 爬虫

#coding=utf-8
import requests
import random
from datetime import datetime
from bs4 import BeautifulSoup
import threading
from six.moves import urllib
import socket
import re
import time


hds=[{'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Mobile Safari/537.36'},]

baseUrl='http://bbs.cnyw.net/'

LOUCEN=1


def readurl(url):
    try:
        req = urllib.request.Request(url, headers=hds[random.randint(0, len(hds) - 1)])
        source_code = urllib.request.urlopen(req, timeout=10).read()
        # print source_code
    except Exception as e:
        print('proxys remove by exception:')
        print (e)
        return None

    return source_code

# ----------------------------------------------------------------------------------------------
# 论坛主页，用于爬取帖子地址
def parseThreadLink(soup2):
    threadList=soup2.find("div",class_="threadlist")
    for link in threadList.find_all("a"):
        print '现在爬去的链接为：'+baseUrl+link.attrs['href']
        print  baseUrl+link.attrs['href']
        content(baseUrl+link.attrs['href'])
    threadNextPage(soup2)

# 判断在读取帖子列表的时候是否要翻页
def threadNextPage(soup4):
    nextPageHref=soup4.find("div",class_="pg").find_all("a")
    # print nextPageHref
    for page in nextPageHref:
        # print page.text
        if page.text==u'\u4e0b\u4e00\u9875':
            # print baseUrl+page.attrs['href']
            # parseHtml(baseUrl+page.attrs['href'])
            parseThreadLink(BeautifulSoup(readurl(baseUrl+page.attrs['href']), 'lxml'))


# ----------------------------------------------------------------------------------------------
# 帖子内容解析
def content(url):
    global LOUCEN
    LOUCEN=1
    parseHtml(BeautifulSoup(readurl(url),'lxml'))

# 解析网页主题内容
def parseHtml(soup1):
    for div in soup1.find_all("div", class_="display pi"):
        # print div
        parseAuthorDateContent(div)
    # 判断是否需要翻页
    nextPage(soup1)


# 解析网页内容和作者、时间
def parseAuthorDateContent(bs):
    global LOUCEN
    # print bs.find("div",class_="message").prettify()
    thread={}
    # 获取作者
    author= bs.find("ul",class_="authi").li.b.text

    # 获取时间
    date= bs.find("ul",class_="authi").find("li",class_="grey rela").text

    # 获取回复、发表文章的正文
    # 去掉内容中的\s
    content= re.sub(r'\s*','',bs.find("div",class_="message").text)
    # print author
    thread.update({'author':author})
    thread.update({'date':date})
    thread.update({'content':content})
    thread.update({'loucen':LOUCEN})
    LOUCEN=LOUCEN+1
    # print thread
    # print '--------------------------------------------'


    # print bs.find("div",class_="message").get_text()

# 是否需要翻页，如果需要翻页则进行翻页操作
def nextPage(soup2):
    nextPageHref=soup2.find("div",class_="pg")
    # print nextPageHref
    if(nextPageHref!=None):
        # print nextPageHref
        for page in nextPageHref.find_all("a"):
          # print page.text
         if page.text==u'\u4e0b\u4e00\u9875':
             # print baseUrl+page.attrs['href']
             # parseHtml(baseUrl+page.attrs['href'])
             print '翻页'
             parseHtml(BeautifulSoup(readurl(baseUrl+page.attrs['href']), 'lxml'))

if __name__=="__main__":
    # soup = BeautifulSoup(readurl('http://bbs.cnyw.net/forum.php?mod=viewthread&tid=3089945&extra=page%3D1&page=1&mobile=2'), 'lxml')
    # # soup = BeautifulSoup(readurl('http://bbs.cnyw.net/forum.php?mod=viewthread&tid=3090353&extra=page%3D1&mobile=2'), 'lxml')
    # parseHtml(soup)

    soup=BeautifulSoup(readurl('http://bbs.cnyw.net/forum.php?mod=forumdisplay&fid=2&page=2&mobile=2'),'lxml')
    parseThreadLink(soup)



