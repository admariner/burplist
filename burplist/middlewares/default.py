# Define here the models for your spider middleware  # Unused
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from typing import Iterator, Union

from scrapy import signals
from scrapy.http import Request, Response

# useful for handling different item types with a single interface
# from itemadapter import is_item, ItemAdapter


class BurplistSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler) -> 'BurplistSpiderMiddleware':
        # This method is used by Scrapy to create your spiders.
        middleware = cls()
        crawler.signals.connect(middleware.spider_opened, signal=signals.spider_opened)
        return middleware

    def process_spider_input(self, response, spider) -> None:
        del response, spider  # Unused
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        # return None

    def process_spider_output(self, response, result, spider) -> Iterator[Request]:
        del response, spider  # Unused
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider) -> None:
        del response, exception, spider  # Unused
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        # return None

    def process_start_requests(self, start_requests, spider) -> Iterator[Request]:
        del spider  # Unused
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for request in start_requests:
            yield request

    def spider_opened(self, spider) -> None:
        spider.logger.info('Spider opened: %s' % spider.name)


class BurplistDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler) -> 'BurplistDownloaderMiddleware':
        # This method is used by Scrapy to create your spiders.
        middleware = cls()
        crawler.signals.connect(middleware.spider_opened, signal=signals.spider_opened)
        return middleware

    def process_request(self, request, spider) -> None:
        del request, spider  # Unused
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called

    def process_response(self, request, response, spider) -> Union[Request, Response]:
        del request, spider  # Unused
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider) -> None:
        del request, exception, spider  # Unused
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain

    def spider_opened(self, spider) -> None:
        spider.logger.info('Spider opened: %s' % spider.name)
