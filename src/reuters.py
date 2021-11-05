from typing import List
from bs4 import BeautifulSoup
import requests


class ReutersArticle:
    def __init__(self, url: str, title: str, date: int, summary: str):
        self.url = url
        self.title = title
        self.date = date
        self.summary = summary

    def format(self) -> str:
        return f"{self.date}\n{self.title}\n{self.url}\n{self.summary}\n"

    def __str__(self) -> str:
        return self.format()

    def __repr__(self) -> str:
        return self.format()


class ReutersCrawler:

    def __init__(self) -> None:
        pass

    def fetch(self, page: int):
        def parse_url(item):
            urls = item.find_all(href=True)
            return "https://www.reuters.com/" + urls[0]['href'] if len(urls) != 0 else None

        def parse_title(item):
            headlines = item.find_all('h3', class_='story-title')
            return " ".join(headlines[0].text.strip().split()) if len(headlines) != 0 else None

        def parse_summary(item):
            summaries = [s.text for s in item.find_all('p')]
            return "\n".join(summaries)
        
        def parse_date(item):
            time = item.find_all('span', class_='timestamp')
            return time[0].text if len(time) != 0 else None

        print(f'Fetching news articles from Reuters for page {page} ...... ', end='')

        url = f'https://www.reuters.com/news/archive/marketsNews?view=page&page={page}'
        fetched = requests.get(url)
        parsed = BeautifulSoup(fetched.text, 'html.parser') \
            .find('div', class_='news-headline-list') \
            .find_all('article')

        articles = [
            ReutersArticle(
                    parse_url(item),
                    parse_title(item),
                    parse_date(item),
                    parse_summary(item),
                )
            for item in parsed
        ]
        print('[done]')
        return articles
