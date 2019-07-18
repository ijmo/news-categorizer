import threading

from .crawler.news_crawler import NewsCrawler
from .crawler import daum
from .crawler import naver
from .crawler.client.requests import RequestsHTTPClient
from .crawler.client.selenium import SeleniumHTTPClient
from . import filedb


if __name__ == '__main__':
    MAX_COUNT = 100

    filedb.init()
    requests_client = RequestsHTTPClient()
    selenium_client = SeleniumHTTPClient()
    stop_event = threading.Event()
    crawlers = [
        NewsCrawler(selenium_client, requests_client, naver, 1, stop_event, max_news_count=MAX_COUNT),
        NewsCrawler(requests_client, requests_client, daum, 1, stop_event, max_news_count=MAX_COUNT)
    ]

    for crawler in crawlers:
        crawler.start()

    for crawler in crawlers:
        crawler.join()

    print("\n\n================\n   complete\n================\n")
