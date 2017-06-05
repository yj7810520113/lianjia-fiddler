#coding=utf-8
import core
import misc
import model
import threading
import  time

def get_communitylist():
	res = []
	for community in model.Community.select():
		res.append(community.title)
	return res


def timeFunc():
    print '开始获取代理服务器了，将联通的代理服务器放入代理池中'
    misc.prepare_proxy()

if __name__=="__main__":
    # 定时器，获取可以访问的代理列表
    timeFunc()
    timer = threading.Timer(3600, timeFunc)
    timer.start()
    # time.sleep(30)
    regionlist = [u'xihu'] # only pinyin support
    model.database_init()
    core.GetCommunityByRegionlist(regionlist) # Init,scrapy celllist and insert database; could run only 1st time
    communitylist = get_communitylist() # Read celllist from database
    core.GetHouseByCommunitylist(communitylist)
    core.GetRentByCommunitylist(communitylist)
    core.GetSellByCommunitylist(communitylist)
