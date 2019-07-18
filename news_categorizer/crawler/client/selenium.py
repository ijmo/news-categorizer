import threading

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

_lock = threading.Lock()


class SeleniumHTTPClient:

    def __init__(self):
        options = Options()
        options.add_argument("--headless")
        options.add_argument('--blink-settings=imagesEnabled=false')
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    def get(self, url):
        global _lock
        with _lock:
            self.driver.get(url)
            response = self.driver.page_source
        return response
