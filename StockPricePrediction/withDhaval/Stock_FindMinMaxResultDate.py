#This program is used to check threshold from Announcement Date
import pandas as pd
from os import path
import matplotlib.pyplot as plt
import numpy as np

df_main = pd.read_csv('C:\\DataSets\\StockAnalysis\\dhaval\\2017-18.csv', usecols = range(0,8))
df_main.columns = ['Symbol', 'date', 'hr:min', 'open', 'high', 'low', 'close', 'Volume']

stock_list_df = pd.read_csv("C:\\datasets\\StockAnalysis\\dhaval\\nifty47StockSymbols.csv")
#stock_list_df = pd.read_csv("C:\\datasets\\StockAnalysis\\dhaval\\niftyStockSymbols_sample.csv")
stock_list = stock_list_df['Symbol']


#stock_list = ['ACC','CIPLA']

csv_filename1 = "C:\\datasets\\StockAnalysis\\dhaval\\Min_Max\\ResultDate_After7DaysAllRecords.csv"
csv_filename2 = "C:\\datasets\\StockAnalysis\\dhaval\\Min_Max\\ResultDate_All_Stocks_After7Days_Max.csv"


df = df_main.copy(deep = True)
df_columns = ['Stock_Symbol', 'Result_Date', 'ResultDateClosePrice', 'Closing_Price_Date', 'ClosePrice', 'Perc_change']

df_all = pd.DataFrame()#it will hold the final details for all the stocks

#STOCK_SYMBOL = 'ACC'

def manage_threshold(df,STOCK_SYMBOL):

    
    df = df[df['Symbol'] == STOCK_SYMBOL]
    print(STOCK_SYMBOL)
    
    #min_ind_stock_lst = []
    
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
    cols_to_drop = ['date', 'year', 'month', 'day', 'hour', 'minute', 'Symbol', 'hr:min', 'date1']
    df.drop(cols_to_drop, axis=1, inplace=True)#delete the non-required columns
    
    #save to csv
    df.to_csv("C:\\DataSets\\StockAnalysis\\dhaval\\company_csvs\\" + STOCK_SYMBOL + ".csv")
    
    #create daily resampled data
    daily_resampled_close = df.close.resample('D').mean()
        
    #interpolate with linear method for missing values
    daily_resampled_close_interpolated = daily_resampled_close.interpolate(method='linear')
    
    #get result dates
    df_result_main = pd.read_csv("C:\\DataSets\\StockAnalysis\\dhaval\\Outputs\\last24months\\last24months_resultdates.csv")
    
    df_result = df_result_main[df_result_main['Symbol'] == STOCK_SYMBOL]
      
    #convert to datetime
    df_result['DisplayDate'] = pd.to_datetime(df_result['DisplayDate'])
    df_result['BoardMeetingDate'] = pd.to_datetime(df_result['BoardMeetingDate'])
    
    df_result['year'] = pd.DatetimeIndex(df_result['DisplayDate']).year #create new column to store year
    
    df_result_2017 = df_result[df_result['year'] == 2017]#create df_result for 2017
    df_result_2018 = df_result[df_result['year'] == 2018]#create df_result for 2018
    
    #retrieve result date and announcement date separately for 2017 and 2018
    result_date_2017 = df_result_2017['BoardMeetingDate']
    result_date_2018 = df_result_2018['BoardMeetingDate']
    #announce_date_2017 = df_result_2017['DisplayDate']
    #announce_date_2018 = df_result_2018['DisplayDate']
    
    #list to store result dates
    result_date_lst_2017 = []
    result_date_lst_2018 = []
    result_date_lst_2017_2018 = []
    
    for i in result_date_2017:
        #i = i.strftime('%d/%m/%Y')
        result_date_lst_2017.append(i)
        result_date_lst_2017_2018.append(i)
        #print(i)
    #print(result_date_lst_2017)
    
    
    for i in result_date_2018:
        #i = i.strftime('%d/%m/%Y')
        result_date_lst_2018.append(i)
        result_date_lst_2017_2018.append(i)
        #print(i)
    #print(result_date_lst_2018)
    #print("result_date_lst_2017_2018 is")
    print(result_date_lst_2017_2018)
    
    import datetime
    
    df_threshold4 = pd.DataFrame()
    
    print("result_date_lst_2017_2018 is")
    print(result_date_lst_2017_2018)
    #result_date_lst_2017 = result_date_lst_2017[0]
    
    #result_date_lst_2017_2018_sample = result_date_lst_2017_2018[0:2]
 
    df_threshold4 = pd.DataFrame()
    
    #result_date_lst_2017_2018_sample = result_date_lst_2017_2018[0:3]
    
    for i in result_date_lst_2017_2018:
        
        df_threshold2 = pd.DataFrame()
        #min_lst = []
        print("result date is")
        #dt1 = datetime.datetime.strptime(i, '%d-%b-%Y')
        #i = result_date_lst_2017_2018[2]
        dt1 = i
        print(dt1)
        #dt1 = result_date_lst_2017_2018[0]
        
        dt1_year = dt1.year
        #print(dt1_year)

        if (dt1_year == 2019):
            break

        price1 = daily_resampled_close_interpolated[dt1]
        price1 = price1.astype(int)
        #print(price1)
        close_price = []
        #date_range = []
        per_change = []
        #check_2019 = False
        #sub_list= []
        for a in range(0,7):#loop through for next 14 days afte result date
            a = a+1
            dt2 = dt1 + datetime.timedelta(days=a)
            print("Date is")
            print(dt2)
            dt2_year = dt2.year
            #print("dt2_year is")
            #print(dt2_year)
 
            if (dt2_year == 2019):
                break
 
            #print(type(dt2))
            #dt2 = dt2.strftime('%d-%b-%Y')
            #date_range.append(dt2)
            price2 = daily_resampled_close_interpolated[dt2]
            price2 = price2.astype(int)
            #print(price2)
            close_price.append(price2)
            change = ((price2-price1)/price1)*100
            change = change.astype(int)
            print("change is")
            print(change)
            per_change.append(change)
            #print(price2)
            #print(dt2)
            #print(change)
            dict_close_price = {
                                     'Stock_Symbol': STOCK_SYMBOL,
                                     'Result_Date' : dt1,
                                     'ResultDateClosePrice' : price1,
                                     'Date':dt2, 
                                     'ClosePrice':price2, 
                                     'Perc_change': change
                                }
            
            print("dict_close_price is")
            print(dict_close_price)
            df_threshold1 = pd.DataFrame(dict_close_price, index=[0])
            print("df_threshold1 is")
            print(df_threshold1)
            print("df_threshold2 is")
            df_threshold2 = pd.concat([df_threshold2, df_threshold1])
            print(df_threshold2)#This will hold details for next # of days after result date
            
        if (path.exists(csv_filename1)):
            df_threshold2.to_csv(csv_filename1, mode = 'a')
            print("file is appended")
        else:
            df_threshold2.to_csv(csv_filename1)
            print("file is created")

        perc_change_s = df_threshold2['Perc_change']
        min_max = perc_change_s.max()
        min_max_Close_Price_index = list(np.where(df_threshold2["Perc_change"] == min_max)[0])
        min_max_Close_Price_index_1stOcc = min_max_Close_Price_index[0]
        print(min_max_Close_Price_index)
        print(min_max_Close_Price_index_1stOcc)
        
        min_max_Closing_Price_Date = df_threshold2.iloc[min_max_Close_Price_index_1stOcc].Date
        print(min_max_Closing_Price_Date)
        min_max_Closing_Price = df_threshold2.iloc[min_max_Close_Price_index_1stOcc].ClosePrice
        print(min_max_Closing_Price)
        min_max_perc_change = df_threshold2.iloc[min_max_Close_Price_index_1stOcc].Perc_change
        print(min_max_perc_change)

        dict_close_price_min_max = {
                             'Stock_Symbol': [STOCK_SYMBOL],
                             'Result_Date' : [dt1],
                             'ResultDateClosePrice' : [price1],
                             'Min_Max__Closing_Price_Date': [min_max_Closing_Price_Date], 
                             'ClosePrice': [min_max_Closing_Price], 
                             'Perc_change': [min_max_perc_change]
                             }
        print("dict_close_price_min_max is")
        print(dict_close_price_min_max)#it will hold one record for each record date
        df_threshold3 = pd.DataFrame(dict_close_price_min_max, index=[0])
        print("df_threshold3 is")
        print(df_threshold3)
        print("df_threshold4 is")
        df_threshold4 = pd.concat([df_threshold4, df_threshold3])#this will hold for each stock, min/max after # of days of result day
        print(df_threshold4)
       
    return df_threshold4

for symbol in stock_list:
    print(symbol)
    df_threshold = manage_threshold(df,symbol)
    df_all = pd.concat([df_all, df_threshold])

print("df_all is")
print(df_all)

df_all.columns = df_columns #set columns


if (path.exists(csv_filename2)):
    df_all.to_csv(csv_filename2, mode = 'a', header = False)
    print("file is appended")
else:
    df_all.to_csv(csv_filename2)
    print("file is created")
