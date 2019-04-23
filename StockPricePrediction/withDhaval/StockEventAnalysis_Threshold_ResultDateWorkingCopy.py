import pandas as pd
from os import path
import matplotlib.pyplot as plt

df_main = pd.read_csv('C:\\DataSets\\StockAnalysis\\dhaval\\2017-18.csv', usecols = range(0,8))
df_main.columns = ['Symbol', 'date', 'hr:min', 'open', 'high', 'low', 'close', 'Volume']

#stock_lst = ['WOCKPHARMA','CNXENERGY','JINDALSTEL','INFRATEL']
stock_list_df = pd.read_csv("C:\\datasets\\StockAnalysis\\dhaval\\nifty47StockSymbols.csv")
#stock_list_df = pd.read_csv("C:\\datasets\\StockAnalysis\\dhaval\\niftyStockSymbols_sample.csv")
stock_list = stock_list_df['Symbol']

stock_list = ['BAJFINANCE']

df = df_main.copy(deep = True)
#stock_list = ['ACC','CIPLA', 'BPCL']

df_threshold_main = pd.DataFrame()

def manage_threshold(df,STOCK_SYMBOL):

    #STOCK_SYMBOL = 'CIPLA'
    df = df[df['Symbol'] == STOCK_SYMBOL]
    print(STOCK_SYMBOL)
    
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
    
    #create daily resampled data
    #daily_resampled_open = df.open.resample('D').mean()
    #daily_resampled_high = df.high.resample('D').mean()
    #daily_resampled_low = df.low.resample('D').mean()
    daily_resampled_close = df.close.resample('D').mean()
    #daily_resampled_volume = df.Volume.resample('D').mean()
    
    #interpolate with linear method for missing values
    #daily_resampled_open_interpolated = daily_resampled_open.interpolate(method='linear')
    #daily_resampled_high_interpolated = daily_resampled_high.interpolate(method='linear')
    #daily_resampled_low_interpolated = daily_resampled_low.interpolate(method='linear')
    daily_resampled_close_interpolated = daily_resampled_close.interpolate(method='linear')
    #daily_resampled_volume_interpolated = daily_resampled_volume.interpolate(method='linear')
    
    
    #daily_resampled_close_interpolated_df = daily_resampled_close_interpolated.to_frame()
    #daily_resampled_volume_interpolated_df = daily_resampled_volume_interpolated.to_frame()
    
    
    #get result dates
    df_result_main = pd.read_csv("C:\\DataSets\\StockAnalysis\\dhaval\\Outputs\\last24months\\last24months_resultdates.csv")
    
    df_result = df_result_main[df_result_main['Symbol'] == STOCK_SYMBOL]
    
    result_date = df_result['BoardMeetingDate']
    
    #list to store result date for both 2017 and 2018
    result_date_lst = []
    
    for i in result_date:
        result_date_lst.append(i)
        #print(i)
    #print(result_date_lst)
    
    #convert to datetime
    df_result['DisplayDate'] = pd.to_datetime(df_result['DisplayDate'])
    df_result['BoardMeetingDate'] = pd.to_datetime(df_result['BoardMeetingDate'])
    
    df_result['year'] = pd.DatetimeIndex(df_result['DisplayDate']).year #create new column to store year
    
    df_result_2017 = df_result[df_result['year'] == 2017]#create df_result for 2017
    df_result_2018 = df_result[df_result['year'] == 2018]#create df_result for 2018
    
    #retrieve result date and announcement date separately for 2017 and 2018
    result_date_2017 = df_result_2017['DisplayDate']
    result_date_2018 = df_result_2018['DisplayDate']
    
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
    print(result_date_lst_2017_2018)
    
    
    #daily_resampled_close_interpolated['2017-01-02']
    #
    #dt1 = '2017-01-02'
    #daily_resampled_close_interpolated[dt1]
    
    import datetime
    
    df_threshold = pd.DataFrame()
    
    #result_date_lst_2017_2018 = ['17-May-2017']
    
    for i in result_date_lst_2017_2018:
        print("result date is")
        print(i)
        #dt1 = datetime.datetime.strptime(i, '%d-%b-%Y')
        dt1 = i
        print(dt1)
        dt1_year = dt1.year
        print(dt1_year)
        if (dt1_year == 2019):
                break
        price1 = daily_resampled_close_interpolated[dt1]
        price1 = price1.astype(int)
        #print(price1)
        close_price = []
        date_range = []
        per_change = []
        #check_2019 = False
        for a in range(0,14):
            a = a+1
            dt2 = dt1 + datetime.timedelta(days=a)
            print(dt2)
            dt2_year = dt2.year
            print("dt2_year is")
            print(dt2_year)
            if (dt2_year == 2019):
                break
            #print(type(dt2))
            #dt2 = dt2.strftime('%d-%b-%Y')
            date_range.append(dt2)
            price2 = daily_resampled_close_interpolated[dt2]
            price2 = price2.astype(int)
            print(price2)
            close_price.append(price2)
            change = ((price2-price1)/price1)*100
            change = change.astype(int)
            print(change)
            if (change > 4):
                print("change is greater than 4")
                break;
            per_change.append(change)
        print(price2)
        print(dt2)
        print(change)
        dict_gt_than_threshold = {
                                 'Stock_Symbol': STOCK_SYMBOL,
                                 'Result_Date' : i,
                                 'ResultDateClosePrice' : price1,
                                 'Threshold_date':dt2, 
                                 'Threshold_ClosePrice':price2, 
                                 'Threshold_perc_change': change
                                 }
        print(dict_gt_than_threshold)
        print(date_range)
        print(close_price)
        print(per_change)
        print("######")
        #df_threshold = pd.DataFrame(dict_gt_than_threhold)
        #print(df_threshold)
        df_threshold1 = pd.DataFrame(dict_gt_than_threshold, index=[0])
        print("df_threshold1 is")
        print(df_threshold1)
        df_threshold1 = df_threshold1[df_threshold1['Threshold_perc_change'] >4]
        print(df_threshold1)
        #df_threhold.append(df)
    
        print("df threshold is ")
        df_threshold = pd.concat([df_threshold, df_threshold1])
        print(df_threshold)
    return df_threshold

for symbol in stock_list:
    print(symbol)
    df_threshold = manage_threshold(df,symbol)
    df_threshold_main = pd.concat([df_threshold_main, df_threshold])

print("df_threshold_main is")
print(df_threshold_main)

csv_filename = "C:\\datasets\\StockAnalysis\\dhaval\\df_threshold_main.csv"
if (path.exists(csv_filename)):
    df_threshold_main.to_csv(csv_filename, mode = 'a', header = False)
    print("file is appended")
else:
    df_threshold_main.to_csv(csv_filename)
    print("file is created")