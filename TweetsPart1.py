# for cursor/Pages & API for tweets
from tweepy import API
from tweepy import Cursor

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import pandas as pd
import numpy as np

# Credentials
ACCESS_TOKEN = ""
ACCESS_TOKEN_SECRET = ""
CONSUMER_KEY = ""
CONSUMER_SECRET = ""


class TwitterClient():

    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)
        self.twitter_user = twitter_user

    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets

    def get_friend_list(self, num_friends):
        friend_list = []
        for friend in Cursor(self.twitter_client.friends, id=self.twitter_user).items(num_friends):
            friend_list.append(friend)
        return friend_list

    def get_home_timeline_tweets(self, num_tweets):
        home_timeline_tweets = []
        for tweet in Cursor(self.twitter_client.home_timeline, id=self.twitter_user).items(num_tweets):
            home_timeline_tweets.append(tweet)
        return home_timeline_tweets

    def get_twitter_client_api(self):
        return self.twitter_client


class TwitterAuthenticator():

    def authenticate_twitter_app(self):
        auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        return auth


class TwitterStreamer():
    """
    Class for Streaming and processing Live Tweets
    """

    def __init__(self):
        self.twitter_authenticator = TwitterAuthenticator()
        pass

    def streamingTweets(self, fetched_tweets_filename, hash_tag_list):
        # Twitter Authentication & Connecting to Streaming API

        listener = TwitterListener(fetched_tweets_filename)
        # Authenticate
        auth = self.twitter_authenticator.authenticate_twitter_app()
        stream = Stream(auth, listener)

        # tracking area for key/Hashtags
        stream.filter(track=hash_tag_list)


# Class where we are printing and Handling error
class TwitterListener(StreamListener):
    """
    print received tweets to StdOut
    """

    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_data(self, data):
        try:
            print(data)
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print("Error on data %s" % str(e))
            return True

    def on_error(self, status):
        if status == 420:
            # returning false if rate limit exceeded
            return False
        print(status)


class TweetAnalyser():
    """
    Fuctioning for analysing and categorising content for tweets
    """

    def __init__(self):
        self.count = 0

    def tweets_to_date_frame(self, tweets):
        df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweets'])
        df['Date & Time'] = np.array([tweet.created_at for tweet in tweets])
        df['favorite_count'] = np.array([tweet.favorite_count for tweet in tweets])
        df['retweet_count'] = np.array([tweet.retweet_count for tweet in tweets])
        # df['images']

        try:
            if 'media' in tweets.entities:
                for image in tweets.entities['media']:
                    self.count = self.count + 1
        except:
            self.count == None

        df['image_count'] = np.array(self.count)

        return df


if __name__ == "__main__":

    twitter_client = TwitterClient()
    tweet_analyser = TweetAnalyser()
    api = twitter_client.get_twitter_client_api()

    tweets = api.user_timeline(screen_name="AamAadmiParty", count=100)

    df = tweet_analyser.tweets_to_date_frame(tweets)
    print(df.head(100))
