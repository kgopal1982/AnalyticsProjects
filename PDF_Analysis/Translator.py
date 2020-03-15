#https://stackabuse.com/text-translation-with-google-translate-api-in-python/
#DOES NOT WoRK due to API limitation

import numpy as np
import pandas as pd
import nltk
#nltk.download('punkt') # one time execution
import re
import os
from nltk import tokenize

#inputfilepath = "C:\\Users\\ekrigos\\Desktop\\DataS\\REVA\\finalyearProj\\pdf_analysis\\inputs_healthHazard\\"
#filename = 'server_noise_health_hazard.pdf.txt_top_ranked.txt'
#filename_transname = 'server_noise_health_hazard.pdf.txt_top_ranked_translated.txt'
inputfilepath = "C:\\Users\\ekrigos\\Desktop\\DataS\\REVA\\finalyearProj\\pdf_analysis\\sentiment_analysis\\"
filename = 'pwc-union-budget-analysis.pdf.txt_top_ranked.txt'
filename_transname = 'pwc-union-budget-analysis.pdf.txt_top_ranked_translated.txt'


filename_translated = inputfilepath + filename_transname

def process_text(inputfilepath, filename):

    #inputfilepath = inputfilepath = "C:\\Users\\ekrigos\\Desktop\\DataS\\REVA\\finalyearProj\\pdf_analysis\\inputs_healthHazard\\"
    #filename = 'server_noise_health_hazard.pdf.txt'
    fileName1 = inputfilepath + filename
    
    file = open(fileName1,"r")
    
    fullText = file.read()
    file.close()
    
    tokens_lst = tokenize.sent_tokenize(fullText)
    print(tokens_lst[:1])
    
# =============================================================================
#     df = pd.DataFrame(tokens_lst, columns = ['text'])
#     print("dataframe is")
#     print(df.head())
#     #add into list
#     sentences = []
#     for s in df['text']:
#       sentences.append(sent_tokenize(s))
#     
#     sentences = [y for x in sentences for y in x] # flatten list
#     print("sentence list")
#     print(sentences[:1])
# =============================================================================
    return tokens_lst
        

        
sentences = process_text(inputfilepath, filename)
print(sentences[:1])

    
#from translate import Translator
# =============================================================================
# from translate import Translator
# translator = Translator(from_lang="english",to_lang="hindi")
# 
# for i in sentences:
#     print("original sentence")
#     print (i)
#     print("________")
#     print("Hindi translated")
#     print(translator.translate(i))
#     print("/////////////////")
# =============================================================================



import googletrans
#list supported languages by google translator
print(googletrans.LANGUAGES)

from googletrans import Translator  # Import Translator module from googletrans package

translator = Translator() # Create object of Translator.

translatedList = translator.translate(sentences, dest='hi')

for translated in translatedList:
           print(translated.origin, '->', translated.text)
          
#dump into a file
with open(filename_translated, 'w', encoding="utf-8") as filehandle:
    for translated in translatedList:
        filehandle.write('%s\n' % translated.text)