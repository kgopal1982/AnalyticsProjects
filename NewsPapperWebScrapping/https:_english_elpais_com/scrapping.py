# importing the necessary packages
import requests
from bs4 import BeautifulSoup
import os

raw_html= open("C:\\Users\\ekrigos\\Desktop\\DataS\\Projects\\web_scrapping\\raw_file_elpais.html","r", encoding="utf-8").read()
soup1 = BeautifulSoup(raw_html, 'html5lib')
print(soup1)

soup_html_file= open("C:\\Users\\ekrigos\\Desktop\\DataS\\Projects\\web_scrapping\\raw_file_elpais_soup.html","w")
soup_html_file.write(str(soup1))
soup_html_file.close()

headlines = soup1.find_all('h2', class_='headline')
print(headlines)

# Scraping the first 5 headlines
number_of_headlines = 5
# Empty lists for content, links and titles
news_contents = []
list_links = []
list_titles = []
list_hyperlinks = []

write_path_hyperlink = "C:\\Users\\ekrigos\\Desktop\\DataS\\Projects\\web_scrapping\\hyperlink_file.html"

if os.path.exists(write_path_hyperlink):
  os.remove(write_path_hyperlink)
  
mode = 'a' if os.path.exists(write_path_hyperlink) else 'w'
with open(write_path_hyperlink, mode) as f1:
    #f.write("%r\n" %hyper_link)
    f1.write('The headlines for newspaper:   ' + 'https://english.elpais.com/')
    f1.write('<br/>')
    #f.write("")
f1.close()

import numpy as np
from ExtractiveSummary_Scrapping import return_top_ranked_sentences

#number_of_headlines
for n in np.arange(0, number_of_headlines):
    
    #n = 1
    print(n)
    list_paragraphs = []
    # Getting the link of the article
    #n = 1
    link = headlines[n].find('a')['href']
    url1 = "https://english.elpais.com/"
    link1 = url1+link
    list_links.append(link1)
    #print("List of headlines links")
    #print(list_links)
    
#    headlines_file_link= open("C:\\Users\\ekrigos\\Desktop\\DataS\\Projects\\web_scrapping\\headlines_file_link.html","w")
#    headlines_file_link.write(str(list_links))
#    headlines_file_link.close()
    
    # Getting the title
    title = headlines[n].find('a').get_text()
    list_titles.append(title)
    #print("List of title")
    #print(list_titles)
    
#    headlines_file= open("C:\\Users\\ekrigos\\Desktop\\DataS\\Projects\\web_scrapping\\headlines_file.html","w")
#    headlines_file.write(str(list_titles))
#    headlines_file.close()
    
    head_link = list_links[n]
    print(head_link)
    
    head_text = list_titles[n]
    print(head_text)
    
    ####
    #Extract Contents
    article = requests.get(link1)
    article_content = article.content
    soup_article = BeautifulSoup(article_content, 'html5lib')
    print("n is=")
    print(n)
    print("Article is")
    print(soup_article)
    soup_html_file_content= open("C:\\Users\\ekrigos\\Desktop\\DataS\\Projects\\web_scrapping\\raw_file_elpais_soup_content.html","a")
    soup_html_file_content.write(str(soup_article))
    soup_html_file_content.close()
    body = soup_article.find_all('div', class_='article')
    soup_html_file_content_body= open("C:\\Users\\ekrigos\\Desktop\\DataS\\Projects\\web_scrapping\\raw_file_elpais_soup_content_body.html","a")
    soup_html_file_content_body.write(str(body))
    soup_html_file_content_body.close()
    x = body[0].find_all('p')
     
    # Unifying the paragraphs
    list_paragraphs = []
    for p in np.arange(0, len(x)):
        paragraph = x[p].get_text()
        list_paragraphs.append(paragraph)
        final_article = " ".join(list_paragraphs)
         
    news_contents.append(final_article)
    print("news_content is")
    print(news_contents)
    
    news_contents_txt = open("C:\\Users\\ekrigos\\Desktop\\DataS\\Projects\\web_scrapping\\news_contents_txt.txt","a")
    news_contents_txt.write(str(body))
    news_contents_txt.close()
    
    
    top_ranked_sentences = return_top_ranked_sentences(news_contents[n])
    print("top_ranked_sentences is ")
    #print(top_ranked_sentences)
#    for item in top_ranked_sentences:
#        print(item)
    #write to file first and then read
    write_path_summary_temp = "C:\\Users\\ekrigos\\Desktop\\DataS\\Projects\\web_scrapping\\write_path_summary"
    write_path_summary = write_path_summary_temp + '_' + str(n) + '.html'
    print(write_path_summary)

    if os.path.exists(write_path_summary):
      os.remove(write_path_summary)
    else:
      print("The file does not exist")
      
    mode = 'a' if os.path.exists(write_path_summary) else 'w'
    with open(write_path_summary, mode) as f2:
       for item in top_ranked_sentences:
           f2.write(item)
           f2.write('<br/>')
    f2.close()
    
    #now read the contents
    mode = 'r'
    with open(write_path_summary, mode) as f3:
        top_ranked_text = f3.read()
    f3.close()
    print("top_ranked_text is")
    print(top_ranked_text)
     
    #news_content_file= open("C:\\Users\\ekrigos\\Desktop\\DataS\\Projects\\web_scrapping\\news_content.txt","w")
    #news_content_file.write(str(news_contents))
    #news_content_file.close()
    
    
    #########
    
    hyperlink_format = '<a href="{link}"target="_blank">{text}</a>'
    #h1 = hyperlink_format.format(link='http://www.google.com', text='linky text')
    hyper_link = hyperlink_format.format(link= head_link, text= head_text)
    
    #for summary
    hyperlink_format_summary = '<a href="{link}"target="_blank">{text}</a>'
    #h1 = hyperlink_format.format(link='http://www.google.com', text='linky text')
    hyper_link_summary = hyperlink_format_summary.format(link= write_path_summary, text= 'Summary')
    
    mode = 'a' if os.path.exists(write_path_hyperlink) else 'w'
    #mode = "w+"
    with open(write_path_hyperlink, mode) as f:
        #f.write("%r\n" %hyper_link)
        f.write('<br/>'+ hyper_link)
        f.write('<br/>')
        f.write(hyper_link_summary)
        f.write('<br/>')
        #f.write("")
    f.close()
    
    list_hyperlinks.append(hyper_link)

    ##
# =============================================================================
     
 # Reading the content (it is divided in paragraphs)

# =============================================================================

print("list_hyperlinks is")
print(list_hyperlinks)
