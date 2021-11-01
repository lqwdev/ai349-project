from typing import List
from bs4 import BeautifulSoup
import requests
from datetime import datetime, timezone


class NewsArticle():

    def __init__(self, url: str, title: str, timestamp: datetime):
        self.url = url
        self.title = title
        self.timestamp = timestamp
    
    def __str__(self) -> str:
        return f"{self.timestamp}\n{self.title}\n{self.url}\n"


def fetch(ticker: str) -> List[NewsArticle]:
    url = f'https://www.marketwatch.com/investing/stock/{ticker}'
    print(f'Fetching MarketWatch news for {ticker} at {url} ...... ', end='')
    page = requests.get(url)
    print('[done]')

    news = BeautifulSoup(page.text, 'html.parser') \
        .find('div', attrs = { 'data-tab-pane': 'MarketWatch' }) \
        .find_all('div', class_='article__content')
    
    return [
        article for article in [
            NewsArticle(
                parse_url(item),
                parse_headline(item),
                parse_timestamp(item),
            )
            for item in news
        ]
        if article.url != '#' and article.title != '' and article.timestamp != None
    ]


def timestamp_to_datetime(ts: str) -> datetime:
    return datetime.strptime(ts, '%Y-%m-%dT%H:%M:%S').replace(tzinfo=timezone.utc)

def parse_url(item):
    urls = item.find_all(href=True)
    return urls[0]['href'] if len(urls) != 0 else None

def parse_headline(item):
    headlines = item.find_all('h3', class_='article__headline')
    return " ".join(headlines[0].text.strip().split()) if len(headlines) != 0 else None

def parse_timestamp(item):
    timestamps = item.find_all('span', class_='article__timestamp')
    if len(timestamps) == 0:
        return None
    tz = datetime.now().astimezone().tzinfo
    return timestamp_to_datetime(timestamps[0]['data-est']).replace(tzinfo=tz)
