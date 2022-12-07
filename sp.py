import scrapy
import re

from steamparse.items import GameItems


class SpSpider(scrapy.Spider):
    name = 'sp'
    allowed_domains = ['store.steampowered.com']
    # start_urls = ['https://store.steampowered.com/search/?term=russia',
    #               'https://store.steampowered.com/search/?term=runner+war',
    #               'https://store.steampowered.com/search/?term=minecraft']

    queries = ['term=russia', 'term=runner+war', 'term=minecraft']

    def start_requests(self):
        for query in self.queries:
            for p in ['&page=1', '&page=2']:
                url = 'https://store.steampowered.com/search/?' + query + p
                yield scrapy.Request(url, callback=self.parse_keyword_response)

    def parse_keyword_response(self, response):
        products = []
        for elem in response.css('a::attr(href)').getall():
            if re.search(r'app', elem):
                products.append(elem)

        for product in products:
            yield scrapy.Request(product, callback=self.parse)

    def preproc(self, items):
        return ' '.join(items).strip().replace("\t", "").replace("\n", " ").replace("\r", "").replace("p\u0443\u0431", " ").replace('All Games', '')

    def parse(self, response):
        items = GameItems()
        name = response.xpath('//div[@class = "blockbg"]/a/span[@itemprop = "name"]/text()').extract()
        category = response.xpath('//div[@class = "blockbg"]/a/text()').extract()
        reviews = response.xpath(
            '//div [@class="summary column"]/span[@class="responsive_hidden"]/text()').extract()
        rating = response.xpath(
            '//div [@class="summary column"]/span[@class="nonresponsive_hidden responsive_reviewdesc"]/text()').extract()
        release = response.xpath('//div[@class="release_date"]/div[@class="date"]/text()').extract()
        developer = response.xpath('//div[@id="developers_list"]/a/text()').extract()
        tag = response.xpath(
            '//a[@class="app_tag"]/text()').extract()
        price = response.xpath(
            '//div[@class="game_purchase_action"]/div[@class="game_purchase_action_bg"]/div[@class="game_purchase_price price"]/text()').extract()
        platforms = response.xpath('//div[@class="sysreq_tabs"]/div/text()').extract()

        items["name"] = self.preproc(name)
        items["category"] = self.preproc(category)
        items["reviews"] = self.preproc(reviews)
        items["rating"] = self.preproc(rating)
        items["release"] = self.preproc(release)
        items["developer"] = self.preproc(developer)
        items["tags"] = self.preproc(tag)
        items["price"] = self.preproc(price)
        items["platforms"] = self.preproc(platforms)

        yield items
