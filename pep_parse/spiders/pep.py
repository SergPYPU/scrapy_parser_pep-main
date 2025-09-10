import re

import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = "pep"
    allowed_domains = ["peps.python.org"]
    start_urls = ["https://peps.python.org/"]

    def parse(self, response):
        links = response.css(
            'section#numerical-index a[href^="/pep-"]::attr(href)'
        ).getall()
        for href in links:
            yield response.follow(href, callback=self.parse_pep)

    def parse_pep(self, response):
        title = response.css("h1.page-title::text, h1::text").get() or ""
        parts = re.split(r"\s+[–—-]\s+", title, maxsplit=1)
        left = (parts[0] or "").strip()
        name = (parts[1] if len(parts) > 1 else "").strip()
        number = left.replace("PEP", "").strip()

        status = response.xpath(
            '//dt[normalize-space()="Status"]'
            "/following-sibling::dd[1]//text()"
        ).get()
        status = (status or "").strip()

        yield PepParseItem(number=number, name=name, status=status)
