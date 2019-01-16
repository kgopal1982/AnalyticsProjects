from textblob import TextBlob
import sys, tweepy
import matplotlib.pyplot as plt
from tweepy import OAuthHandler

def perc(part, whole):
    return 100*float(part)/float(whole)

consumer_key = ''
consumer_secret = ''
access_token = ''
access_secret = ''

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

auth = tweepy.OAuthHandler(consumer_key, consumer_secret) #Interacting with twitter's API
auth.set_access_token(access_token, access_secret)

api = tweepy.API (auth,  wait_on_rate_limit=True) #creating the API object

searchTerm = input("Enter keyword/hashtag to search about:")
noOfSearchTerms = int(input("Enter how many tweets to analyze: "))

tweets = tweepy.Cursor(api.search, q=searchTerm).items(noOfSearchTerms)

positive = 0
negative = 0
neutral = 0
polarity = 0

for tweet in tweets:
    #print(tweet.text)
    analysis = TextBlob(tweet.text)
    polarity += analysis.sentiment.polarity
    
    if (analysis.sentiment.polarity == 0.0):
        neutral = neutral + 1
    elif (analysis.sentiment.polarity < 0.0):
       negative = negative + 1
    elif (analysis.sentiment.polarity > 0.0):
        positive = positive + 1
positive = perc(positive, noOfSearchTerms)
negative = perc(negative, noOfSearchTerms)
neutral = perc(neutral, noOfSearchTerms)
polarity = perc(polarity, noOfSearchTerms)

#print("% of positive responses")
#print(positive)
#print("% of negative responses")
#print(negative)
#print("% of neutral responses")
#print(neutral)
#print("% of polarity")
#print(polarity)

print("How people are reacting on " + searchTerm + " by analyzing " + str(noOfSearchTerms) + " Tweets.")

if (polarity == 0):
    print("Neutral")
elif (polarity <0.0):
    print("Negative")
elif (polarity >0.0):
    print("Positive")
    
#labels = ['Positive [' + str(positive) + '%]', 'Neutral [' + str(neutral) + '%]'], 'Negative [' + str(negative) + '%]']
labels = ['Positive [' + str(positive) + '%]', 'Neutral [' + str(neutral) + '%]', 'Negative [' + str(negative) + '%]']
sizes = [positive, neutral, negative]
colors = ['green', 'gold', 'red']
patches, text = plt.pie(sizes, colors = colors, startangle=90)
plt.legend(patches, labels, loc="best")
plt.title("How people are reacting on" + searchTerm + " by analyzing " + str(noOfSearchTerms) + "Tweets.")
plt.axis('equal')
plt.tight_layout()
plt.show()
    
