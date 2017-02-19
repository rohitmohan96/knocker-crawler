import re
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from knocker.items import JobItem


class KnockerSpider(CrawlSpider):
    name = "knocker"
    allowed_domains = ['jobopenings.infosys.com', 'jobs.cisco.com']
    start_urls = ['https://jobopenings.infosys.com/viewalljobs/', 'https://jobs.cisco.com/']

    rules = (
        Rule(LinkExtractor(deny=('\.pdf',)), callback='parse_categories'),
    )

    def parse_categories(self, response):
        regex = re.compile(r'consultant|manager|executive|developer|engineer', re.I)
        links = response.css('a')
        for link in links:
            if link.css('::text').re_first(regex):
                yield scrapy.Request(response.urljoin(link.css('::attr(href)').extract_first()),
                                     callback=self.parse_job)

    def parse_job(self, response):
        item = JobItem()
        item['title'] = response.css('title::text').extract_first()
        item['url'] = response.url
        yield item
