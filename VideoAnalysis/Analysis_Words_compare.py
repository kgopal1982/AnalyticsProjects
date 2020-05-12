#Compare time taken for 2 wav files for the common words
#This wil be executed after execution of the file AudioAnalysisUsingPocketShhinx.py
import pandas as pd

orig_filename = 'What_is_Happiness_Sadhguru_usingPhoenix_words_time.csv'
imit_1_filename = 'converted_What_is_Happiness_Sadhguru_imitate_1_usingPhoenix_words_time.csv'
#common_filename = 'What_is_Happiness_Sadhguru_Common_Words.csv'

orig_df = pd.read_csv(orig_filename)
imit_1_df = pd.read_csv(imit_1_filename)
#common_df = pd.read_csv(common_filename)

orig_df.head()
imit_1_df.head()
#common_df.head()

df1 = orig_df.copy(deep = True)
df2 = imit_1_df.copy(deep = True)
#df3 = common_df.copy(deep = True)

df1 = df1[['word', 'time_taken']]
df2 = df2[['word', 'time_taken']]
#df3 = df3[['0']]

orig_df1_count = df1.shape[0]
orig_df2_count = df2.shape[0]
#orig_df3_count = df3.shape[0]

print("orig_df1_count is: ", orig_df1_count)
print("orig_df2_count is: ", orig_df2_count)
#print("orig_df3_count is: ", orig_df3_count)

#remove duplicates
df1 = df1.drop_duplicates(subset=['word'])
df2 = df2.drop_duplicates(subset=['word'])
# df3 = df3.drop_duplicates()

#convert to dict
df1_dict = dict(zip(df1.word, df1.time_taken))
df2_dict = dict(zip(df2.word, df2.time_taken))

#find common words betwen the 2 files
common_keys = set(df1_dict).intersection(df2_dict)
common_words_lst = []
for word in common_keys:
    common_words_lst.append(word)
    
print(len(common_words_lst))


#create dataframe to store time taken for df1, based on words from df3
df1_common_lst_word = []
df1_common_lst_time_taken = []

#word = 'happiness'
#word_lst = ['happiness', 'with', 'was']

for word in common_words_lst:
    for key,value in df1_dict.items():
        if (key == word):
            df1_common_lst_word.append(key)
            df1_common_lst_time_taken.append(value)
            
print(len(df1_common_lst_word))
        
df1_common_word = pd.DataFrame(list(zip(df1_common_lst_word, df1_common_lst_time_taken)),
                               columns = ['Word', 'time_taken'])
print(df1_common_word.head())


#create dataframe to store time taken for df2, based on words from df3
df2_common_lst_word = []
df2_common_lst_time_taken = []

#word = 'happiness'
#word_lst = ['happiness', 'with', 'was']
for word in common_words_lst:
    for key,value in df2_dict.items():
        if (key == word):
            df2_common_lst_word.append(key)
            df2_common_lst_time_taken.append(value)
            
print(len(df2_common_lst_word))
        
df2_common_word = pd.DataFrame(list(zip(df2_common_lst_word, df2_common_lst_time_taken)),
                               columns = ['Common Words', 'time_taken'])
print(df2_common_word.head(10))

