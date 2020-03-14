#http://carrefax.com/new-blog/2017/3/20/tokenize-text-file-into-sentences-with-python
import nltk.data
import codecs
import os

doc = codecs.open('C:\\Users\\ekrigos\\Desktop\\DataS\\REVA\\finalyearProj\\pdf_analysis\\inputs_pdf\\Q1_wipro_2010_1.pdf.txt', 'r')
content = doc.read()
from nltk.tokenize import sent_tokenize
#tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

#print ('\n-----\n'.join(tokenizer.tokenize(content)))
#print(sent_tokenize(content))

sent_lst = sent_tokenize(content)

for i in sent_lst:
    print(i)
    print("__________________")

import pandas as pd
    
df_sent = pd.DataFrame(sent_lst)
print(df_sent)

df_sent.to_csv("C:\\Users\\ekrigos\\Desktop\\DataS\\REVA\\finalyearProj\\pdf_analysis\\inputs_pdf\\text_file_csv.csv")