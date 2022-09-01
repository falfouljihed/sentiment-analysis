#!/usr/bin/python3
import requests
import pandas as pd
import os
import string


class DataBuilder:
    """
    Build data needed from the twitter API
    """


    def __init__(self, value=""):
        """
        construct a DataBuilder object
        :param value: hashtag to search
        """
        
        self._url = "https://api.twitter.com/2/tweets/search/recent"
        self._value = value
        self.query_builder()


    def query_builder(self):
        """
        construct a twitter query to get tweets from some hashtags
        """

        temp = ""
        target = []

        if self._value == "":
            print("Put one recent series / films (to confirm press enter 2 times): ")
            while temp != "#":
                
                temp = "#" + input()
                target.append(temp)

            target.remove(target[-1])
        else:
            target.append(self._value)

        query = "("

        for entrie in target:
            query += entrie + " OR "
        
        query = query[0:-4] + ") -is:retweet lang:en -has:links"

        # impossible to have more 100 results with twitter api
        self._query_params = {'query': query, 'tweet.fields': '', 'max_results':100}


    def bearer_oauth(self, r):
        """
        Method required by bearer token authentication.
        """

        r.headers["Authorization"] = f"Bearer {bearer_token}"
        r.headers["User-Agent"] = "v2RecentSearchPython"
        return r


    def connect_to_endpoint(self):
        """
        connect to endpoint
        :return: response into json format
        """
        
        response = requests.get(self._url, auth=self.bearer_oauth, params=self._query_params)
        #print(response.status_code)
        if response.status_code != 200:
            raise Exception(response.status_code, response.text)
        return response.json()
    

    def create_db(self):
        """
        create a dataframe with tweets and prepare a empty column for the sentiment analysis
        :return: dataframe with two columns : tweet and sentiment (empty)
        """
        
        json_response = self.connect_to_endpoint()
        tweets = []

        for tweet in json_response['data']:
            tweets.append(tweet['text'].replace("\n", " "))

        db = {"tweet":tweets, "sentiment":["" for i in tweets]}
        return pd.DataFrame(db)


    def process(self, filename):
        """
        Create a database with tweets and prepare a empty column for the sentiment analysis an
        :param filename: name of the file to save the data without the extension
        """

        self.create_db().to_csv(filename + '.csv', index=False)
        print("Data is saved")

    
    def clear(self, tweet):
        """
        Remove punctuation from a tweet to count the number of words
        :param tweet: tweet to clean
        """
        
        x = tweet
        for c in string.punctuation:
            x = x.replace(c, "")
        return x


    def get_tweets_to_analyze(self):
        """
        Get tweets from api, clean them and return a list of tweets
        :return: list of tweets
        """
        
        tweets = self.create_db()
        tweets.drop(tweets[tweets["tweet"].map(lambda x: len(self.clear(x).split())) <= 3].index, inplace=True)
        return tweets['tweet'].values.tolist()


# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = 'AAAAAAAAAAAAAAAAAAAAAKc6WQEAAAAAsPBuMUXD4fFPxY7a1R4nSVeu14o%3DAn4BzJOSgXtPny8ymsrQ8xcfyWTWuhhhXMCN8fMIXiaPOmKapp'
#bearer_token = os.environ["BEARER_TOKEN"]


if __name__ == "__main__":

    dataBuilder = DataBuilder()
    dataBuilder.process("train_tweet")