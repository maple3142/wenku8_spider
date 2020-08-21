# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import os
import scrapy
from scrapy.utils.python import to_bytes
import hashlib
from b2sdk.v1 import B2Api
from wenku8_spider.credentials import *
from twisted.internet.defer import Deferred


class FilesUploadingPipeline:
    def __init__(self, crawler):
        self.crawler = crawler
        self.api = B2Api()
        self.api.authorize_account(
            'production', B2_ACCOUNT_ID, B2_APPLICATION_KEY)
        self.bucket = self.api.get_bucket_by_name(B2_BUCKET)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_item(self, item, spider):
        url = item['content_original_url']
        d = Deferred()
        self.crawler.engine.crawl(
            scrapy.Request(url, callback=self.receive_content(item, d)),
            spider
        )
        return d

    def receive_content(self, item, deferred):
        def helper(response):
            file_id = hashlib.sha1(
                to_bytes(response.request.url)).hexdigest()
            file_path = B2_PATH + file_id
            self.bucket.upload_bytes(
                response.body, file_name=file_path, content_type='text/plain')
            item['content_url'] = B2_ENDPOINT + B2_BUCKET + '/' + file_path
            deferred.callback(item)
        return helper
