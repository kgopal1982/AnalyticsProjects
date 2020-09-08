###################################
#Here, we are performing Emotion Analysis using DepecheMood lexicon
###################################

from Retrieve_Mood import *

#text = "When she remembered the style of his address, she was still full of indignation; but when she considered how unjustly she had condemned and upbraided him, her anger was turned against herself; and his disappointed feelings became the object of compassion."

#fileName = "What_is_Happiness_Sadhguru_using_Local_DeepSpeech_Model.txt"
fileName = "/home/krishna/datas/video_analysis/CallHome/4390_Speaker1_Using_DeepSpeech_Model.txt"

file = open(fileName,"r", encoding = 'utf-8')

text = file.read()
file.close()

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# categories
emo_name = ['AFRAID','AMUSED','ANGRY','ANNOYED','DONT_CARE','HAPPY','INSPIRED','SAD']

# score
score = mood_metric_scores(dm,text)

#emotion plotting
import matplotlib.pyplot as plt
fig = plt.figure(figsize=(20,10))
ax = fig.add_axes([0,0,1,1])
plt.xlabel('Emotion Types', fontsize = 40)
plt.ylabel('Scores', fontsize = 40)
plt.rcParams.update({'font.size': 40})
plt.xticks(rotation=45)
#plt.figure(figsize=(20,10))
df = pd.DataFrame({'emotion':emo_name, 'score':score})
ax.bar(emo_name,score)
#plt.savefig('/home/krishna/datas/video_analysis/CallHome/4390_Speaker1_Using_DeepSpeech_Model.jpg')

# plot the scores
# plt.figure(figsize=(10,7))
# df = pd.DataFrame({'emotion':emo_name, 'score':score})
# ax = sns.barplot(x='emotion', y='score', data=df, palette="hls")
# ax.set_xlabel('mood', fontsize = 25)
# ax.set_ylabel('score', fontsize = 25)
# ax.legend()
# ax.tick_params(axis="x", labelsize=15, labelrotation=45)
# ax.tick_params(axis="y", labelsize=15, labelrotation=45)
# plt.show()