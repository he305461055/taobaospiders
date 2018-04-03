from scrapy.spiders import CrawlSpider
from scrapy.http import Request
from selenium import webdriver
import os
from scrapy.selector import Selector
import time
import taobaospider.tool as tool
import json
import re
import urllib.request
import pandas as pd

def get_data(driver):
    user_id = Selector(text=driver.page_source).xpath(u'//div[@class="shop"]/a/@data-userid').extract()
    data_nid = Selector(text=driver.page_source).xpath(u'//div[@class="shop"]/a/@data-nid').extract()
    data=list(zip(user_id,data_nid))
    return data


class Spiders(CrawlSpider):
    name='taobaospider'
    allowed_domains=['tmall.com']
    '''
    chrome_driver=chrome_driver = os.path.abspath(r"C:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe")
    os.environ["webdriver.chrome.driver"] = chrome_driver
    driver=webdriver.Chrome(chrome_driver)
    driver.maximize_window()
    url='https://s.taobao.com/search?q=%E4%BC%91%E9%97%B2%E5%A4%B9%E5%85%8B%E7%94%B7&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20170410&ie=utf8'
    driver.get(url)
    ID=[]
    for i in range(99):
        for id in get_data(driver):
            data='%s,%s' %(id[0],id[1])
            ID.append(data)
            tool.GetFile('shop_id',data,3,50000)
        driver.find_element_by_xpath('//*[@id="mainsrp-pager"]/div/div/div/ul/li[last()]/a').click()
        time.sleep(20)
    '''
    '''
    start_urls=[]
    with open('C:/Users/Administrator/Desktop/taobao/休闲男装/taobao_shop_id_0.txt','r',encoding='utf-8') as f:
        for line in f:
            start_urls.append(line.strip().replace('\n',''))
    ID=set(start_urls)
    '''
    #'''
    # start_urls=['https://rate.tmall.com/list_detail_rate.htm?itemId=10496300260&sellerId=707199638&currentPage=1&tagId=620']
    #start_urls = ['707199638,10496300260,620']
    #ID = set(start_urls)
    start_urls = []
    with open('C:/Users/Administrator/Desktop/taobao/休闲男装/taobao_tags_0.txt', 'r', encoding='utf-8') as f:
        for line in f:
            temp=[]
            temp.append(line.split('[}')[0])
            temp.append(line.split('[}')[1])
            temp.append(line.split('[}')[2])
            temp.append(line.split('[}')[-1])
            start_urls.append(','.join(temp))
    ID = set(start_urls)
    #'''
    def start_requests(self):
        while self.ID.__len__():
            id=self.ID.pop()
            seller_id=id.split(',')[0]
            item_id=id.split(',')[1]
            tag_id = id.split(',')[2]
            mark = id.split(',')[-1]
            content_url = 'http://rate.tmall.com/list_detail_rate.htm?itemId=%s&sellerId=%s&currentPage=1&tagId=%s' % ( item_id, seller_id, tag_id)
            yield Request(url=content_url,meta={'parameter': id},dont_filter=True,callback=self.parse1)#如果不加dont_filter，按照默认的会重定向被过滤掉，因为它重定向会回到原来的网址，scrapy认为是重复的url就给我过滤掉了
            #tags_url = 'https://rate.tmall.com/listTagClouds.htm?itemId=%s&isAll=true&isInner=true' % item_id
            #yield  Request(url=tags_url,meta={'ID':id} ,callback=self.parse_0)


    def parse_0(self, response):
        id = response.meta['ID']
        seller_id = id.split(',')[0]
        item_id = id.split(',')[1]
        mydata = response.body_as_unicode()
        myjson = re.findall('\"tagClouds\":(.*?),\"userTagCloudList\"', mydata)[0]
        for i in json.loads(myjson):
            tagid=i['id']
            count=i['count']
            tag=i['tag']
            posi=i['posi']
            data='%s[}%s[}%s[}%s[}%s[}%s' %(seller_id,item_id,tagid,count,tag,posi)
            print(data);
            tool.GetFile('tags',data,3,10000)
            #content_url = 'http://rate.tmall.com/list_detail_rate.htm?itemId=%s&sellerId=%s&currentPage=1&tagId=%s' % (item_id, seller_id, tagid)
            #parameter = id + ',%s' % tagid
            meta = {
                # 'dont_redirect': True,  # 禁止网页重定向
                # 'handle_httpstatus_list': [301, 302],  # 对哪些异常返回进行处理
            }
            #yield  Request(url=content_url,meta={'parameter': parameter},dont_filter=True,callback=self.parse)


    def parse1(self, response):
        mydata=response.body_as_unicode()
        try:
            mypage = re.findall('\"paginator\":(.*?),\"rateCount\"', mydata)[0]
            page=json.loads(mypage)['page']
            last_page=json.loads(mypage)['lastPage']
            myjson = re.findall('\"rateList\":(.*?),\"searchinfo\"',mydata)[0]
        except:
            print(response.url)

        for i in json.loads(myjson):
            id=i['id']
            usernick = i['displayUserNick']
            sku = i['auctionSku']
            ratecontent = i['rateContent']
            tags=re.findall('<b>(.*?)</b>',ratecontent)
            ratedate = i['rateDate']
            parameter = response.meta['parameter']
            seller_id = parameter.split(',')[0]
            item_id = parameter.split(',')[1]
            tag_id=parameter.split(',')[2]
            mark=parameter.split(',')[-1]
            data = '%s[}%s[}%s[}%s[}%s[}%s[}%s[}%s[}%s[}%s' %(seller_id,item_id,tag_id,id,usernick,sku,ratecontent.replace('<b>','').replace('</b>',''),','.join(tags),mark.replace('\n',''),ratedate)
            #print(data)
            tool.GetFile('user_content', data, 3, 10000)
        if page!=last_page:
         content_url = 'http://rate.tmall.com/list_detail_rate.htm?itemId=%s&sellerId=%s&currentPage=%d&tagId=%s' % (item_id, seller_id, int(page)+1,tag_id)
         #print(content_url)
         yield  Request(url=content_url,meta={'parameter':parameter},dont_filter=True,callback=self.parse1)