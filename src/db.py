from typing import List, Tuple
import pandas as pd
import sqlite3
import os

from reuters import ReutersArticle


class DB:

    def __init__(self, name: str):
        # create the databases directory if it doesn't exist
        os.makedirs('databases/', exist_ok=True)
        # open a connection to the database
        self.engine = sqlite3.connect(f'databases/{name}.db')
        # set the cursor of the class
        self.cursor = self.engine.cursor()


class ReutersStructuredCompanyNews(DB):

    def __init__(self):
        super().__init__('reuters-structured-company-news')


    def create_table(self, ticker: str):
        print(f"Maybe create table for ticker {ticker} ...... ", end="")

        # create a table for each stock ticker
        stmt = f"""CREATE TABLE IF NOT EXISTS
            {ticker} (
                url          TEXT PRIMARY KEY,
                origin_url   TEXT,
                date         TEXT,
                title        TEXT,
                summary      TEXT,
                content      TEXT
            );
        """
        self.cursor.execute(stmt)
        self.engine.commit()


    def insert(self, ticker: str, article: Tuple[str, str, str, str, str, str]):
        print(f"Inserting news {article[0]} rows for ticker {ticker} ...... ", end="")

        # try to create a table for the ticker
        self.create_table(ticker)
        # ignore duplicate values
        stmt = f"""INSERT OR IGNORE INTO
            {ticker} (url, origin_url, date, title, summary, content)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        self.cursor.executemany(stmt, [article])
        self.engine.commit()
        print('[done]')


    def article_urls(self, ticker: str) -> List[str]:
        print(f"Retrieving news for ticker {ticker} ...... ", end="")
        self.create_table(ticker)
        self.cursor.execute(f"SELECT url FROM {ticker};")
        news = [i[0] for i in self.cursor.fetchall()]
        print('[done]')
        return news


class ReutersCompanyNewsDownloaded(DB):

    def __init__(self):
        super().__init__('reuters-company-news-downloaded')


    def create_table(self, ticker: str):
        print(f"Maybe create table for ticker {ticker} ...... ", end="")

        # create a table for each stock ticker
        stmt = f"""CREATE TABLE IF NOT EXISTS
            {ticker} (
                url            TEXT PRIMARY KEY,
                origin_url     TEXT,
                content        TEXT
            );
        """
        self.cursor.execute(stmt)
        self.engine.commit()


    def insert(self, ticker: str, article: Tuple[str, str, str]):
        print(f"Inserting news {article[0]} rows for ticker {ticker} ...... ", end="")

        # try to create a table for the ticker
        self.create_table(ticker)
        # ignore duplicate values
        stmt = f"""INSERT OR IGNORE INTO
            {ticker} (url, origin_url, content)
            VALUES (?, ?, ?)
        """
        self.cursor.executemany(stmt, [article])
        self.engine.commit()
        print('[done]')


    def downloaded_urls(self, ticker: str) -> List[str]:
        print(f"Retrieving news for ticker {ticker} ...... ", end="")
        self.create_table(ticker)
        self.cursor.execute(f"SELECT url FROM {ticker};")
        news = [i[0] for i in self.cursor.fetchall()]
        print('[done]')
        return news
    

    def downloaded_article(self, ticker: str, url: str) -> str:
        print(f"Retrieving content for {url} ...... ", end="")
        self.cursor.execute(f"""
            SELECT url, origin_url, content
            FROM {ticker}
            WHERE url = '{url}';
        """)
        content = self.cursor.fetchall()
        if len(content) == 0:
            print('[NOT FOUND]')
            return None
        else:
            print('[done]')
            return content[0]


class ReutersCompanyNews(DB):

    def __init__(self):
        super().__init__('reuters-company-news')


    def create_table(self, ticker: str):
        print(f"Maybe create table for ticker {ticker} ...... ", end="")

        # create a table for each stock ticker
        stmt = f"""CREATE TABLE IF NOT EXISTS
            {ticker} (
                url      TEXT PRIMARY KEY,
                title    TEXT,
                summary  TEXT
            );
        """
        self.cursor.execute(stmt)
        self.engine.commit()


    def insert(self, ticker: str, data: List[Tuple[str, str, str]]):
        print(f"Inserting {len(data)} rows for ticker {ticker} ...... ", end="")

        # try to create a table for the ticker
        self.create_table(ticker)
        # ignore duplicate values
        stmt = f"""INSERT OR IGNORE INTO
            {ticker} (url, title, summary)
            VALUES (?, ?, ?)
        """
        self.cursor.executemany(stmt, data)
        self.engine.commit()
        print('[done]')


    def news(self, ticker: str) -> List[Tuple[str, str, str]]:
        print(f"Retrieving news for ticker {ticker} ...... ", end="")
        self.create_table(ticker)
        self.cursor.execute(f"SELECT url, title, summary FROM {ticker};")
        data = self.cursor.fetchall()
        print('[done]')
        return data
    

    def summary_for_url(self, ticker: str, url: str) -> str:
        print(f"Retrieving {url} for ticker {ticker} ...... ", end="")
        self.create_table(ticker)
        self.cursor.execute(f"SELECT summary FROM {ticker} WHERE url = '{url}';")
        content = self.cursor.fetchall()
        if len(content) == 0:
            print('[NOT FOUND]')
            return None
        else:
            print('[done]')
            return content[0][0]


class ReutersNews(DB):

    def __init__(self):
        super().__init__('reuters')
        print(f"Maybe create table for Reuters news ...... ", end="")
        table1 = f"""CREATE TABLE IF NOT EXISTS
            articles (
                url      TEXT PRIMARY KEY,
                title    TEXT,
                date     TEXT,
                summary  TEXT
            );
        """
        self.cursor.execute(table1)
        self.engine.commit()
        table2 = f"""CREATE TABLE IF NOT EXISTS
            downloaded_articles (
                url      TEXT PRIMARY KEY,
                content  TEXT
            );
        """
        self.cursor.execute(table2)
        self.engine.commit()
        print('[done]')


    def insert(self, articles: List[ReutersArticle]):
        print(f"Inserting {len(articles)} articles ...... ", end="")
        # ignore duplicate values
        stmt = f"""INSERT OR IGNORE INTO articles
            (url, title, date, summary)
            VALUES (?, ?, ?, ?)
        """
        processed = [
            (e.url, e.title, e.date, e.summary)
            for e in articles
        ]
        self.cursor.executemany(stmt, processed)
        self.engine.commit()
        print('[done]')


    def articles(self) -> List[ReutersArticle]:
        print(f"Retrieving news articles ...... ", end="")
        self.cursor.execute(f"""
            SELECT url, title, date, summary
            FROM articles;
        """)
        articles = [
            ReutersArticle(i[0], i[1], i[2], i[3])
            for i in self.cursor.fetchall()
        ]
        print('[done]')
        return articles


    def insert_downloaded_article(self, url: str, content: str):
        print(f"Inserting content for {url} ...... ", end="")
        stmt = f"""INSERT OR IGNORE INTO downloaded_articles
            (url, content)
            VALUES (?, ?)
        """
        self.cursor.executemany(stmt, [(url, content)])
        self.engine.commit()
        print('[done]')


    def downloaded_articles(self) -> List[Tuple[str, str]]:
        print(f"Retrieving downloaded articles ...... ", end="")
        self.cursor.execute(f"""
            SELECT url, content
            FROM downloaded_articles;
        """)
        articles = self.cursor.fetchall()
        print('[done]')
        return articles


    def downloaded_article_urls(self) -> List[str]:
        print(f"Retrieving downloaded article urls ...... ", end="")
        self.cursor.execute(f"""
            SELECT url
            FROM downloaded_articles;
        """)
        articles_urls = [a[0] for a in self.cursor.fetchall()]
        print('[done]')
        return articles_urls


    def downloaded_article(self, url: str) -> str:
        print(f"Retrieving content for {url} ...... ", end="")
        self.cursor.execute(f"""
            SELECT content
            FROM downloaded_articles
            WHERE url = '{url}';
        """)
        content = [c[0] for c in self.cursor.fetchall()]
        if len(content) == 0:
            print('[NOT FOUND]')
            return None
        else:
            print('[done]')
            return content[0]


class DailyStock(DB):

    def __init__(self):
        super().__init__('daily')


    def create_table(self, ticker: str):
        print(f"Maybe create table for ticker {ticker} ...... ", end="")

        # create a table for each stock ticker
        stmt = f"""CREATE TABLE IF NOT EXISTS
            {ticker} (
                date    TEXT PRIMARY KEY,
                open    REAL,
                high    REAL,
                low     REAL,
                close   REAL,
                volume  REAL
            );
        """
        self.cursor.execute(stmt)
        self.engine.commit()


    def insert(self, ticker: str, data: pd.DataFrame):
        print(f"Inserting {len(data)} rows for ticker {ticker} ...... ", end="")

        # try to create a table for the ticker
        self.create_table(ticker)
        # ignore duplicate values
        stmt = f"""INSERT OR IGNORE INTO
            {ticker} (date, open, high, low, close, volume)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        # convert pd.DataFrame to a list of tuples
        processed = [
            (str(i), r['Open'], r['High'], r['Low'], r['Close'], r['Volume'])
            for i, r in data.iterrows()
        ]
        self.cursor.executemany(stmt, processed)
        self.engine.commit()
        print('[done]')


    def daily(self, ticker: str, cols: List[str] = ['Close']) -> pd.DataFrame:
        # concat the 'Date' column to the request columns
        cols = ['Date'] + cols
        fields = ', '.join(cols)

        print(f"Retrieving columns ({fields}) for ticker {ticker} ...... ", end="")
        self.cursor.execute(f"SELECT {fields} FROM {ticker};")

        # convert the data into a pd.DataFrame
        df = pd.DataFrame(self.cursor.fetchall(), columns=cols)
        # convert date strings into pd DateTimeIndex object
        df['Date'] = pd.to_datetime(df['Date'])
        # set 'Date' as the index
        df.set_index('Date', inplace=True, drop=True)

        print('[done]')
        return df
