#analyze the json file
import json 
import pandas as pd 
from pandas.io.json import json_normalize #package for flattening json in pandas df

# =============================================================================
# #load json object
# with open('C:\\datasets\\crimedata\\12thFeb\\crimes_tweets_12thFeb.json') as f:
#     data = [json.loads(line) for line in f]
# =============================================================================

#load the json file   
df_orig = pd.read_json('C:\\datasets\\crimedata\\12thFeb\\crimes_tweets_12thFeb.json', lines=True)
df_orig.head()

df = df_orig.copy(deep = True)

#keep the columns which are of interest
df = df[['created_at','id','id_str','lang','retweet_count','retweeted','source','text','user']]

#check for duplicates
df.duplicated('id')

#it shows there are duplicates
#drop the duplicates
df.drop_duplicates(subset = "id", keep = 'first', inplace = True)

#out of 3500 records, only 709 records are left