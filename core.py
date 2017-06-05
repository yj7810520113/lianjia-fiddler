from bs4 import BeautifulSoup
import model
import misc
import time
import datetime
import urllib2
import logging

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
#You could modify city at here.
BASE_URL = u"https://hz.lianjia.com/"

def GetHouseByCommunitylist(communitylist):
    logging.info("Get House Infomation")
    starttime = datetime.datetime.now()
    for community in communitylist:
        try:
            get_house_percommunity(community)
            logging.info(community + "Done")
        except Exception as e:
            logging.error(e)
            logging.error(community + "Fail")
            pass
    endtime = datetime.datetime.now()
    logging.info("Run time: " + str(endtime - starttime))

def GetSellByCommunitylist(communitylist):
    logging.info("Get Sell Infomation")
    starttime = datetime.datetime.now()
    for community in communitylist:
        try:
            get_sell_percommunity(community)
            logging.info(community + "Done")
        except Exception as e:
            logging.error(e)
            logging.error(community + "Fail")
            pass
    endtime = datetime.datetime.now()
    logging.info("Run time: " + str(endtime - starttime))

def GetRentByCommunitylist(communitylist):
    logging.info("Get Rent Infomation")
    starttime = datetime.datetime.now()
    for community in communitylist:
        try:
            get_rent_percommunity(community)
            logging.info(community + "Done")
        except Exception as e:
            logging.error(e)
            logging.error(community + "Fail")
            pass
    endtime = datetime.datetime.now()
    logging.info("Run time: " + str(endtime - starttime))

def GetCommunityByRegionlist(regionlist):
    logging.info("Get Community Infomation")
    starttime = datetime.datetime.now()
    for regionname in regionlist:
        try:
            get_community_perregion(regionname)
            logging.info(regionname + "Done")
        except Exception as e:
            logging.error(e)
            logging.error(regionname + "Fail")
            pass
    endtime = datetime.datetime.now()
    logging.info("Run time: " + str(endtime - starttime))

def get_house_percommunity(communityname):
    url = BASE_URL + u"ershoufang/rs" + urllib2.quote(communityname.encode('utf8')) + "/"
    source_code = misc.get_source_code(url)
    soup = BeautifulSoup(source_code, 'lxml')

    if check_block(soup):
        return
    total_pages = misc.get_total_pages(url)
    
    if total_pages == None:
        row = model.Houseinfo.select().count()
        raise RuntimeError("Finish at %s because total_pages is None" % row)

    for page in range(total_pages):
        if page > 0:
            url_page = BASE_URL + u"ershoufang/pg%drs%s/" % (page+1, urllib2.quote(communityname.encode('utf8')))
            source_code = misc.get_source_code(url_page)
            soup = BeautifulSoup(source_code, 'lxml')

        nameList = soup.findAll("li", {"class":"clear"})
        i = 0

        for name in nameList: # per house loop
            i = i + 1
            info_dict = {}
            try:
                housetitle = name.find("div", {"class":"title"})
                info_dict.update({u'title':housetitle.get_text().strip()})
                info_dict.update({u'link':housetitle.a.get('href')})

                houseaddr = name.find("div", {"class":"address"})
                info = houseaddr.div.get_text().split('|')
                info_dict.update({u'community':info[0].strip()})
                info_dict.update({u'housetype':info[1].strip()})
                info_dict.update({u'square':info[2].strip()})
                info_dict.update({u'direction':info[3].strip()})

                housefloor = name.find("div", {"class":"flood"})
                floor_all = housefloor.div.get_text().split('-')[0].strip().split(' ')
                info_dict.update({u'floor':floor_all[0].strip()})
                info_dict.update({u'years':floor_all[-1].strip()})

                followInfo = name.find("div", {"class":"followInfo"})
                info_dict.update({u'followInfo':followInfo.get_text()})

                tax = name.find("div", {"class":"tag"})
                info_dict.update({u'taxtype':tax.get_text().strip()})

                totalPrice = name.find("div", {"class":"totalPrice"})
                info_dict.update({u'totalPrice':int(totalPrice.span.get_text())})

                unitPrice = name.find("div", {"class":"unitPrice"})
                info_dict.update({u'unitPrice':int(unitPrice.get('data-price'))})
                info_dict.update({u'houseID':unitPrice.get('data-hid')})
            except:
                continue
            # houseinfo insert into mysql
            model.Houseinfo.insert(**info_dict).upsert().execute()
            model.Hisprice.insert(houseID=info_dict['houseID'], totalPrice=info_dict['totalPrice']).upsert().execute()

        time.sleep(1)

def get_sell_percommunity(communityname):
    url = BASE_URL + u"chengjiao/rs" + urllib2.quote(communityname.encode('utf8')) + "/"
    source_code = misc.get_source_code(url)
    soup = BeautifulSoup(source_code, 'lxml')

    if check_block(soup):
        return
    total_pages = misc.get_total_pages(url)
    
    if total_pages == None:
        row = model.Sellinfo.select().count()
        raise RuntimeError("Finish at %s because total_pages is None" % row)

    for page in range(total_pages):
        if page > 0:
            url_page = BASE_URL + u"chengjiao/pg%drs%s/" % (page+1, urllib2.quote(communityname.encode('utf8')))
            source_code = misc.get_source_code(url_page)
            soup = BeautifulSoup(source_code, 'lxml')
        i = 0
        for ultag in soup.findAll("ul", {"class":"listContent"}):
            for name in ultag.find_all('li'):
                i = i + 1
                info_dict = {}
                try:
                    housetitle = name.find("div", {"class":"title"})
                    info_dict.update({u'title':housetitle.get_text().strip()})
                    info_dict.update({u'link':housetitle.a.get('href')})
                    houseID = int(housetitle.a.get('href').split("/")[-1].split(".")[0])
                    info_dict.update({u'houseID':houseID})

                    house = housetitle.get_text().strip().split(' ')
                    info_dict.update({u'community':house[0]})
                    info_dict.update({u'housetype':house[1]})
                    info_dict.update({u'square':house[2]})

                    houseinfo = name.find("div", {"class":"houseInfo"})
                    info = houseinfo.get_text().split('|')
                    info_dict.update({u'direction':info[0]})
                    info_dict.update({u'status':info[1]})

                    housefloor = name.find("div", {"class":"positionInfo"})
                    floor_all = housefloor.get_text().strip().split(' ')
                    info_dict.update({u'floor':floor_all[0]})
                    info_dict.update({u'years':floor_all[-1]})

                    followInfo = name.find("div", {"class":"source"})
                    info_dict.update({u'source':followInfo.get_text()})

                    totalPrice = name.find("div", {"class":"totalPrice"})
                    info_dict.update({u'totalPrice':int(totalPrice.span.get_text())})

                    unitPrice = name.find("div", {"class":"unitPrice"})
                    info_dict.update({u'unitPrice':int(unitPrice.span.get_text())})

                    dealDate= name.find("div", {"class":"dealDate"})
                    info_dict.update({u'dealdate':dealDate.get_text()})
                except:
                    continue
                # Sellinfo insert into mysql
                model.Sellinfo.insert(**info_dict).upsert().execute()

        time.sleep(1)

def get_community_perregion(regionname):
    url = BASE_URL + u"xiaoqu/" + regionname +"/"
    print url;
    source_code = misc.get_source_code(url)
    print source_code
    soup = BeautifulSoup(source_code, 'lxml')
    print soup.get_text()
    if check_block(soup):
        return
    total_pages = misc.get_total_pages(url)
    
    if total_pages == None:
        row = model.Community.select().count()
        raise RuntimeError("Finish at %s because total_pages is None" % row)

    for page in range(total_pages):
        if page > 0:
            url_page = BASE_URL + u"xiaoqu/" + regionname +"/pg%d/" % (page+1,)
            source_code = misc.get_source_code(url_page)
            soup = BeautifulSoup(source_code, 'lxml')

        nameList = soup.findAll("li", {"class":"clear"})
        i = 0

        for name in nameList: # Per house loop
            i = i + 1
            info_dict = {}
            try:
                communitytitle = name.find("div", {"class":"title"})
                print communitytitle.get_text();
                info_dict.update({u'title':communitytitle.get_text().strip('\n')})
                info_dict.update({u'link':communitytitle.a.get('href')})

                district = name.find("a", {"class":"district"})
                info_dict.update({u'district':district.get_text()})
                bizcircle = name.find("a", {"class":"bizcircle"})
                info_dict.update({u'bizcircle':bizcircle.get_text()})

                tagList = name.find("div", {"class":"tagList"})
                info_dict.update({u'tagList':tagList.get_text().strip('\n')})
            except:
                continue
            # communityinfo insert into mysql
            model.Community.insert(**info_dict).upsert().execute()

        time.sleep(1)

def get_rent_percommunity(communityname):
    url = BASE_URL + u"zufang/rs" + urllib2.quote(communityname.encode('utf8')) + "/"
    source_code = misc.get_source_code(url)
    soup = BeautifulSoup(source_code, 'lxml')

    if check_block(soup):
        return
    total_pages = misc.get_total_pages(url)

    if total_pages == None:
        row = model.Rentinfo.select().count()
        raise RuntimeError("Finish at %s because total_pages is None" % row)

    for page in range(total_pages):
        if page > 0:
            url_page = BASE_URL + u"rent/pg%drs%s/" % (page+1, urllib2.quote(communityname.encode('utf8')))
            source_code = misc.get_source_code(url_page)
            soup = BeautifulSoup(source_code, 'lxml')
        i = 0
        for ultag in soup.findAll("ul", {"class":"house-lst"}):
            for name in ultag.find_all('li'):
                i = i + 1
                info_dict = {}
                try:
                    housetitle = name.find("div", {"class":"info-panel"})
                    info_dict.update({u'title':housetitle.get_text().strip()})
                    info_dict.update({u'link':housetitle.a.get('href')})
                    houseID = int(housetitle.a.get('href').split("/")[-1].split(".")[0])
                    info_dict.update({u'houseID':houseID})

                    region = name.find("span", {"class":"region"})
                    info_dict.update({u'region':region.get_text().strip()})

                    zone = name.find("span", {"class":"zone"})
                    info_dict.update({u'zone':zone.get_text().strip()})

                    meters = name.find("span", {"class":"meters"})
                    info_dict.update({u'meters':meters.get_text().strip()})

                    other = name.find("div", {"class":"con"})
                    info_dict.update({u'other':other.get_text().strip()})

                    subway = name.find("span", {"class":"fang-subway-ex"})
                    info_dict.update({u'subway':subway.span.get_text().strip()})

                    decoration = name.find("span", {"class":"decoration-ex"})
                    info_dict.update({u'decoration':decoration.span.get_text().strip()})

                    heating = name.find("span", {"class":"heating-ex"})
                    info_dict.update({u'heating':heating.span.get_text().strip()})

                    price = name.find("div", {"class":"price"})
                    info_dict.update({u'price':int(price.span.get_text().strip())})

                    pricepre = name.find("div", {"class":"price-pre"})
                    info_dict.update({u'pricepre':pricepre.get_text().strip()})
                except:
                    continue
                # Rentinfo insert into mysql
                model.Rentinfo.insert(**info_dict).upsert().execute()

        time.sleep(1)

def check_block(soup):
    if soup.title.string == "414 Request-URI Too Large":
        logging.error("Lianjia block your ip, please verify captcha manually at lianjia.com")
        return True
    return False
