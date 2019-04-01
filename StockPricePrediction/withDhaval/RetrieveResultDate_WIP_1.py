import os.path
from os import path
import glob
import re
import pandas as pd

#retreive boardmeeting date
def retrieve_board_meeting_date(text):
    iter = re.finditer(r"\bBoardMeetingDate\b", text)#find out index of BoardMeetingDate
    indices_start = [m.start(0) for m in iter]
    #print(indices_start)
    
    board_meeting_date_lst = []
    
    #loop through each starting index of boardmeeting dates and store in the list board_meeting_date
    for i in indices_start:
        i = i+ 18
        #print(i)
        #print(i+11)
        bm_date = text[i:i+11]
        #print(text[i:i+11])
        board_meeting_date_lst.append(bm_date)
    #print(board_meeting_date_lst)
    return board_meeting_date_lst
    
#retreive display date
def retrieve_display_date(text):
    iter = re.finditer(r"\DisplayDate\b", text)#find out index of DisplayDate
    indices_start = [m.start(0) for m in iter]
    #print(indices_start)
    
    display_date_lst = []
    
    #loop through each starting index of display dates and store in the list display_date
    for i in indices_start:
        i = i+ 13
        d_date = text[i:i+11]
        #print(text[i:i+11])
        display_date_lst.append(d_date)
    #print(display_date_lst)
    return display_date_lst

#retreive Company Symbol
def retrieve_company_symbol(text):
    iter_start = re.finditer(r"\"\b", text)#find out index of "
    indices_start = [m.start(0) for m in iter_start]
    
    iter_end = re.finditer(r"\,\b", text)#find out index of ,
    indices_end = [m.start(0) for m in iter_end]
    #print(indices_start)
    
    #retreive company symbol based on index# of " and '
    s1 = indices_start[0]+1
    s3 = indices_end[2]-1
    symb = text[s1:s3]
    
    return symb
    
#retreive Company Symbol
def retrieve_company_name(text):
    iter_start = re.finditer(r"\"\b", text)#find out index of "
    indices_start = [m.start(0) for m in iter_start]
    
    iter_end = re.finditer(r"\,\b", text)#find out index of ,
    indices_end = [m.start(0) for m in iter_end]
    #print(indices_start)
    
    #retreive company name based on index# of " and '
    s2 = indices_start[1]+1
    s4 = indices_end[3]-1
    comp_name = text[s2:s4]

    return comp_name


if __name__ == "__main__":
    #go through each file name
    for filename in glob.glob(r"C:\\DataSets\\StockAnalysis\\dhaval\\company_results_old\\*.html"):
        text_file_name = filename.strip()
        print(text_file_name)
        df = pd.DataFrame()# create empty dataframe    
        df['Symbol'] = ''
        df['CompanyName'] = ''
        csv_fileName = "C:\\DataSets\\StockAnalysis\\dhaval\\Outputs\\morethan24months\\morethan_24months_resultdates.csv" #path of the output csv file
        with open (text_file_name) as f:
            text = f.read().strip()
            symb = retrieve_company_symbol(text)# get list of company symbol
            comp_name = retrieve_company_name(text)
            display_date_lst = retrieve_display_date(text)#get list of display date
            board_meeting_date_lst = retrieve_board_meeting_date(text)
            print(symb)
            print(comp_name)
            df['DisplayDate'] = display_date_lst
            df['BoardMeetingDate'] = board_meeting_date_lst
            for i in range(len(df)):
                df['Symbol'].values[i] = symb
                df['CompanyName'].values[i] = comp_name
            print(df)
            
#            #check if the file already exists with data
            if (path.exists(csv_fileName)):
                df.to_csv(csv_fileName, mode = 'a', header = False)
                print("file is appended")
            else:
                df.to_csv(csv_fileName)
                print("file is created")