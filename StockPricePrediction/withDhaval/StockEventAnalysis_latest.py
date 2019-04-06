import pandas as pd
import sqlite3
from os import path
import matplotlib.pyplot as plt

df_main = pd.read_csv('C:\\DataSets\\StockAnalysis\\dhaval\\2017-18.csv', usecols = range(0,8))
df_main.columns = ['Symbol', 'date', 'hr:min', 'open', 'high', 'low', 'close', 'Volume']

df = df_main.copy(deep = True)

STOCK_SYMBOL = 'ASHOKLEY'

df = df[df['Symbol'] == STOCK_SYMBOL]

#df.to_csv("C:\\DataSets\\StockAnalysis\\dhaval\\company_csvs\\" + STOCK_SYMBOL + "orig.csv")

df.date = df.date.astype(str)#convert to string
df['date'] =  pd.to_datetime(df['date'])#convert to datetime

#extract year,month and day
df['year'] = pd.DatetimeIndex(df['date']).year
df['month'] = pd.DatetimeIndex(df['date']).month
df['day'] = pd.DatetimeIndex(df['date']).day

df = df.rename(columns = {'hr:mm': 'hrmm'})
df[['hour','minute']] = df['hr:min'].str.split(":",expand=True,)#split into 2 separate columns

#delete the records which are not required
df = df.drop(df[(df.hour == '15') & (df.minute > '30')].index)
df = df.drop(df[(df.hour == '16')].index)
df = df.drop(df[(df.hour == '09') & (df.minute == '08')].index)

df['date1'] = pd.to_datetime(df[['year', 'month', 'day', 'hour', 'minute']])#create a new date column
#set date as index
df.index = df['date1']
#delete unnessary columns
del df['date']
del df['year']
del df['month']
del df['day']
del df['hour']
del df['minute']
del df['Symbol']
del df['hr:min']
del df['date1']
#save to csv
df.to_csv("C:\\DataSets\\StockAnalysis\\dhaval\\company_csvs\\" + STOCK_SYMBOL + ".csv")

#get result dates
df_result_main = pd.read_csv("C:\\DataSets\\StockAnalysis\\dhaval\\Outputs\\last24months\\last24months_resultdates.csv")

df_result = df_result_main[df_result_main['Symbol'] == STOCK_SYMBOL]

result_date = df_result['BoardMeetingDate']
announce_date = df_result['DisplayDate']

#list to store result date for both 2017 and 2018
result_date_lst = []

for i in result_date:
    result_date_lst.append(i)
    #print(i)
print(result_date_lst)

#list to store announcement date for both 2017 and 2018
announce_date_lst = []

for i in announce_date:
    announce_date_lst.append(i)
    #print(i)
print(announce_date_lst)

#convert to datetime
df_result['DisplayDate'] = pd.to_datetime(df_result['DisplayDate'])
df_result['BoardMeetingDate'] = pd.to_datetime(df_result['BoardMeetingDate'])

df_result['year'] = pd.DatetimeIndex(df_result['DisplayDate']).year #create new column to store year

df_result_2017 = df_result[df_result['year'] == 2017]#create df_result for 2017
df_result_2018 = df_result[df_result['year'] == 2018]#create df_result for 2018

#retrieve result date and announcement date separately for 2017 and 2018
result_date_2017 = df_result_2017['BoardMeetingDate']
result_date_2018 = df_result_2018['BoardMeetingDate']
announce_date_2017 = df_result_2017['DisplayDate']
announce_date_2018 = df_result_2018['DisplayDate']

#list to store result dates
result_date_lst_2017 = []
result_date_lst_2018 = []

for i in result_date_2017:
    #i = i.strftime('%d/%m/%Y')
    result_date_lst_2017.append(i)
    #print(i)
print(result_date_lst_2017)


for i in result_date_2018:
    #i = i.strftime('%d/%m/%Y')
    result_date_lst_2018.append(i)
    #print(i)
print(result_date_lst_2018)

#lists to store announcement dates
announce_date_lst_2017 = []
announce_date_lst_2018 = []

for i in announce_date_2017:
    #i = i.strftime('%d/%m/%Y')
    announce_date_lst_2017.append(i)
    #print(i)
print(announce_date_lst_2017)

for i in announce_date_2018:
    #i = i.strftime('%d/%m/%Y')
    announce_date_lst_2018.append(i)
    #print(i)
print(announce_date_lst_2018)

#create daily resampled data
daily_resampled_open = df.open.resample('D').mean()
daily_resampled_high = df.high.resample('D').mean()
daily_resampled_low = df.low.resample('D').mean()
daily_resampled_close = df.close.resample('D').mean()
daily_resampled_volume = df.Volume.resample('D').mean()

#interpolate with linear method for missing values
daily_resampled_open_interpolated = daily_resampled_open.interpolate(method='linear')
daily_resampled_high_interpolated = daily_resampled_high.interpolate(method='linear')
daily_resampled_low_interpolated = daily_resampled_low.interpolate(method='linear')
daily_resampled_close_interpolated = daily_resampled_close.interpolate(method='linear')
daily_resampled_volume_interpolated = daily_resampled_volume.interpolate(method='linear')

#daily_resampled_close_interpolated['date1']=pd.DatetimeIndex(daily_resampled_close_interpolated['date1'])


#df_test = pd.DataFrame()


daily_resampled_close_interpolated_df = daily_resampled_close_interpolated.to_frame()
daily_resampled_volume_interpolated_df = daily_resampled_volume_interpolated.to_frame()
#daily_resampled_close_interpolated_dict = daily_resampled_close_interpolated.to_dict()


from  datetime import datetime, timedelta

#create table for close and volume dfs
conn = sqlite3.connect('C:\\DataSets\\StockAnalysis\\dhaval\\StockAnalysis.db')
print ("Opened database successfully")
daily_resampled_close_interpolated_df.to_sql('daily_resampled_close_interpolated_df',conn, if_exists = 'replace')
daily_resampled_volume_interpolated_df.to_sql('daily_resampled_volume_interpolated_df',conn, if_exists = 'replace')
#rfmdm = pd.read_sql("select * from RFMDM",conn)
print ("new table got created successfully")


#create empty list for storing results for different dates
result_date_lst_7days_Ago = []
result_date_lst_14days_Ago = []
result_date_lst_7days_After = []
result_date_lst_14days_After = []

from dateutil.parser import parse

for dt in result_date_lst:
    d = parse(dt)
    date_7_days_ago = d - timedelta(days=7)
    result_date_lst_7days_Ago.append(date_7_days_ago)
    
    date_14_days_ago = d - timedelta(days=14)
    result_date_lst_14days_Ago.append(date_14_days_ago)
    
    date_7_days_After = d + timedelta(days=7)
    result_date_lst_7days_After.append(date_7_days_After)
    
    date_14_days_After = d + timedelta(days=7)
    result_date_lst_14days_After.append(date_14_days_After)

print(result_date_lst)
print(result_date_lst_7days_Ago)


#store close price on the result date
close_price_result_date_lst = []

for dt in result_date_lst:
    d = parse (dt)
    #print(d)
    cur = conn.cursor()
    #dt = unicode(d)
    #print(d)
    #cur.execute("SELECT * FROM daily_resampled_close_interpolated_df where date1 = '2017-01-02 00:00:00'")
    cur.execute("SELECT * FROM daily_resampled_close_interpolated_df where date1=?", (d,))
    rows = cur.fetchall()
    for row in rows:
        #print(row[1])
        close_price = row[1]
        print(close_price)
        close_price_result_date_lst.append(int(close_price))
    #print(type(row))
print(close_price_result_date_lst)

#store close price 7 days before result date
close_price_result_date_lst_7days_Ago = []

for d in result_date_lst_7days_Ago:
    #d = parse (dt)
    #print(dt)
    cur = conn.cursor()
    #dt = unicode(d)
    #print(d)
    #cur.execute("SELECT * FROM daily_resampled_close_interpolated_df where date1 = '2017-01-02 00:00:00'")
    cur.execute("SELECT * FROM daily_resampled_close_interpolated_df where date1=?", (str(d),))
    rows = cur.fetchall()
    for row in rows:
        #print(row[1])
        close_price = row[1]
        #print(close_price)
        close_price_result_date_lst_7days_Ago.append(int(close_price))
    #print(type(row))
#print(result_date_lst)
#print(result_date_lst_7days_Ago)
#print(close_price_result_date_lst)
print(close_price_result_date_lst_7days_Ago)


#store close price 14 days before result date
close_price_result_date_lst_14days_Ago = []

for d in result_date_lst_14days_Ago:
    #dt = parse (d)
   # print(dt)
    cur = conn.cursor()
    #dt = unicode(d)
    #print(d)
    #cur.execute("SELECT * FROM daily_resampled_close_interpolated_df where date1 = '2017-01-02 00:00:00'")
    cur.execute("SELECT * FROM daily_resampled_close_interpolated_df where date1=?", (str(d),))
    rows = cur.fetchall()
    for row in rows:
        #print(row[1])
        close_price = row[1]
        #print(close_price)
        close_price_result_date_lst_14days_Ago.append(int(close_price))
    #print(type(row))
#print(result_date_lst)
#print(result_date_lst_14days_Ago)
#print(close_price_result_date_lst)
print(close_price_result_date_lst_14days_Ago)

#store close price 7 days after result date
close_price_result_date_lst_7days_After = []

for d in result_date_lst_7days_After:
    #dt = parse (d)
   # print(dt)
    cur = conn.cursor()
    #dt = unicode(d)
    #print(d)
    #cur.execute("SELECT * FROM daily_resampled_close_interpolated_df where date1 = '2017-01-02 00:00:00'")
    cur.execute("SELECT * FROM daily_resampled_close_interpolated_df where date1=?", (str(d),))
    rows = cur.fetchall()
    for row in rows:
        #print(row[1])
        close_price = row[1]
        #print(close_price)
        close_price_result_date_lst_7days_After.append(int(close_price))
    #print(type(row))
#print(result_date_lst)
#print(result_date_lst_7days_After)
#print(close_price_result_date_lst)
print(close_price_result_date_lst_7days_After)


#store close price 14 days after result date
close_price_result_date_lst_14days_After = []

for d in result_date_lst_14days_After:
    #dt = parse (d)
   # print(dt)
    cur = conn.cursor()
    #dt = unicode(d)
    #print(d)
    #cur.execute("SELECT * FROM daily_resampled_close_interpolated_df where date1 = '2017-01-02 00:00:00'")
    cur.execute("SELECT * FROM daily_resampled_close_interpolated_df where date1=?", (str(d),))
    rows = cur.fetchall()
    for row in rows:
        #print(row[1])
        close_price = row[1]
        #print(close_price)
        close_price_result_date_lst_14days_After.append(int(close_price))
    #print(type(row))
#print(result_date_lst)
#print(result_date_lst_14days_After)
#print(close_price_result_date_lst)
print(close_price_result_date_lst_14days_After)


#store volume on the result date
volume_result_date_lst = []


for dt in result_date_lst:
    d = parse (dt)
   # print(dt)
    cur = conn.cursor()
    #dt = unicode(d)
    #print(d)
    #cur.execute("SELECT * FROM daily_resampled_close_interpolated_df where date1 = '2017-01-02 00:00:00'")
    cur.execute("SELECT * FROM daily_resampled_volume_interpolated_df where date1=?", (d,))
    rows = cur.fetchall()
    for row in rows:
        #print(row[1])
        volume = row[1]
        #print(close_price)
        volume_result_date_lst.append(int(volume))
    #print(type(row))
print(volume_result_date_lst)


#store volume 7 days before result date
volume_result_date_lst_7days_Ago = []

for d in result_date_lst_7days_Ago:
    #dt = parse (d)
   # print(dt)
    cur = conn.cursor()
    #dt = unicode(d)
    #print(d)
    #cur.execute("SELECT * FROM daily_resampled_close_interpolated_df where date1 = '2017-01-02 00:00:00'")
    cur.execute("SELECT * FROM daily_resampled_volume_interpolated_df where date1=?", (str(d),))
    rows = cur.fetchall()
    for row in rows:
        #print(row[1])
        close_price = row[1]
        #print(close_price)
        volume_result_date_lst_7days_Ago.append(int(volume))
    #print(type(row))
#print(result_date_lst)
#print(result_date_lst_7days_Ago)
#print(volume_result_date_lst)
print(volume_result_date_lst_7days_Ago)


#store volume 14 days before result date
volume_result_date_lst_14days_Ago = []

for d in result_date_lst_14days_Ago:
    #dt = parse (d)
   # print(dt)
    cur = conn.cursor()
    #dt = unicode(d)
    #print(d)
    #cur.execute("SELECT * FROM daily_resampled_close_interpolated_df where date1 = '2017-01-02 00:00:00'")
    cur.execute("SELECT * FROM daily_resampled_volume_interpolated_df where date1=?", (str(d),))
    rows = cur.fetchall()
    for row in rows:
        #print(row[1])
        close_price = row[1]
        #print(close_price)
        volume_result_date_lst_14days_Ago.append(int(volume))
    #print(type(row))
#print(result_date_lst)
#print(result_date_lst_14days_Ago)
#print(volume_result_date_lst)
print(volume_result_date_lst_14days_Ago)


#store volume 7 days after result date
volume_result_date_lst_7days_After = []

for d in result_date_lst_7days_After:
    #dt = parse (d)
   # print(dt)
    cur = conn.cursor()
    #dt = unicode(d)
    #print(d)
    #cur.execute("SELECT * FROM daily_resampled_close_interpolated_df where date1 = '2017-01-02 00:00:00'")
    cur.execute("SELECT * FROM daily_resampled_volume_interpolated_df where date1=?", (str(d),))
    rows = cur.fetchall()
    for row in rows:
        #print(row[1])
        close_price = row[1]
        #print(close_price)
        volume_result_date_lst_7days_After.append(int(volume))
    #print(type(row))
#print(result_date_lst)
#print(result_date_lst_7days_After)
#print(volume_result_date_lst)
print(volume_result_date_lst_7days_After)


#store volume 14 days after result date
volume_result_date_lst_14days_After = []

for d in result_date_lst_14days_After:
    #dt = parse (d)
   # print(dt)
    cur = conn.cursor()
    #dt = unicode(d)
    #print(d)
    #cur.execute("SELECT * FROM daily_resampled_close_interpolated_df where date1 = '2017-01-02 00:00:00'")
    cur.execute("SELECT * FROM daily_resampled_volume_interpolated_df where date1=?", (str(d),))
    rows = cur.fetchall()
    for row in rows:
        #print(row[1])
        close_price = row[1]
        #print(close_price)
        volume_result_date_lst_14days_After.append(int(volume))
    #print(type(row))
#print(result_date_lst)
#print(result_date_lst_14days_After)
#print(volume_result_date_lst)
print(volume_result_date_lst_14days_After)

conn.close()

#create dataframe and store the lists created above

df_result_date_anlys = pd.DataFrame({'CP_ResultDate':close_price_result_date_lst})
df_result_date_anlys['Symbol'] = STOCK_SYMBOL
df_result_date_anlys['ResultDate'] = pd.Series(result_date_lst)
df_result_date_anlys['CP_ResultDate_7DaysAgo'] = pd.Series(close_price_result_date_lst_7days_Ago)
df_result_date_anlys['CP_ResultDate_14DaysAgo'] = pd.Series(close_price_result_date_lst_14days_Ago)
df_result_date_anlys['CP_ResultDate_7DaysAfter'] = pd.Series(close_price_result_date_lst_7days_After)
df_result_date_anlys['CP_ResultDate_14DaysAfter'] = pd.Series(close_price_result_date_lst_14days_After)

df_result_date_anlys['Volume_ResultDate'] = pd.Series(volume_result_date_lst)
df_result_date_anlys['Volume_ResultDate_7DaysAgo'] = pd.Series(volume_result_date_lst_7days_Ago)
df_result_date_anlys['Volume_ResultDate_14DaysAgo'] = pd.Series(volume_result_date_lst_14days_Ago)
df_result_date_anlys['Volume_ResultDate_7DaysAfter'] = pd.Series(volume_result_date_lst_7days_After)
df_result_date_anlys['Volume_ResultDate_14DaysAfter'] = pd.Series(volume_result_date_lst_14days_After)
#df_result_date_anlys['ClosePrice'] = close_price_result_date_lst
#check if the file already exists with data
csv_filename = "C:\\DataSets\\StockAnalysis\\dhaval\\df_result_date_anlys.csv"
print(df_result_date_anlys)
if (path.exists(csv_filename)):
    df_result_date_anlys.to_csv(csv_filename, mode = 'a', header = False)
    print("file is appended")
else:
    df_result_date_anlys.to_csv(csv_filename)
    print("file is created")
#df_result_date_anlys.to_csv("C:\\DataSets\\StockAnalysis\\dhaval\\df_result_date_anlys.csv")

#plotting for 2017 and 2018 combined
fig, ax = plt.subplots(figsize = (20,10))
#plt.figure(figsize=(20,10))
daily_resampled_close_interpolated.plot()
#i = pd.Timestamp('2017-05-10')
for i in result_date:
    d1 = pd.Timestamp(i)
    #print(d)
    plt.axvline(d1,color='r')
    #plt.xlabel(d)
#plt.axvline(pd.Timestamp('2017-05-10'),color='r')
for j in announce_date:
    d2 = pd.Timestamp(j)
    #print(d)
    plt.axvline(d2,color='g')
    #plt.xlabel(d)
plt.title(STOCK_SYMBOL)
plt.xlabel("Date")
plt.ylabel("ClosePrice")
plt.figtext(0.5, -0.1,"Announcement Date is", horizontalalignment='center', fontsize=12)
plt.figtext(0.5, -0.2,announce_date_lst, horizontalalignment='center', fontsize=12)
plt.figtext(0.5, -0.3,"Result Date is", horizontalalignment='center', fontsize=12)
plt.figtext(0.5, -0.4,result_date_lst, horizontalalignment='center', fontsize=12)
ax.legend()
plt.savefig("C:\\datasets\\StockAnalysis\\dhaval\\ResultsSaveFigs\\" + STOCK_SYMBOL + "Result_2017_2018.jpg",bbox_inches = "tight")

#separate 2017 and 2018 records
daily_resampled_close_interpolated_2017 = daily_resampled_close_interpolated['2017']
daily_resampled_close_interpolated_2018 = daily_resampled_close_interpolated['2018']

#2017 plotting
fig, ax = plt.subplots(figsize = (20,10))
#plt.figure(figsize=(20,10))
daily_resampled_close_interpolated_2017.plot()
#i = pd.Timestamp('2017-05-10')
for i in result_date:
    d1 = pd.Timestamp(i)
    #print(d)
    plt.axvline(d1,color='r')
    #plt.xlabel(d)
for j in announce_date:
    d2 = pd.Timestamp(j)
    #print(d)
    plt.axvline(d2,color='g')
    #plt.xlabel(d)
title = STOCK_SYMBOL + '2017'
plt.title(title)
plt.xlabel("Date")
plt.ylabel("ClosePrice")
plt.figtext(0.5, -0.1,"Announcement Date is", horizontalalignment='center', fontsize=12)
plt.figtext(0.5, -0.2,announce_date_lst_2017, horizontalalignment='center', fontsize=12)
plt.figtext(0.5, -0.3,"Result Date is", horizontalalignment='center', fontsize=12)
plt.figtext(0.5, -0.4,result_date_lst_2017, horizontalalignment='center', fontsize=12)
ax.legend()
#plt.show();
plt.savefig("C:\\datasets\\StockAnalysis\\dhaval\\ResultsSaveFigs\\" + STOCK_SYMBOL + "Result_2017.jpg",bbox_inches = "tight")
print("2017 plot is saved")


#2018 plotting
fig, ax = plt.subplots(figsize = (20,10))
#plt.figure(figsize=(20,10))
daily_resampled_close_interpolated_2018.plot()
#i = pd.Timestamp('2017-05-10')
for i in result_date:
    d1 = pd.Timestamp(i)
    #print(d)
    plt.axvline(d1,color='r')
    #plt.xlabel(d)
for j in announce_date:
    d2 = pd.Timestamp(j)
    #print(d)
    plt.axvline(d2,color='g')
    #plt.xlabel(d)
title = STOCK_SYMBOL + '2018'
plt.title(title)
plt.xlabel("Date")
plt.ylabel("ClosePrice")
plt.figtext(0.5, -0.1,"Announcement Date is", horizontalalignment='center', fontsize=12)
plt.figtext(0.5, -0.2,announce_date_lst_2018, horizontalalignment='center', fontsize=12)
plt.figtext(0.5, -0.3,"Result Date is", horizontalalignment='center', fontsize=12)
plt.figtext(0.5, -0.4,result_date_lst_2018, horizontalalignment='center', fontsize=12)
ax.legend()
#plt.show();
plt.savefig("C:\\datasets\\StockAnalysis\\dhaval\\ResultsSaveFigs\\" + STOCK_SYMBOL + "Result_2018.jpg",bbox_inches = "tight")
print("2018 plot is saved")

    