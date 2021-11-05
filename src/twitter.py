import tweepy

class Twitter():

    def __init__(self):
        key = "RJHK5moSffpY04onaW6wwvB1n"
        secret = "W1akrMeeIBrNSTShhfln1bzvqcsC3lEqGhzDkpK3aMM9ER0TOK"
        token = "AAAAAAAAAAAAAAAAAAAAADBlVQEAAAAA9jTY7TnNr9XVrOiGheOdEzDVL8A%3DbSnS1ClFF9Vpv0XgmdtUctTfiq6NWGdHlE9HDNq8ws3fzCXG68"
        auth = tweepy.AppAuthHandler(key, secret)
        self.api = tweepy.API(auth)


class Timeline(Twitter):

    def __init__(self, name: str):
        super().__init__()
        self.name = name
        self.tweets = []


    def load(self, year):
        print(f"Loading tweets for year: {year} ...... ", end='')

        tweets = tweepy.Cursor(
            self.api.search_full_archive,
            'dev',
            'from:MarketWatch',
            fromDate=f'{year}01010000',
            toDate=f'{year+1}01010000',
            maxResults=100,
        ).items(10000000)

        for tweet in tweets:
            self.tweets.append(tweet)

        print('[done]')
