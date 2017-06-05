#coding=utf-8
import requests
import random
from datetime import datetime
from bs4 import BeautifulSoup
import threading
from six.moves import urllib
import socket
import time

hds=[{'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},\
    {'User-Agent':'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},\
    {'User-Agent':'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'},\
    {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0'},\
    {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36'},\
    {'User-Agent':'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},\
    {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},\
    {'User-Agent':'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0'},\
    {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'},\
    {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'},\
    {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11'},\
    {'User-Agent':'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11'},\
    {'User-Agent':'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11'}]

hd = {
    'Host': 'hz.lianjia.com',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Referer': 'http://captcha.lianjia.com/?redirect=http%3A%2F%2Fhz.lianjia.com%2Fxiaoqu%2Fxihu%2F',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
	'Cookie': 'lianjia_uuid=a4d7cdbb-7967-4206-a3dc-ac555903b59d; UM_distinctid=15c75d4af55887-0676bb9fb1900d-5393662-13c680-15c75d4af57740; select_city=330100; all-lj=c28812af28ef34a41ba2474a2b5c52c2; CNZZDATA1253492436=1257714428-1496624967-%7C1496624967; _smt_uid=5934b153.3d77668d; CNZZDATA1254525948=573701921-1496620302-%7C1496625702; CNZZDATA1255633284=812904091-1496621000-%7C1496626240; CNZZDATA1255604082=1611105927-1496622498-%7C1496622498; _gat=1; _gat_past=1; _gat_global=1; _gat_new_global=1; _ga=GA1.2.1228703738.1496625493; _gid=GA1.2.349333515.1496625493; _gat_dianpu_agent=1; lianjia_ssid=71eb1af4-ed4b-4232-8e90-5b6a71804614'

    }

def get_source_code(url):
    try:
        urlContent=readurl_by_proxy(url)
        if urlContent != 'None':
            source_code=urlContent
            print source_code
        else:
            get_source_code(url)
        # result = requests.get(url, headers=hds[random.randint(0,len(hds)-1)])
        # result = requests.get(url, headers=hd)
        # source_code = result.content
    except Exception as e:
        print '这个代理获取内容失败，准备重新获取'
        get_source_code(url)
    return source_code

def get_total_pages(url):
    source_code = get_source_code(url)
    soup = BeautifulSoup(source_code, 'lxml')
    total_pages = 0
    try:
        page_info = soup.find('div',{'class':'page-box house-lst-page-box'})
    except AttributeError as e:
        page_info = None

    if page_info == None:
        return None
    page_info_str = page_info.get('page-data').split(',')[0]  #'{"totalPage":5,"curPage":1}'
    total_pages = int(page_info_str.split(':')[1])
    return total_pages

#===========proxy ip spider, we do not use now because it is not stable===========
proxys_src = []
proxys = []

def spider_proxyip():
    try:
        for i in range(1,4):
            url='http://www.xicidaili.com/nt/' + str(i)
            req = requests.get(url,headers=hds[random.randint(0, len(hds) - 1)])
            source_code = req.content
            soup = BeautifulSoup(source_code,'lxml')
            ips = soup.findAll('tr')

            for x in range(1,len(ips)):
                ip = ips[x]
                tds = ip.findAll("td")
                proxy_host = "http://" + tds[1].contents[0]+":"+tds[2].contents[0]
                proxy_temp = {tds[5].contents[0]:proxy_host}
                proxys_src.append(proxy_temp)
    except Exception as e:
        print ("spider_proxyip exception:")
        print (e)

def test_proxyip_thread(i):
    socket.setdefaulttimeout(5)
    url = "http://www.baidu.com"
    try:
        proxy_support = urllib.request.ProxyHandler(proxys_src[i])
        opener = urllib.request.build_opener(proxy_support)
        urllib.request.install_opener(opener)
        res = urllib.request.Request(url,headers=hds[random.randint(0, len(hds) - 1)])
        source_cod = urllib.request.urlopen(res,timeout=10).read()
        if source_cod.find(b'\xe6\x82\xa8\xe6\x89\x80\xe5\x9c\xa8\xe7\x9a\x84IP') == -1 and proxys_src[i] not in proxys:
            proxys.append(proxys_src[i])
    except Exception as e:
        return
       # print(e)

def test_proxyip():
    print ("proxys before:"+str(len(proxys_src)))
    threads = []
    try:
        for i in range(len(proxys_src)):
            thread = threading.Thread(target=test_proxyip_thread, args=[i])
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()
    except Exception as e:
        print (e)
    time.sleep(20)
    print ("proxys after:" + str(len(proxys)))

def prepare_proxy():
    spider_proxyip()
    test_proxyip()
    print proxys

def readurl_by_proxy(url):
    try:
        print proxys
        tet = proxys[random.randint(0, len(proxys) - 1)]
        print ('这次请求使用的代理服务器ip为：')
        print tet
        proxy_support = urllib.request.ProxyHandler(tet)
        opener = urllib.request.build_opener(proxy_support)
        urllib.request.install_opener(opener)
        req = urllib.request.Request(url, headers=hds[random.randint(0, len(hds) - 1)])
        source_code = urllib.request.urlopen(req, timeout=10).read()
        print source_code
        if source_code.find(b'\xe6\x82\xa8\xe6\x89\x80\xe5\x9c\xa8\xe7\x9a\x84IP') != -1:
            proxys.remove(tet)
            print('proxys remove by IP traffic, new length is:' + str(len(proxys)))
            return None

    except Exception as e:
        proxys.remove(tet)
        print('proxys remove by exception:')
        print (e)
        print ('proxys new length is:' + str(len(proxys)))
        return None

    return source_code