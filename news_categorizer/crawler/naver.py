name = "naver"
root_url = "https://news.naver.com"

news_url_patterns = [r"/main/read\.nhn\?mode=LSD&amp;mid=shm&amp;sid1=\d+&amp;oid=\d+&amp;aid=\d+"]
news_id_pattern = r"oid=(\d+)&aid=(\d+)"

news_title_selector = "#articleTitle"
news_body_selector = "#articleBodyContents"

news_urls = {"society": {"path": "/main/main.nhn?mode=LSD&mid=shm&sid1=102&",
                         "pageArgument": "page",
                         "includes": ["#section_body"]},
             "politics": {"path": "/main/main.nhn?mode=LSD&mid=shm&sid1=100&",
                          "pageArgument": "page",
                          "includes": ["#section_body"]},
             "economic": {"path": "/main/main.nhn?mode=LSD&mid=shm&sid1=101&",
                          "pageArgument": "page",
                          "includes": ["#section_body"]},
             "foreign": {"path": "/main/main.nhn?mode=LSD&mid=shm&sid1=104&",
                         "pageArgument": "page",
                         "includes": ["#section_body"]},
             "culture": {"path": "/main/main.nhn?mode=LSD&mid=shm&sid1=103&",
                         "pageArgument": "page",
                         "includes": ["#section_body"]},
             "digital": {"path": "/main/main.nhn?mode=LSD&mid=shm&sid1=105&",
                         "pageArgument": "page",
                         "includes": ["#section_body"]}}
