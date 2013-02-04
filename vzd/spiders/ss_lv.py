from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector

from scrapy.http import Request
from scrapy.utils.response import get_base_url
from scrapy.utils.url import urljoin_rfc

from vzd.items import VzdItem

def extract(hxs, xpath):
    data = hxs.select(xpath).extract()
    return ' '.join(data).strip()

class SsLvSpider(BaseSpider):
    name = 'ss.lv'
    allowed_domains = ['ss.lv']
    BASE_URL = 'http://www.ss.lv/lv/real-estate/plots-and-lands'
#BASE_URL = 'http://www.ss.lv/lv/real-estate/'
    start_urls = [BASE_URL]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)

        categories = hxs.select(u'//h4/a/@href').extract()
        for url in categories:
            url = urljoin_rfc(get_base_url(response), url)
            if url.startswith(self.BASE_URL):
                yield Request(url, callback=self.parse)

        if not categories:
            yield Request(response.url + 'sell/',
                    callback=self.parse_list)

    def parse_list(self, response):
        hxs = HtmlXPathSelector(response)

        for url in hxs.select(u'//a[@class="am"]/@href').extract():
            url = urljoin_rfc(get_base_url(response), url)
            yield Request(url, callback=self.parse_item)

        # paging
        for url in hxs.select(u'//a[@name="nav_id"]/@href').extract():
            url = urljoin_rfc(get_base_url(response), url)
            yield Request(url, callback=self.parse_list)

    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)

        item = VzdItem()
        item['url'] = response.url

        ad_data = hxs.select(u'//div[@id="msg_div_msg"]')
        item['note'] = extract(ad_data, u'.//tr[1]/td[@colspan="2"]//text()')
        item['city'] = extract(ad_data, u'.//td[contains(text(),"Pils\u0113ta:")]/../td[2]//text()')
        if not item['city']:
            self.log('Second city')
            item['city'] = extract(ad_data, u'.//td[contains(text(),"Pils\u0113ta, rajons:")]/../td[2]//text()')

        item['district'] = extract(ad_data, u'.//td[contains(text(),"Rajons:")]/../td[2]//text()')
        if not item['district']:
            item['district'] = extract(ad_data, u'.//td[contains(text(),"Pils\u0113ta/pagasts:")]/../td[2]//text()')

        item['village'] = extract(ad_data, u'.//td[contains(text(),"Ciems:")]/../td[2]//text()')

        item['street'] = extract(ad_data, u'.//td[contains(text(),"Iela:")]/../td[2]//text()')
        item['space'] = extract(ad_data, u'.//td[contains(text(),"Plat\u012bba:")]/../td[2]//text()')
        item['price'] = extract(ad_data, u'.//td[contains(text(),"Cena:")]/../td[2]//text()')
        item['images'] = extract(hxs, u'//td[contains(text(),"Foto:")]//a/@href')

        yield item
