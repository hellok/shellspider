import hashlib
import json
import os

from beautiful_soup import BeautifulSoup as bs
from scrapy.http import Request
from scrapy.spider import BaseSpider
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector

PATH = os.path.abspath(os.path.join(__file__, '../../../out/'))

class shellstormSpider(BaseSpider):
    name = 'shellstorm'
    allowed_domains = []
    start_urls = ['http://shell-storm.org/repo/CTF/']
    url=""
    def save_as_file(self, response,filename):
        sha1_response = response.url
        folder = PATH + '/' + sha1_response
        if response.url[-1]=="/":
            if not os.path.exists(folder):
                os.makedirs(folder)
        else:
            with open(folder, 'w+') as file_obj:
                file_obj.write(response.body)
    
    def parse(self, response):
        url=""
        link=[]
        if response.url[-1]=="/":
            hxs = HtmlXPathSelector(response)
            sites = hxs.select('//pre')
            for site in sites:
                title = site.select('a/text()').extract()
                link = site.select('a/@href').extract()
                desc = site.select('text()').extract()
            skip=2
            for n_link in link:
                if skip<1:
                    url=str(response.url)+str(n_link)
                    print "\nnew url:",url
                    try:
                        yield Request(url, callback=self.parse)
                    except ValueError:
                        yield Request(url, callback=self.parse)
                    self.save_as_file(response,'/index.html')
                else:
                    skip=skip-1
        else:
            self.save_as_file(response,response.url.split('/')[-1])



