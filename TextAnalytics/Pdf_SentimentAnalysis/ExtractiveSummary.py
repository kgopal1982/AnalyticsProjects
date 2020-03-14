#https://www.analyticsvidhya.com/blog/2018/11/introduction-text-summarization-textrank-python/
import numpy as np
import pandas as pd
import nltk
#nltk.download('punkt') # one time execution
import re
import os
from nltk import tokenize

inputfilepath = "C:\\Users\\ekrigos\\Desktop\\DataS\\REVA\\finalyearProj\\pdf_analysis\\inputs_healthHazard\\"
filename = 'server_noise_health_hazard.pdf.txt'
output_file_name_top_ranked = inputfilepath + filename + '_top_ranked.txt'

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

#clean the data
# remove punctuations, numbers and special characters
clean_sentences = pd.Series(sentences).str.replace("[^a-zA-Z]", " ")

# make alphabets lowercase
clean_sentences = [s.lower() for s in clean_sentences]

#remove stopwords
#nltk.download('stopwords')
from nltk.corpus import stopwords
stop_words = stopwords.words('english')

# function to remove stopwords
def remove_stopwords(sen):
    sen_new = " ".join([i for i in sen if i not in stop_words])
    return sen_new

# remove stopwords from the sentences
clean_sentences = [remove_stopwords(r.split()) for r in clean_sentences]



#extract the word embeddings
word_embeddings = {}
f = open('c:\\datasets\\glove\\glove.6B.100d.txt', encoding='utf-8')
for line in f:
    values = line.split()
    word = values[0]
    coefs = np.asarray(values[1:], dtype='float32')
    word_embeddings[word] = coefs
f.close()

len(word_embeddings)

#let's create vectors for our sentences
sentence_vectors = []
for i in clean_sentences:
  if len(i) != 0:
    v = sum([word_embeddings.get(w, np.zeros((100,))) for w in i.split()])/(len(i.split())+0.001)
  else:
    v = np.zeros((100,))
  sentence_vectors.append(v)
  
#similarity matrix representation
#Let’s first define a zero matrix of dimensions (n * n).  
#We will initialize this matrix with cosine similarity scores of the sentences. 
#Here, n is the number of sentences.
  
# similarity matrix
sim_mat = np.zeros([len(sentences), len(sentences)])

#We will use Cosine Similarity to compute the similarity between a pair of sentences.
from sklearn.metrics.pairwise import cosine_similarity

#And initialize the matrix with cosine similarity scores.
for i in range(len(sentences)):
  for j in range(len(sentences)):
    if i != j:
      sim_mat[i][j] = cosine_similarity(sentence_vectors[i].reshape(1,100), sentence_vectors[j].reshape(1,100))[0,0]
      
# =============================================================================
#  let’s convert the similarity matrix sim_mat into a graph. 
#  The nodes of this graph will represent the sentences and 
#  the edges will represent the similarity scores between the sentences. 
#  On this graph, we will apply the PageRank algorithm to arrive at the sentence rankings.
# =============================================================================

import networkx as nx

nx_graph = nx.from_numpy_array(sim_mat)
scores = nx.pagerank(nx_graph)

#Summary Extraction
#extract the top N sentences based on their rankings for summary generation
ranked_sentences = sorted(((scores[i],s) for i,s in enumerate(sentences)), reverse=True)
top_ranked_sentences = []

# Extract top 10 sentences as the summary
for i in range(10):
  print(ranked_sentences[i][1])
  top_ranked_sentences.append(ranked_sentences[i][1])
  
print(top_ranked_sentences)

#dump into a file
with open(output_file_name_top_ranked, 'w') as filehandle:
    for listitem in top_ranked_sentences:
        filehandle.write('%s\n' % listitem)