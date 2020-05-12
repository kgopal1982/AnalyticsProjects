###################################
#Here, we are performing Emotion Analysis using NRC lexicon
###################################
from nltk import tokenize
import pandas as pd
import re

import os

#fileName = "What_is_Happiness_Sadhguru_using_Local_DeepSpeech_Model.txt"
fileName = "converted_What_is_Happiness_Sadhguru_imitate_1_using_Local_DeepSpeech_Model.txt"

file = open(fileName,"r", encoding = 'utf-8')

fullText = file.read()
file.close()

#fullText = "Hello Krishna, How are you? I am fine. I am ok"

tokens_lst = tokenize.sent_tokenize(fullText)
print(tokens_lst)
    
df = pd.DataFrame(tokens_lst, columns = ['text'])
print(df.head())

#clean the texts
def clean_text(text): 
        ''' 
        Utility function to clean tweet text by removing links, special characters 
        using simple regex statements. 
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", text).split())

df['text'] = df['text'].map(lambda com : clean_text(com))

#remove stopwords
    
from nltk.tokenize import ToktokTokenizer
token=ToktokTokenizer()

from nltk.corpus import stopwords
stopWordList = stopwords.words('english')

def stopWordsRemove(text):
    wordList=[x.lower().strip() for x in token.tokenize(text)]
    removedList=[x for x in wordList if not x in stopWordList]
    text=' '.join(removedList)
    return text

print(df.head())
df['text'] = df['text'].map(lambda com : stopWordsRemove(com))
print(df.head())

#remove punctuation

from string import punctuation

def strip_punctuation(text):
    return ''.join(c for c in text if c not in punctuation)

print(df.head())
df['text'] = df['text'].map(lambda com : strip_punctuation(com))
print(df.head())

#remove digits
def removeDigits(text):
    return ''.join([i for i in text if not i.isdigit()])

print(df.head())
df['text'] = df['text'].map(lambda com : removeDigits(com))
print(df.head())

cleaned_text = df.iloc[0]['text']

#http://jonathansoma.com/lede/algorithms-2017/classes/more-text-analysis/nrc-emotional-lexicon/
lex_filepath = "NRC-Emotion-Lexicon-Wordlevel-v0.92.txt"
emolex_df = pd.read_csv(lex_filepath, names=["word", "emotion", "association"], sep='\t')
emolex_df.head()

emolex_df.emotion.unique()

emolex_df['emotion'].value_counts()

emolex_df[emolex_df.association == 1].emotion.value_counts()

lst_cleaned_text = list(cleaned_text.split(" "))
print(lst_cleaned_text)

angry_words = emolex_df[(emolex_df.association == 1) & (emolex_df.emotion == 'anger')].word
angry_words = angry_words.tolist()

joy_words = emolex_df[(emolex_df.association == 1) & (emolex_df.emotion == 'joy')].word
joy_words = joy_words.tolist()

negative_words = emolex_df[(emolex_df.association == 1) & (emolex_df.emotion == 'negative')].word
negative_words = negative_words.tolist()

positive_words = emolex_df[(emolex_df.association == 1) & (emolex_df.emotion == 'positive')].word
positive_words = positive_words.tolist()

fear_words = emolex_df[(emolex_df.association == 1) & (emolex_df.emotion == 'fear')].word
fear_words = fear_words.tolist()

fear_words = emolex_df[(emolex_df.association == 1) & (emolex_df.emotion == 'fear')].word
fear_words = fear_words.tolist()

trust_words = emolex_df[(emolex_df.association == 1) & (emolex_df.emotion == 'trust')].word
trust_words = trust_words.tolist()

sadness_words = emolex_df[(emolex_df.association == 1) & (emolex_df.emotion == 'sadness')].word
sadness_words = sadness_words.tolist()

disgust_words = emolex_df[(emolex_df.association == 1) & (emolex_df.emotion == 'disgust')].word
disgust_words = disgust_words.tolist()


anticipation_words = emolex_df[(emolex_df.association == 1) & (emolex_df.emotion == 'anticipation')].word
anticipation_words = anticipation_words.tolist()

surprise_words = emolex_df[(emolex_df.association == 1) & (emolex_df.emotion == 'surprise')].word
surprise_words = surprise_words.tolist()

angry_score = 0
for word in lst_cleaned_text:
    #print(li)
    if word in angry_words:
        print(word)
        angry_score = angry_score + 1
print(angry_score)

joy_score = 0
for word in lst_cleaned_text:
    #print(li)
    if word in joy_words:
        print(word)
        joy_score = joy_score + 1
print(joy_score)

negative_score = 0
for word in lst_cleaned_text:
    #print(li)
    if word in negative_words:
        print(word)
        negative_score = negative_score + 1
print(negative_score)


positive_score = 0
for word in lst_cleaned_text:
    #print(li)
    if word in positive_words:
        print(word)
        positive_score = positive_score + 1
print(positive_score)


fear_score = 0
for word in lst_cleaned_text:
    #print(li)
    if word in fear_words:
        print(word)
        fear_score = fear_score + 1
print(fear_score)


trust_score = 0
for word in lst_cleaned_text:
    #print(li)
    if word in trust_words:
        print(word)
        trust_score = trust_score + 1
print(trust_score)


sadness_score = 0
for word in lst_cleaned_text:
    #print(li)
    if word in sadness_words:
        print(word)
        sadness_score = sadness_score + 1
print(sadness_score)


disgust_score = 0
for word in lst_cleaned_text:
    #print(li)
    if word in disgust_words:
        print(word)
        disgust_score = disgust_score + 1
print(disgust_score)


anticipation_score = 0
for word in lst_cleaned_text:
    #print(li)
    if word in anticipation_words:
        print(word)
        anticipation_score = anticipation_score + 1
print(anticipation_score)


surprise_score = 0
for word in lst_cleaned_text:
    #print(li)
    if word in surprise_words:
        print(word)
        surprise_score = surprise_score + 1
print(surprise_score)

emotion_type_lst = ['fear','anger','trust','sadness','disgust','anticipation','joy','surprise']
emotion_type_score = [fear_score,angry_score,trust_score,sadness_score,disgust_score,anticipation_score,joy_score,surprise_score]

sentiment_type_list = ['positive', 'negative']
sentiment_type_score = ['positive_score', 'negative_score']


df_score_emotion = pd.DataFrame(list(zip(emotion_type_lst, emotion_type_score)), columns = ['Type','Score'])
df_score_emotion

df_score_sentiment = pd.DataFrame(list(zip(sentiment_type_list, sentiment_type_score)), columns = ['Type','Score'])
df_score_sentiment


#emotion plotting
import matplotlib.pyplot as plt
fig = plt.figure(figsize=(20,10))
ax = fig.add_axes([0,0,1,1])
ax.set_xlabel('Emotion Types', fontsize = 40)
ax.set_ylabel('Scores', fontsize = 40)
plt.rcParams.update({'font.size': 40})
plt.xticks(rotation=45)
#plt.figure(figsize=(20,10))
ax.bar(emotion_type_lst,emotion_type_score)
plt.show();


#sentiment plotting
# import matplotlib.pyplot as plt
# fig = plt.figure(figsize=(20,10))
# ax = fig.add_axes([0,0,1,1])
# ax.set_xlabel('Sentiment Types', fontsize = 25)
# ax.set_ylabel('Scores', fontsize = 20)
# plt.rcParams.update({'font.size': 22})
# plt.xticks(rotation=45)
# #plt.figure(figsize=(20,10))
# ax.bar(sentiment_type_list,sentiment_type_score)
# plt.show();
