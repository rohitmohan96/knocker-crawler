import re
import scrapy
import html2text
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from knocker.items import JobItem


class KnockerSpider(CrawlSpider):
    name = "knocker"

    allowed_domains = [
        'jobopenings.infosys.com',
        'jobs.sap.com',
        'akamaijobs.referrals.selectminds.com',
        'jobs.capgemini.com'
    ]

    start_urls = [
        'https://jobopenings.infosys.com/viewalljobs/',
        'https://jobs.sap.com/asia-pacific/english/?locale=en_US',
        'https://akamaijobs.referrals.selectminds.com/',
        'https://jobs.capgemini.com/india/'
    ]

    rules = (
        Rule(LinkExtractor(deny=('\.pdf',
                                 'key/.*',
                                 'topjobs',)),
             callback='parse_categories'),
    )

    job_title_pattern = re.compile(r'(consultant|manager|executive|developer|engineer)(?!.*jobs)', re.I)
    page_no_pattern = re.compile(r'\s*(\d+|next)\s*', re.I)
    location_pattern = re.compile(r'location:\s*([\w, ]*)', re.I)
    experience_pattern = re.compile(r'(\d+\s*(?:-|to)?\s*\d*\+?)\s*(?:year|yr)', re.I)

    h = html2text.HTML2Text()
    h.ignore_emphasis = True
    h.ignore_links = True
    h.ignore_tables = True
    h.ignore_images = True

    def parse_categories(self, response):
        links = response.css('a')
        for link in links:
            if link.css('::text').re_first(self.job_title_pattern):
                yield scrapy.Request(response.urljoin(link.css('::attr(href)').extract_first()),
                                     callback=self.parse_job)
            elif link.css('::text').re_first(self.page_no_pattern):
                yield scrapy.Request(response.urljoin(link.css('::attr(href)').extract_first()),
                                     callback=self.parse_categories)

    def parse_job(self, response):
        item = JobItem()
        item['title'] = response.css('title::text').extract_first()
        item['url'] = response.url

        text = self.h.handle(response.css('body').extract_first())

        match_location = self.location_pattern.search(text)

        if match_location is not None:
            item['location'] = match_location.group(1).strip()
        else:
            t = response.css('[class*="location"] a::text').extract()
            item['location'] = ''.join(t).strip()

        match_experience = self.experience_pattern.search(text)
        item['experience'] = match_experience.group(1).strip()

        yield item
