from textblob import TextBlob
import sys, tweepy
import matplotlib.pyplot as plt
from tweepy import OAuthHandler
import re
import pandas as pd
import json

def perc(part, whole):
    return 100*float(part)/float(whole)

consumer_key = 'Kr6euZvC2WrRPB8gZTnMtmCDJ'
consumer_secret = 'fqzEkQZk4Et6jJe2VV2KMkdepIWqr8b3BPCIleXDY47fsc2PpB'
access_token = '2538332490-iYOH0lWlPy6LDm7VXa5dsaaDXJRKKcNlFRxm1CY'
access_secret = 'YDdaWVYJdFKyttLc5sG9K8iSS7bQrqSXSVR2qyh7IcTAw'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

auth = tweepy.OAuthHandler(consumer_key, consumer_secret) #Interacting with twitter's API
auth.set_access_token(access_token, access_secret)

api = tweepy.API (auth,  wait_on_rate_limit=True) #creating the API object

searchTerm = input("Enter keyword/hashtag to search about:")
noOfSearchTerms = int(input("Enter how many tweets to analyze: "))

def clean_tweet(tweet): 
        ''' 
        Utility function to clean tweet text by removing links, special characters 
        using simple regex statements. 
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", tweet).split())

tweets = tweepy.Cursor(api.search, q=searchTerm).items(noOfSearchTerms)

def write_tweets(tweets, filename):
    ''' Function that appends tweets to a file. '''
 
    with open(filename, 'a') as f:
        for tweet in tweets:
            json.dump(tweet._json, f)
            f.write('\n')
            
filename = "C:\\datasets\\priyanka\\tweets_priyanka1.json"
write_tweets(tweets,filename)
print("tweet json file is stored")
#print(tweets)

#create tweets dictionary from json file
tweet_files = [filename]
dict1 = []
for file in tweet_files:
    with open(file,'r') as f:
        for line in f.readlines():
            dict1.append(json.loads(line))

#store the result in dataframe
def populate_tweet_df(dict1):
    df = pd.DataFrame()
 
    df['text'] = list(map(lambda tweet: tweet['text'], dict1))
 
    return df

#PriyankaGandhi
df = populate_tweet_df(dict1)
df.to_csv("C:\\DataSets\\priyanka\\tweets_priyanka.csv")
print("Dataframe is created")
#data_set.to_csv("C:\\DataSets\\citizenship\\twitter_CitizenshipAmendmentBill_4_text.csv")
#print("Data is stored")

#create a empty list to store the polarity
polarity_list = []


for row_index,row in df.iterrows():
     analysis = TextBlob(clean_tweet(row.text))
     #print(row_index,analysis)
     #print("Polarity")
     Polarity = analysis.sentiment.polarity
     #print(row_index,Polarity)
     
     if (Polarity == 0.0):
        polarity_list.append('Neutral')
     elif (Polarity < 0.0):
        polarity_list.append('Negative')
     elif (Polarity > 0.0):
        polarity_list.append('Postive')
     #df['Polarity'] = analysis.sentiment.polarity

df['Polarity'] = polarity_list
#save into dataframe
df.to_csv("C:\\DataSets\\priyanka\\tweets_priyanka_polarity.csv")
print("dataframe is updated with polarity")
#datafram is saved with polarity

#check the sentiment of the tweets
total_count = len(df)
positive_df = df[df['Polarity'] == "Postive"]
positive_count = len(positive_df)
negative_df = df[df['Polarity'] == "Negative"]
negative_count = len(negative_df)
neutral_df = df[df['Polarity'] == "Neutral"]
neutral_count = len(neutral_df)

#calculate percentage of polarity
import numpy as np
print("Postive review percentags is")
positive_perc = np.round(float(positive_count)/float(total_count)*100,2)
print(positive_perc)

print("Negative review percentags is")
negative_perc = np.round(float(negative_count)/float(total_count)*100,2)
print(negative_perc)

print("Neutral review percentags is")
neutral_perc = np.round(float(neutral_count)/float(total_count)*100,2)
print(neutral_perc)

#draw pie plot
#labels = ['Positive [' + str(positive) + '%]', 'Neutral [' + str(neutral) + '%]'], 'Negative [' + str(negative) + '%]']
labels = ['Positive [' + str(positive_perc) + '%]', 'Neutral [' + str(neutral_perc) + '%]', 'Negative [' + str(negative_perc) + '%]']
sizes = [positive_perc, neutral_perc, negative_perc]
colors = ['green', 'gold', 'red']
patches, text = plt.pie(sizes, colors = colors, startangle=90)
plt.legend(patches, labels, loc="best")
plt.title("How people are reacting on" + searchTerm + " by analyzing " + str(noOfSearchTerms) + "Tweets.")
plt.axis('equal')
plt.tight_layout()
plt.show()


