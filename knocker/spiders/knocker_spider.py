import re
import scrapy
import html2text
from scrapy.linkextractors import LinkExtractor
from scrapy_splash import SplashRequest
from knocker.items import JobItem


class KnockerSpider(scrapy.Spider):
    name = "knocker"

    allowed_domains = [
        'jobopenings.infosys.com',
        'jobs.sap.com',
        'akamaijobs.referrals.selectminds.com',
        'jobs.capgemini.com',
        'amazon.jobs'
    ]

    start_urls = [
        'https://jobopenings.infosys.com/viewalljobs/',
        'https://jobs.sap.com/asia-pacific/english/?locale=en_US',
        'https://akamaijobs.referrals.selectminds.com/',
        'https://jobs.capgemini.com/india/',
        'https://www.amazon.jobs/en/job_categories'
    ]

    splash_args = {
        'html': 1,
        'wait': 0.5,
        'render_all': 1,
    }

    job_title_pattern = re.compile(r'(consultant|manager|executive|developer|engineer)(?!.*jobs)', re.I)
    page_no_pattern = re.compile(r'\s*(\d+|next)\s*', re.I)
    location_pattern = re.compile(r'location:\s*([\w, ]*)', re.I)
    experience_pattern = re.compile(r'(\d+\s*(?:-|to)?\s*\d*\+?)\s*(?:year|yr)', re.I)

    h = html2text.HTML2Text()
    h.ignore_emphasis = True
    h.ignore_links = True
    h.ignore_tables = True
    h.ignore_images = True

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={'wait': 0.5})

    def parse(self, response):
        le = LinkExtractor(deny=('\.pdf',
                                 'key/.*',
                                 'topjobs',))
        for link in le.extract_links(response):
            yield SplashRequest(link.url, self.parse_categories, args=self.splash_args)

    def parse_categories(self, response):
        links = response.css('a')
        for link in links:
            if link.css('::text').re_first(self.job_title_pattern):
                yield SplashRequest(response.urljoin(link.css('::attr(href)').extract_first()),
                                    self.parse_job, args=self.splash_args)
            elif link.css('::text').re_first(self.page_no_pattern):
                yield SplashRequest(response.urljoin(link.css('::attr(href)').extract_first()),
                                    self.parse_categories, args=self.splash_args)

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
