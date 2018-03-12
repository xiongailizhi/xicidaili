# -*- coding: utf-8 -*-
import scrapy
from xici.items import XiciItem
from scrapy.http import Request

class XicidailiSpider(scrapy.Spider):
    name = 'xicidaili'
    allowed_domains = ['xicidaili,com']
    start_urls = ['http://www.xicidaili,com/']

    bash_url = 'http://www.xicidaili.com/nn/'

    # headers = {
    #     'Referer': 'http://www.xicidaili.com/nn/1'
    # }

    def start_requests(self):
        for i in range(1,2):
            url = self.bash_url+str(i)
            yield Request(url, callback=self.parse)

    def parse(self, response):
        ip_list = response.xpath('//*[@id="ip_list"]')
        trs = ip_list[0].xpath('tr')
        items = []
        for ip in trs[1:]:
            # print(ip)
            pre_item = XiciItem()
            pre_item['IP'] = ip.xpath('td[2]/text()')[0].extract()
            pre_item['PORT'] = ip.xpath('td[3]/text()')[0].extract()
            pre_item['ADDRESS'] = ip.xpath('string(td[4]/a)')[0].extract()
            pre_item['SPEED'] = ip.xpath('td[7]/div[@class="bar"]/@title')[0].extract()
            pre_item['LAST_CHECK_TIME'] = ip.xpath('td[10]/text()')[0].extract()
            # print(pre_item)
            # yield pre_item
        #
            items.append(pre_item)
            #print(items)
        return items
        # print(response.text)