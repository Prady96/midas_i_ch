from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

## twitter Credentials File
import twitter_credentials

ACCESS_TOKEN = "921699665757605890-u7obRzCk9DQ4E4p69yz9HPKoWAHEFjz"
ACCESS_TOKEN_SECRET = "Ry4jtp5HjU6XvBgt2XwgVXd2Lv2Tjf2thIVAVI8gtA6zZ"
CONSUMER_KEY = "yOeXbVkOQIvAGKKHaFGpzGpYj"
CONSUMER_SECRET = "5GxAfFncPqmL9ebCfVaaV3vRYlHBJblKy1xknbRxRGB2YzLgHd"

# Class will be used to handle data/tweets and errors
class TwitterStreamer():
    """

    """

class StdOutListener(StreamListener):

    # returning Tweets
    def on_data(self, data):
        print(data)
        return True

    def on_error(self, status):
        print(status)

if __name__ == '__main__':
    listener = StdOutListener()
    ## authentication
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    stream = Stream(auth , listener)

    ## filter tweets basis on these keyword
    stream.filter(track = ['python', 'java'])
