from typing import List
import pandas as pd
import sqlite3
import os


class DB:

    def __init__(self, name: str):
        # create the databases directory if it doesn't exist
        os.makedirs('databases/', exist_ok=True)
        # open a connection to the database
        self.engine = sqlite3.connect(f'databases/{name}.db')
        # set the cursor of the class
        self.cursor = self.engine.cursor()


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
