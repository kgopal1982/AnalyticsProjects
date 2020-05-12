#Compare the text files generated after audio-to-text conversion

#compare no of total words in the files
orig_file = 'What_is_Happiness_Sadhguru_using_Local_DeepSpeech_Model.txt'
conv_file = 'converted_What_is_Happiness_Sadhguru_imitate_1_using_Local_DeepSpeech_Model.txt'
file_name = "What_is_Happiness_Sadhguru"
#df_file_name_common_words = file_name + '_Common_Words' + '.csv'

#function to count no of words in a file
def count_words(filename):
    filename = open(filename,"r")
    data = filename.read()
    words = data.split()
    return len(words)


len_words1 = count_words(orig_file)
len_words2 = count_words(conv_file)

print('Number of words in original text file :', len_words1)
print('Number of words in converted text file :', len_words2)

#find words in a file
def find_words(filename):
    #filename = orig_file
    filename = open(filename, "r")
    data = filename.read()
    data = data.lower()
    words = data.split()
    return words

lst_words1 = find_words(orig_file)
lst_words2 = find_words(conv_file)

print(len(lst_words1))
print(len(lst_words2))

# #remove duplicates
# set_lst_words1 = set(lst_words1)
# set_lst_words2 = set(lst_words2)

# print(len(set_lst_words1))
# print(len(set_lst_words2))

# #convert to lst
# lst_lst_words1 = list(set_lst_words1)
# lst_lst_words2 = list(set_lst_words2)


# lst_common_words = []

# #check which list is bigger in length
# if (len(lst_lst_words1)>len(lst_lst_words2)):
#     for i in lst_lst_words2:
#         for j in lst_lst_words1:
#             if i == j:
#                 lst_common_words.append(i)
# else:
#     for i in lst_lst_words1:
#      for j in lst_lst_words2:
#          if i == j:
#              lst_common_words.append(i)
             

# print("Common words are")
# print(lst_common_words)
# print("length of common words is")
# print(len(lst_common_words))

# import pandas as pd
# df = pd.DataFrame(lst_common_words)
# df.to_csv(df_file_name_common_words)


