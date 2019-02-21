#Importing packages
from selenium import webdriver
import pandas as pd
from bs4 import BeautifulSoup
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"
from selenium.webdriver.common.keys import Keys

def read_input_file():
    df_input = pd.read_csv("C:\\DataSets\\CreditAnalysis\\InputCompanyDetails.csv")
    CompanyName_Lst = df_input.loc[:,'CompanyName']
    return CompanyName_Lst
    
    
def process_html(rownum):
    
    #get the Company Overview from the xpath
    companyOverview_element = driver.find_elements_by_xpath('//*[@id="AppCompany_compDescription"]')[0]
    companyOverview_element = companyOverview_element.text

    #Selenium hands the page source to Beautiful Soup
    soup=BeautifulSoup(driver.page_source, 'html.parser')
    df_company_details = create_empty_df_companyOverview()
    df_director = create_empty_df_directorList()
    retreive_company_overview(soup, df_company_details)#function to retreive company overview details
    retreive_director_details(soup,df_director)#function to retreive director details
    
def create_empty_df_companyOverview():
    COLUMN_NAMES = ['Company CIN','Age (Incorp. Date)','Company Status','Company Type','Sub.Category','Email ID','Company Website',
                    'Industry', 'Paid up Capital', 'Open Charges', 'Directors', 'Signatories', 'Last AGM Date', 'Balance Sheet Date', 
                    'Profit After Tax', 'Address']
    df_company_details = pd.DataFrame(columns = COLUMN_NAMES)
    df_company_details.to_csv("C:\\DataSets\\CreditAnalysis\\company_overview.csv", mode = 'w', header=True)#creat the template
    return df_company_details

def create_empty_df_directorList():
    COLUMN_NAMES = ['Name','DIN','Designation','Appointment Date','Capitalization (â‚¹. Lakhs)',
                    'Total Directorships','Disqualified u/s 164(2)','DIN Deactivated']
    df_director = pd.DataFrame(columns = COLUMN_NAMES)
    df_director.to_csv("C:\\DataSets\\CreditAnalysis\\director_details.csv", mode = 'w', header=True)#create the template
    return df_director
        
def retreive_company_overview(soup,rownum):
    
    #get the CompanyOverview
    company_overview_tbl = soup.find('table', id = 'CompanyOverview')
    
    #Generate Lists
    A = []
    B = []
    C = []
    D = []

    #add the table values into lists
    for row in company_overview_tbl.findAll("tr"):
        cells = row.findAll("td")
        #print(cells)
        A.append(cells[0].find(text=True))
        B.append(cells[1].find(text=True))
        C.append(cells[2].find(text=True))
        D.append(cells[3].find(text=True))
    
        #create rows and columns to be created in dataframe
        #columns_headers = A + C
        columns_values = B + D

        
        #create touple
        #list_of_touples = list(zip(columns_headers, columns_values))
        
        #create dataframe from the list of touple
        #df = pd.DataFrame(list_of_touples)  
        df=pd.DataFrame(columns_values)
        #transpose the dataframe to make rows as columns
        df_t = df.transpose()
    #append to csv
    df_t.to_csv("C:\\DataSets\\CreditAnalysis\\company_overview.csv", mode = 'a', header=False)
        
        #make the 2nd row as header
        #headers = df_t.iloc[0]
        
# =============================================================================
#         if (rownum == 1):#create the dataframe
#             print("rownum1")
#             df_company_details  = pd.DataFrame(df_t.values[1:], columns=headers)
#         else:
#             #append the data into the dataframe
#             print("NotRowNum1")
#             print(rownum)
#             df_company_details.append(df_t.values[1:])
# =============================================================================
        #save into csv
        #df_company_details.to_csv("C:\\DataSets\\CreditAnalysis\\company_overview.csv")

def retreive_director_details(soup,rownum):

        #retrieve director details
        director_tbl = soup.find('table', id = 'DataTables_Table_0')
        #get the column headers
        column_headers = [th.getText() for th in 
                          director_tbl.findAll('tr', limit=2)[0].findAll('th')]
        
        #get teh data rows
        data_rows = director_tbl.findAll('tr')[1:]  # skip the first 2 header rows
        
        director_data = [[td.getText() for td in data_rows[i].findAll('td')]
                    for i in range(len(data_rows))]
        
        #if(rownum == 1):
            #create director's dataframe
        df_director = pd.DataFrame(director_data, columns = column_headers)
        #else:
            #append the data into the dataframe
            
        #append to csv
        df_director.to_csv("C:\\DataSets\\CreditAnalysis\\director_details.csv", mode = 'a', header=False)

if __name__ == "__main__":
    companyNames = read_input_file()#get the companynames from the files
    #print(companyNames)
    cnt = 0
    for cname in companyNames:
        print(cname)
        cnt = cnt+1#increment the cnt for each loop through
        print(cnt)
        search_query = cname
        driver = webdriver.Chrome('C:\\chromedriver\\chromedriver.exe')        # alternatively: browser = webdriver.Chrome(pathtowebdriver)
        driver.implicitly_wait(10) # seconds
        driver.get("about:blank")
        driver.get("https://www.instafinancials.com/")
        search_textbox = driver.find_element_by_xpath("//*[@id='txtCompanySearch']")   #XPATH can be found with developer tools in browsers
        search_textbox.send_keys(search_query)
        driver.find_element_by_xpath('//*[@id="compSearchResults"]').click()
        process_html(cnt)
        driver.close()
