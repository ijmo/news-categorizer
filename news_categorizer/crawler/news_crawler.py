from html import unescape
import re
import threading
from urllib.parse import urlencode
from bs4 import BeautifulSoup

from .. import filedb


class NewsCrawler(threading.Thread):
    default_encoding = "utf-8"

    def __init__(self, http_client_for_list, http_client_for_detail, site, max_depth, stop_event, max_news_count):
        super().__init__()
        self.http_client_for_list = http_client_for_list
        self.http_client_for_detail = http_client_for_detail
        self.site = site
        self.max_depth = max_depth
        self.key_prefix = site.name + "/" + site.name + "_"
        self.stop_event = stop_event
        self.max_news_count = max_news_count
        self.news_count = 0
        self.urls = {}
        self.lock = threading.Lock()
        # self.q = FifoDiskQueue("_queue_" + site.name)

    # def push_to_queue(self, category, url, depth):
    #     self.q.push("|".join([category, url, str(depth)]).encode(self.default_encoding))
    #
    # def pop_from_queue(self):
    #     category_id_depth = self.q.pop()
    #     if category_id_depth is None:
    #         return None, None, None
    #     category, url, depth = str(category_id_depth, self.default_encoding).split("|")
    #     return category, url, int(depth)
    #
    # def push_urls(self, category, urls, depth=1):
    #     list(map(self.push_to_queue, [category] * len(urls), urls, [depth] * len(urls)))

    @staticmethod
    def fetch_html(url, http_get):
        return http_get(url)

    def parse_news_id_from_url(self, url):
        result = re.findall(self.site.news_id_pattern, url)[0]
        if type(result) == tuple:
            result = "".join(result)
        return result

    @staticmethod
    def find_urls(html_text, patterns):
        matches = [list(re.finditer(pattern, html_text)) for pattern in patterns]  # TODO
        return list(set([unescape(matches[i][j].group(0))
                         for i in range(len(matches))
                         for j in range(len(matches[i]))]))

    def format_url(self, news_id):
        return self.site.news_url_format.format(news_id=news_id)

    def get_db_key(self, news_id):
        return self.key_prefix + news_id

    def get_news_from_db(self, news_id):
        return filedb.find_by_id(self.get_db_key(news_id))

    def save_news_in_db(self, news_id, data):
        filedb.save(self.get_db_key(news_id), data)

    def get_title_body_from_soup(self, soup):
        try:
            news_title = soup.select(self.site.news_title_selector)[0].text.strip()
            news_body = soup.select(self.site.news_body_selector)[0].text.strip()
            return news_title, news_body

        except IndexError:
            print("Failed to parse news content", end=" ")
            return False

        except TypeError:
            print("Failed to save content", end=" ")
            return False

    def is_exists_as_file(self, news_id):
        return filedb.exists(self.get_db_key(news_id))

    @staticmethod
    def extract_from_soup(soup, selector):
        try:
            result = soup.select(selector)[0]
            return result
        except IndexError:
            return None

    def search_urls_in_page(self, http_get, category, details):
        path = details["path"]
        page_arg = details["pageArgument"]
        include_selectors = details["includes"]

        base_url = self.site.root_url + path

        self.urls[category] = set()

        for page_no in range(1, 3):
            if self.stop_event.wait(0.001):
                break
            url = base_url + urlencode({page_arg: page_no})
            soup = BeautifulSoup(self.fetch_html(url, http_get), 'html.parser')
            soup = self.extract_from_soup(soup, include_selectors[0])
            if not soup:
                break
            news_urls = self.find_urls(str(soup), self.site.news_url_patterns)
            if news_urls and not news_urls[0].startswith("http"):
                news_urls = [self.site.root_url + _path for _path in news_urls]
            with self.lock:
                self.urls[category] |= set(news_urls)
            print(self.site.name, category, url, len(news_urls))

            if len(self.urls[category]) >= self.max_news_count:
                break

    def fetch_news_in_category(self, http_get, category):
        urls = self.urls[category]

        for url in urls:
            if self.stop_event.wait(0.001):
                break
            news_id = self.parse_news_id_from_url(url)
            print(self.site.name, category if category else "", url, end=" ")

            if self.is_exists_as_file(news_id):
                data = self.get_news_from_db(news_id)
                print("already exists. (category -", data["category"], end=")")

                if category not in data["category"]:
                    data["category"].append(category)
                    self.save_news_in_db(news_id, data)
            else:
                html_text = self.fetch_html(url, http_get)
                soup = BeautifulSoup(html_text, 'html.parser')
                [s.extract() for s in soup('script')]

                news_title, news_body = self.get_title_body_from_soup(soup)
                data = {"url": url, "normalized": False, "category": [category], "title": news_title, "body": news_body}

                self.save_news_in_db(news_id, data)
                # This is expected to be locked, but I have not. Because it doesn't matter.
                self.news_count += 1
                print(news_title, end=" ")

            if self.news_count >= self.max_news_count:
                break

            print()

    def search_and_fetch_news(self, category, details):
        self.search_urls_in_page(self.http_client_for_list.html_getter(), category, details)
        self.fetch_news_in_category(self.http_client_for_detail.html_getter(), category)

    def start_crawling(self):
        threads = []

        for category, details in self.site.news_urls.items():
            threads.append(threading.Thread(target=self.search_and_fetch_news, args=(category, details)))

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

    def run(self):
        self.start_crawling()
