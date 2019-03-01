#pull crime data
# Import modules
#references>>>
#https://galeascience.wordpress.com/2016/03/18/collecting-twitter-data-with-python/
#https://github.com/agalea91/twitter_search/blob/master/twitter_search.py

#from tweepy.streaming import StreamListener
#from tweepy import Stream
import tweepy
from tweepy import OAuthHandler
import datetime as dt
import time
import json
import pandas as pd
import os
from datetime import datetime


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

            
def create_directory():
    #create the directoty where we will store the json
    today = datetime.now()
    base_dir = "C:/DataSets/crimedata/tweetAnalysis"

    full_dir = os.path.join(base_dir, today.strftime('%Y{0}%m{0}%d').format(os.path.sep))
    
    if not os.path.exists(full_dir):
        os.makedirs(full_dir)
    
    return full_dir

    
def store_process_csv(json_file):
    #load the json file   
    df_orig = pd.read_json(json_file, lines=True)
    #save into csv
    full_dir = create_directory()
    df_orig.to_csv(os.path.join(full_dir,r'original_crimes_tweets.csv'))
    #df_orig.to_csv("C:\\DataSets\\crimedata\\tweetAnalysis\\2019\\03\\01\\original_crimes_tweets.csv")
    #print(df_orig.head())
    df = df_orig.copy(deep = True)

    #keep the columns which are of interest
    df = df[['created_at','id','id_str','lang','retweet_count','retweeted','source','text','user']]
    
    #check for duplicates
    df.duplicated('id')
    
    #it shows there are duplicates
    #drop the duplicates
    df.drop_duplicates(subset = "id", keep = 'first', inplace = True)
    df_filtered = df[df['lang']=="en"]
    #save into csv
    df_filtered.to_csv(os.path.join(full_dir,r'modified_crimes_tweets.csv'))
    #df.to_csv("C:\\DataSets\\crimedata\\tweetAnalysis\\2019\\03\\01\\modified_crimes_tweets.csv")

def main():
    #create the folders based on date
    full_dir = create_directory()
    
    #create the json file
    json_file = os.path.join(full_dir,'crime_tweets.json')

    f = open(json_file,'w')

    ''' search variables: '''
    search_params = [['Robbery'], ['Kidnap'], ['Shooting'], ['Arrest'],['Homicide'], ['Narcotics'],['Marijuana']]
    
    #loop through each search term and dump the tweets as json
    for i in range(0, len(search_params)):
        search_phrases = search_params[i]
        #print("Generating tweet for:"+ search_phrases)
    
        #time_limit = 1.5        # runtime limit in hours
        max_tweets = 500        # number of tweets per search (will be iterated over) - maximum is 100
        Chicago = '41.881832, -87.623177, 320km'
        #Chicago = '39.8,-95.583068847656,2500km'
        #json_file = "C:\\datasets\\crimedata\\crimes_tweets_26thFeb.json"
        
        # authorize and load the twitter API
        api = load_api()
         
        # collect tweets
        tweets = tweet_search(api, search_phrases, max_tweets,geocode=Chicago)
        #tweets = tweet_search(api, search_phrases, max_tweets)
        write_tweets(tweets, json_file)
    
    #store the json file into csv and process
    store_process_csv(json_file)
    #close the file handle
    f.close()
    
    
if __name__ == "__main__":
    main()
    print("Process got executed")
