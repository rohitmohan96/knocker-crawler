import re
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from knocker.items import JobItem


class KnockerSpider(CrawlSpider):
    name = "knocker"

    allowed_domains = [
        'jobopenings.infosys.com',
        'jobs.cisco.com',
        'jobs.sap.com'
    ]

    start_urls = [
        'https://jobopenings.infosys.com/viewalljobs/',
        'https://jobs.cisco.com/',
        'https://jobs.sap.com/asia-pacific/english/?locale=en_US'
    ]

    rules = (
        Rule(LinkExtractor(deny=('\.pdf',
                                 'key/.*',
                                 'topjobs',)),
             callback='parse_categories'),
    )

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.regex = re.compile(r'(consultant|manager|executive|developer|engineer)(?!.*jobs)', re.I)
        self.pageNo = r'\s*\d+\s*'

    def parse_categories(self, response):
        links = response.css('a')
        for link in links:
            if link.css('::text').re_first(self.regex):
                yield scrapy.Request(response.urljoin(link.css('::attr(href)').extract_first()),
                                     callback=self.parse_job)
            elif link.css('::text').re_first(self.pageNo):
                yield scrapy.Request(response.urljoin(link.css('::attr(href)').extract_first()),
                                     callback=self.parse_categories)

    def parse_job(self, response):
        item = JobItem()
        item['title'] = response.css('title::text').extract_first()
        item['url'] = response.url
        yield item
