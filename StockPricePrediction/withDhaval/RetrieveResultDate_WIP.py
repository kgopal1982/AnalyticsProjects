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
        #print(i)
        #print(i+11)
        d_date = text[i:i+11]
        #print(text[i:i+11])
        display_date_lst.append(d_date)
    #print(display_date_lst)
    return display_date_lst

#retreive Company Symbol
def retrieve_company_symbol(text):
    iter = re.finditer(r"\Symbol\b", text)#find out index of Symbol
    indices_start = [m.start(0) for m in iter]
    #print(indices_start)
    
    comp_symbol_lst = []
    
    #loop through each starting index of display dates and store in the list display_date
    for i in indices_start:
        i = i+ 8
        #print(i)
        #print(i+11)
        symb = text[i:i+3]
        #print(symb)
        comp_symbol_lst.append(symb)
    #print(comp_symbol_lst)
    return comp_symbol_lst
#retreive display date<<<


if __name__ == "__main__":
    #go through each file name
    for filename in glob.glob(r"C:\\datasets\\StockAnalysis\\dhaval\\company_results_last24\\*.html"):
        text_file_name = filename.strip()
        print(text_file_name)
        df = pd.DataFrame()# create empty dataframe        
        csv_fileName = "C:\\DataSets\\StockAnalysis\\dhaval\\Outputs\\resultdates.csv" #path of the output csv file
        with open (text_file_name) as f:
            text = f.read().strip()
            board_meeting_date_lst = retrieve_board_meeting_date(text) #get list of boarding meeting date
            print(board_meeting_date_lst)
            display_date_lst = retrieve_display_date(text)#get list of display date
            print(display_date_lst)
            comp_symbol_lst = retrieve_company_symbol(text)# get list of company symbol
            print(comp_symbol_lst)
            #create dataframe and save into csv
            df['Symbol'] = comp_symbol_lst
            df['BoardMeetingDate'] = board_meeting_date_lst
            df['DisplayDate'] = display_date_lst
            #print(df)
            
            #check if the file already exists with data
            if (path.exists(csv_fileName)):
                df.to_csv(csv_fileName, mode = 'a', header = False)
                print("file is appended")
            else:
                df.to_csv(csv_fileName)
                print("file is created")
            print(df)