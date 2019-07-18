name = "daum"
root_url = "https://media.daum.net"

news_url_patterns = [r"https?://v\.media\.daum\.net/v/\d+"]
news_id_pattern = r"\d+$"

news_title_selector = "#cSub > div > h3"
news_body_selector = "#harmonyContainer"

news_urls = {"society": {"path": "/breakingnews/society?",
                         "pageArgument": "page",
                         "includes": ["#mArticle"]},
             "politics": {"path": "/breakingnews/politics?",
                          "pageArgument": "page",
                          "includes": ["#mArticle"]},
             "economic": {"path": "/breakingnews/economic?",
                          "pageArgument": "page",
                          "includes": ["#mArticle"]},
             "foreign": {"path": "/breakingnews/foreign?",
                         "pageArgument": "page",
                         "includes": ["#mArticle"]},
             "culture": {"path": "/breakingnews/culture?",
                         "pageArgument": "page",
                         "includes": ["#mArticle"]},
             "digital": {"path": "/breakingnews/digital?",
                         "pageArgument": "page",
                         "includes": ["#mArticle"]}}
