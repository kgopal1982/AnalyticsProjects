from nltk import tokenize
import pandas as pd
import re

import os

inputfilepath = "C:\\Users\\ekrigos\\Desktop\\DataS\\REVA\\finalyearProj\\pdf_analysis\\inputs_pdf\\"
wipro_output_file = "C:\\Users\\ekrigos\\Desktop\\DataS\\REVA\\finalyearProj\\pdf_analysis\\inputs_pdf\\2009_Wipro_Director_Speech.csv"


def process_text(inputfilepath, filename,wipro_output_file):

    #inputfilepath = 'C:\\Users\\ekrigos\\Desktop\\DataS\\REVA\\finalyearProj\\pdf_analysis\\inputs_pdf\\'
    #filename = 'Q1_wipro_2010_1.pdf.txt'
    fileName1 = inputfilepath + filename
    
    file = open(fileName1,"r")
    
    fullText = file.read()
    file.close()
    
    tokens_lst = tokenize.sent_tokenize(fullText)
    #print(tokens_lst)
    
    df = pd.DataFrame(tokens_lst, columns = ['text'])
    print(df.head())
    #clean the tweets
    def clean_tweet(tweet): 
            ''' 
            Utility function to clean tweet text by removing links, special characters 
            using simple regex statements. 
            '''
            return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", tweet).split())
    
    df['text'] = df['text'].map(lambda com : clean_tweet(com))
    
    
    print(df.head())
    
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
    
    
    def perc(part, whole):
        return 100*float(part)/float(whole)
    
    #sentiment analysis
    from textblob import TextBlob
    
    positive = 0
    negative = 0
    neutral = 0
    polarity = 0
    
    noOfSearchTerms = len(df)
    
    tweets = df['text']
    for tweet in tweets:
        analysis = TextBlob(tweet)
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
    #polarity = perc(polarity, noOfSearchTerms)
    
    print("% of positive responses")
    #positive = int(positive)
    positive = round(positive,2)
    print(positive)
    print("% of negative responses")
    #negative = int(negative)
    negative = round(negative,2)
    print(negative)
    print("% of neutral responses")
    #neutral = int(neutral)
    neutral = round(neutral,2)
    print(neutral)
    #print("% of polarity")
    #print(polarity)
    
#    pos_resp = "% of positive response"
#    pos_resp_perc = str(positive)
#    pos_resp_text = pos_resp + ":=" + pos_resp_perc
#    print(pos_resp_text)
#    
#    neg_resp = "% of negative response"
#    neg_resp_perc = str(negative)
#    neg_resp_text = neg_resp + ":=" + neg_resp_perc
#    print(neg_resp_text)
#    
#    neut_resp = "% of neutral response"
#    neut_resp_perc = str(neutral)
#    neut_resp_text = neut_resp + ":=" + neut_resp_perc
#    print(neut_resp_text)
    
    #final_response_text = pos_resp_text + "\n" + neg_resp_text + "\n" + neut_resp_text + "\n"
    #
    #output_fileName = fileName + '_output_sentiment.txt'
    #text_file = open(output_fileName, "w")
    #text_file.write(final_response_text)
    #text_file.close()
    
    lst_columns = ["Positive_Response_Perc", "Negative_Response_Perc", "Neutral_Response_Perc"]
    lst_vals = [positive, negative, neutral]
    df = pd.DataFrame(list(zip(lst_columns, lst_vals)), 
               columns =['Name', 'val']) 
    #df = pd.DataFrame(lst_val)
    #df = df.transpose()
    #df.columns = ["FileName", "Positive_Response_Perc", "Negative_Response_Perc", "Neutral_Response_Perc"]
    print(df)
    
    import matplotlib.pyplot as plt
    labels = ['Positive [' + str(positive) + '%]', 'Neutral [' + str(neutral) + '%]', 'Negative [' + str(negative) + '%]']
    sizes = [positive, neutral, negative]
    colors = ['green', 'gold', 'red']
    patches, text = plt.pie(sizes, colors = colors, startangle=90)
    plt.legend(patches, labels, loc="best")
    plt.title("Sentiment Analysis")
    plt.axis('equal')
    plt.tight_layout()
    plt.show()
    
    df.to_csv(wipro_output_file, mode='a')


for filename in os.listdir(inputfilepath):
    if filename.endswith(".txt"): 
         # print(os.path.join(directory, filename))
        print(filename)
        process_text(inputfilepath, filename, wipro_output_file)