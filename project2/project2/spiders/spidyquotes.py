import scrapy


class SpidyquotesSpider(scrapy.Spider):
    name = 'spidyquotes'
    allowed_domains = ['spidyquotes.herokuapp.com']
    start_urls = ['http://spidyquotes.herokuapp.com/']

    def parse(self, response):
        pass
