from scrapy import signals


class PepParseSpiderMiddleware:
    """Spider middleware (no-op)."""

    @classmethod
    def from_crawler(cls, crawler):
        inst = cls()
        crawler.signals.connect(
            inst.spider_opened, signal=signals.spider_opened
        )
        return inst

    def process_spider_input(self, response, spider):
        return None

    def process_spider_output(self, response, result, spider):
        for item in result:
            yield item

    def process_spider_exception(self, response, exception, spider):
        pass

    def process_start_requests(self, start_requests, spider):
        for req in start_requests:
            yield req

    def spider_opened(self, spider):
        spider.logger.info(f"Spider opened: {spider.name}")


class PepParseDownloaderMiddleware:
    """Downloader middleware (no-op)."""

    @classmethod
    def from_crawler(cls, crawler):
        inst = cls()
        crawler.signals.connect(
            inst.spider_opened, signal=signals.spider_opened
        )
        return inst

    def process_request(self, request, spider):
        return None

    def process_response(self, request, response, spider):
        return response

    def process_exception(self, request, exception, spider):
        pass

    def spider_opened(self, spider):
        spider.logger.info(f"Spider opened: {spider.name}")
