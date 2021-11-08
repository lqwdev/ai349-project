from typing import List, Tuple
from bs4 import BeautifulSoup
import requests
import re
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import time

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


class ReutersParsedArticle:
    def __init__(self, title: str, date: str, author: int, content: str):
        self.title = title
        self.date = date
        self.author = author
        self.content = content

    def format(self) -> str:
        return f"{self.title}\n{self.date}\n{self.author}\n\n{self.content}\n"

    def __str__(self) -> str:
        return self.format()

    def __repr__(self) -> str:
        return self.format()


class ReutersCrawler:

    def __init__(self) -> None:
        pass


    def fetch_company(self, ticker: str) -> List[Tuple[str, str, str]]:
        ticker = ticker.upper()
        print(f'Fetching news articles from Reuters for ticker {ticker} ...... ')

        url = f"https://www.reuters.com/companies/{ticker}.O/news"

        options = Options()
        options.add_argument("--incognito")
        options.add_argument("--window-size=1920x1080")
        driver = webdriver.Chrome(options=options)
        driver.get(url)

        # set scroll pause time
        SCROLL_PAUSE_TIME = 0.5
        # get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")
        # keep scrolling until we've reached the bottom
        while True:
            # scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # wait to load page
            time.sleep(SCROLL_PAUSE_TIME)
            # calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        
        # parse loaded page
        parsed = BeautifulSoup(driver.page_source, 'html.parser')
        items = parsed.find_all('div', {'class': 'item'})
        # parse news items
        news = [
            (i.find('a')['href'], i.find('a').text, i.find('p').text)
            for i in items
        ]

        return news


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


def reuters_parse(content: str):
    parsed = BeautifulSoup(content, 'html.parser')
    # parse title
    title = parsed.find('h1').text
    # parse date
    date = ' '.join([span.text for span in parsed.find('time').find_all('span')[:2]])
    # parse author
    author = parsed.find('a', {'rel': 'author'}).text
    # parse contents
    regex = re.compile('.*ArticleBody__content__.*')
    content = "\n".join([p.text for p in parsed.find('div', {'class': regex}).find_all('p')])
    return ReutersParsedArticle(title, date, author, content)
