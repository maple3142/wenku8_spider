from wenku8_spider.items import BookItem
from wenku8_spider.credentials import username, password
from json import load
import scrapy


class Wenku8Spider(scrapy.Spider):
    name = 'wenku8'
    allowed_domains = ['www.wenku8.net', 'dl.wenku8.com']
    start_urls = ['https://www.wenku8.net/modules/article/articlelist.php']
    login_form = 'https://www.wenku8.net/login.php'

    def start_requests(self):
        yield scrapy.Request(
            self.login_form,
            callback=self.parse_login_page
        )

    def parse_login_page(self, response):
        yield scrapy.FormRequest.from_response(
            response,
            formdata={'username': username, 'password': password},
            callback=self.login_success
        )

    def login_success(self, response):
        return self.start_crawl()

    def start_crawl(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse_list_page)

    def parse_list_page(self, response):
        for link in response.css('table.grid td>div b>a ::attr(href)').extract():
            yield scrapy.Request(response.urljoin(link), callback=self.parse_book_page)
        next_page = response.css(
            '.pagelink .next ::attr(href)').extract_first()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse_list_page)

    def parse_book_page(self, response):
        try:
            item = BookItem()
            url = response.request.url
            item['book_id'] = url.split('/')[-1].split('.')[0]
            item['title'] = response.css(
                '#content>div>table:nth-child(1) table tr span b ::text').extract_first()
            item['author'] = response.css(
                '#content>div>table:nth-child(1) tr:nth-child(2) td:nth-child(2) ::text').extract_first().split('：')[1]
            item['last_update'] = response.css(
                '#content>div>table:nth-child(1) tr:nth-child(2) td:nth-child(4) ::text').extract_first().split('：')[1]
            book_id = item['book_id']
            item['content_original_url'] = f'http://dl.wenku8.com/down.php?type=big5&id={book_id}'
            yield item
        except:
            pass
