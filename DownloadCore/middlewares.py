# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import random
from DownloadCore.settings import USER_AGENT_LIST

class DownloadcoreSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class DownloadcoreDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)

# random user agent middleware
class RandomUserAgentMiddleware:
    def process_request(self, request, spider):
        user_agent = random.choice(USER_AGENT_LIST)
        request.headers["User-Agent"] = user_agent

# headers middleware
class HeadersMiddleware:
    def process_request(self, request, spider):
        if spider.name == "bilibili":
            headers = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                "Accept-Encoding": "gzip, deflate, br, zstd",
                "Accept-Language": "zh,zh-CN;q=0.9",
            }
            request.headers.update(headers)

# cookies middleware
class CookiesMiddleware:
    def process_request(self, request, spider):
        if spider.name == "bilibili":
            cookies = {
                "DedeUserID": "44130240",
                "DedeUserID__ckMd5": "d9d280c6c689a28a",
                "SESSDATA": "2d2536a7%2C1729043292%2Ced692%2A41CjDyJBIOML_NEHTh8ss5P1KDgVDdiOa6G63mLV1eMmoPgr43RgZ6ovZ2pNMstJgyAJISVlQydkxYdjJhNzhZNGtzUmNCTkdYYUpyTzNOM2RxdEIxd3ZUU0w5bVNXSWtLV2VyVldyd00xZHU3VVdkdDBjZVhlTzJXYW80aHVlemJrZHdZVThHM0pRIIEC",
                "bili_jct": "4c1cae5779c153a86d2e2dd0ffa2f022",
                "sid": "7zpmuwp0",
            }
            request.cookies.update(cookies)