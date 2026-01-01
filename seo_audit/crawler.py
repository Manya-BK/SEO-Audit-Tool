"""
Web crawler using Scrapy for site discovery
"""
import scrapy
from scrapy.crawler import CrawlerProcess
from urllib.parse import urljoin, urlparse
import logging

logging.getLogger('scrapy').setLevel(logging.WARNING)

# Global storage for pages data (used to pass data from spider to crawler)
_pages_data_storage = []


class SEOSpider(scrapy.Spider):
    name = 'seo_spider'
    
    def __init__(self, start_url, max_pages=50, *args, **kwargs):
        super(SEOSpider, self).__init__(*args, **kwargs)
        self.start_urls = [start_url]
        self.allowed_domains = [urlparse(start_url).netloc]
        self.max_pages = max_pages
        self.visited_urls = set()
        
    def parse(self, response):
        if len(self.visited_urls) >= self.max_pages:
            return
            
        url = response.url
        if url in self.visited_urls:
            return
            
        self.visited_urls.add(url)
        
        # Extract page data
        page_data = {
            'url': url,
            'status_code': response.status,
            'title': response.css('title::text').get() or '',
            'meta_description': response.css('meta[name="description"]::attr(content)').get() or '',
            'meta_keywords': response.css('meta[name="keywords"]::attr(content)').get() or '',
            'h1_tags': response.css('h1::text').getall(),
            'h2_tags': response.css('h2::text').getall(),
            'images': [],
            'links': [],
            'canonical': response.css('link[rel="canonical"]::attr(href)').get() or '',
            'robots_meta': response.css('meta[name="robots"]::attr(content)').get() or '',
            'html_lang': response.css('html::attr(lang)').get() or '',
            'content_length': len(response.body),
        }
        
        # Extract images
        for img in response.css('img'):
            page_data['images'].append({
                'src': img.css('::attr(src)').get() or '',
                'alt': img.css('::attr(alt)').get() or '',
            })
        
        # Extract links
        for link in response.css('a'):
            href = link.css('::attr(href)').get() or ''
            if href:
                absolute_url = urljoin(response.url, href)
                page_data['links'].append({
                    'href': absolute_url,
                    'text': link.css('::text').get() or '',
                    'is_external': urlparse(absolute_url).netloc != urlparse(response.url).netloc,
                })
        
        _pages_data_storage.append(page_data)
        
        # Follow internal links
        if len(self.visited_urls) < self.max_pages:
            for link in response.css('a::attr(href)').getall():
                absolute_url = urljoin(response.url, link)
                parsed = urlparse(absolute_url)
                if parsed.netloc == self.allowed_domains[0] and absolute_url not in self.visited_urls:
                    yield response.follow(absolute_url, self.parse)


class Crawler:
    def __init__(self, start_url, max_pages=50):
        self.start_url = start_url
        self.max_pages = max_pages
        
    def crawl(self):
        """Run the crawler and return collected data"""
        global _pages_data_storage
        _pages_data_storage = []  # Reset storage
        
        process = CrawlerProcess({
            'USER_AGENT': 'SEO-Audit-Tool/1.0',
            'ROBOTSTXT_OBEY': True,
            'DOWNLOAD_DELAY': 1,
            'RANDOMIZE_DOWNLOAD_DELAY': True,
            'CONCURRENT_REQUESTS': 16,
            'LOG_LEVEL': 'ERROR',
        })
        
        process.crawl(SEOSpider, start_url=self.start_url, max_pages=self.max_pages)
        process.start()
        
        return _pages_data_storage.copy()

