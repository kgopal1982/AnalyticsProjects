#####################################
#Analyze .wav file using pocketsphinx and convert from audio file to text
#Fnd out time taken for each word

#sudo apt-get install python3-sphinx
#sudo apt-get update -y
#sudo apt-get install -y python-pocketsphinx
#####################################

##https://github.com/bambocher/pocketsphinx-python
import os
from pocketsphinx import Pocketsphinx, get_model_path, get_data_path

import pandas as pd

model_path = get_model_path()
data_path = get_data_path()

    
config = {
    'hmm': os.path.join(model_path, 'en-us'),
    'lm': os.path.join(model_path, 'en-us.lm.bin'),
    'dict': os.path.join(model_path, 'cmudict-en-us.dict')
}

#place the .wav fie in the directory of data_path 
# /home/krishna/anaconda3/lib/python3.7/site-packages/pocketsphinx/data

ps = Pocketsphinx(**config)
ps.decode(
    audio_file=os.path.join(data_path, 'obama_farewell_speech.wav'),
    buffer_size=2048,
    no_search=False,
    full_utt=False
)

#print(ps.segments())

#save the detailed segments of the words, 
#which will contain details word, probablity, start_time and end_time
print('Detailed segments:', *ps.segments(detailed=True), sep='\n')

with open('output_segments_obama_farewell_speech.txt', 'a') as f:
    print(*ps.segments(detailed=True), sep='\n', file=f)
    
#convert from audio to text and save    
# text = ps.hypothesis()

# file1 = open("Donald_Trumps_Victory_Speech_DeepSpeech_UsingPocketSphinx.txt","w")#write mode 
# file1.write(text) 
# file1.close() 

#load into dataframe
# For the above saved file, modify manually by removing '(',')',' and then save as modified fie
df = pd.read_csv('output_segments_donaldTrump_modified.txt', sep=",", header=None)
df.columns = ["word", "prob","startTime", "endTime"]
df.head()
#calculate time taken for each word
df['time_taken']=df['endTime'] - df['startTime']
df.head(20)

#calculate average of time taken for each word
avg_time = df['time_taken'].mean()
avg_time = int(avg_time)
print("Average Time taken for each word")
print(avg_time)

#df['Intense'] = df['yes' if df['avg_time']>df['time_taken'] else 'no']
#add a new column as Intense. The logic is, if the time_taken is greater than average 
#time taken, then consider it as intense word (Stress or relaxed)
import numpy as np
df['Intense'] = np.where(df['time_taken'] >= avg_time, 'Yes', 'No')
df = df.drop(['prob'], axis = 1)
df.head(30)

#remove rows with word <sil>,<s>
search_string=['<sil>','<s>','[SPEECH]']
df_new = df[~df.word.isin(search_string)]

df_new.head(30)
