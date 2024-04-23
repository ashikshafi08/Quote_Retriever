import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import json
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
import os
import argparse

class QuoteCrawler(scrapy.Spider):
    name = 'quotes'
    start_urls = ['https://quotes.toscrape.com/']

    def __init__(self, max_depth=10, max_pages=100, *args, **kwargs):
        super(QuoteCrawler, self).__init__(*args, **kwargs)
        self.max_depth = max_depth
        self.max_pages = max_pages

    def parse(self, response):
        quotes = response.css('div.quote')
        for quote in quotes:
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

def delete_existing_files():
    if os.path.exists('quotes.json'):
        os.remove('quotes.json')
    if os.path.exists('quotes_index.pkl'):
        os.remove('quotes_index.pkl')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Scrape quotes and generate index.')
    parser.add_argument('--max-depth', type=int, default=10, help='Maximum depth to crawl')
    parser.add_argument('--max-pages', type=int, default=100, help='Maximum number of pages to crawl')
    args = parser.parse_args()

    settings = get_project_settings()
    settings.update({
        'USER_AGENT': 'Mozilla/5.0 (compatible; QuoteCrawler/1.0; +http://example.com/bot)',
        'DEPTH_LIMIT': args.max_depth,
        'CLOSESPIDER_PAGECOUNT': args.max_pages,
        'FEED_FORMAT': 'json',
        'FEED_URI': 'quotes.json'
    })

    delete_existing_files()

    process = CrawlerProcess(settings)
    process.crawl(QuoteCrawler, max_depth=args.max_depth, max_pages=args.max_pages)
    process.start()

    # Once crawling is done, index the data
    if os.path.exists('quotes.json'):
        with open('quotes.json', 'r') as file:
            quotes = json.load(file)
        documents = [quote['text'] for quote in quotes]
        tfidf_vectorizer = TfidfVectorizer()
        tfidf_matrix = tfidf_vectorizer.fit_transform(documents)
        with open('quotes_index.pkl', 'wb') as f:
            pickle.dump((tfidf_vectorizer, tfidf_matrix), f)
