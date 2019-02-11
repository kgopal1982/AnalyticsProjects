#pull crime data
# Import modules
#references>>>
#https://galeascience.wordpress.com/2016/03/18/collecting-twitter-data-with-python/
#https://github.com/agalea91/twitter_search/blob/master/twitter_search.py

from tweepy.streaming import StreamListener
from tweepy import Stream
import tweepy
from tweepy import OAuthHandler
import datetime as dt
import time
import json


def load_api():
    ''' Function that loads the twitter API after authorizing the user. '''

    consumer_key = 'Kr6euZvC2WrRPB8gZTnMtmCDJ'
    consumer_secret = 'fqzEkQZk4Et6jJe2VV2KMkdepIWqr8b3BPCIleXDY47fsc2PpB'
    access_token = '2538332490-iYOH0lWlPy6LDm7VXa5dsaaDXJRKKcNlFRxm1CY'
    access_secret = 'YDdaWVYJdFKyttLc5sG9K8iSS7bQrqSXSVR2qyh7IcTAw'
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    # load the twitter API via tweepy
    return tweepy.API(auth)

def tweet_search(api, query, max_tweets, geocode):
    ''' Function that takes in a search string 'query', the maximum
        number of tweets 'max_tweets' It returns a list of tweepy.models.Status objects. '''

    searched_tweets = []
    while len(searched_tweets) < max_tweets:
        remaining_tweets = max_tweets - len(searched_tweets)
        try:
            new_tweets = api.search(q=query, count=remaining_tweets)
            print('found',len(new_tweets),'tweets')
            if not new_tweets:
                print('no tweets found')
                break
            searched_tweets.extend(new_tweets)
        except tweepy.TweepError:
            print('exception raised, waiting 15 minutes')
            print('(until:', dt.datetime.now()+dt.timedelta(minutes=15), ')')
            time.sleep(15*60)
            break # stop the loop
    return searched_tweets

def write_tweets(tweets, filename):
    ''' Function that appends tweets to a file. '''

    with open(filename, 'a') as f:
        for tweet in tweets:
            json.dump(tweet._json, f)
            f.write('\n')

#class StdOutListener(StreamListener):
#    """ A listener handles tweets that are received from the stream.
#    This is a basic listener that just prints received tweets to stdout.
#    """
#    def on_status(self, status):
#        print(status.text)
#        return True
#
#    def on_error(self, status_code):
#        if status_code == 420:
#            return False
        
def main():
    ''' search variables: '''
#    search_phrases = ['Robbery', 'Kidnap', 
#                     'Shooting', 'Arrest',
#                     'Homicide', 'Narcotics',
#                     'Marijuana']
    search_phrases = ['Marijuana']
    #time_limit = 1.5        # runtime limit in hours
    max_tweets = 500        # number of tweets per search (will be iterated over) - maximum is 100
    Chicago = '41.881832, -87.623177, 320km'
    #Chicago = '39.8,-95.583068847656,2500km'
    json_file = "C:\\datasets\\crimedata\\crimes_tweets.json"
    
    # authorize and load the twitter API
    api = load_api()
     
    # collect tweets
    tweets = tweet_search(api, search_phrases, max_tweets,geocode=Chicago)
    #tweets = tweet_search(api, search_phrases, max_tweets)
    write_tweets(tweets, json_file)
    
if __name__ == "__main__":
    main()
