#https://www.geeksforgeeks.org/python-reading-contents-of-pdf-using-ocr-optical-character-recognition/
#conda install -c conda-forge poppler
#conda install -c conda-forge tesseract

from PIL import Image
import pytesseract
import sys
from pdf2image import convert_from_path 
import os

inputfilepath = "C:\\Users\\ekrigos\\Desktop\\DataS\\REVA\\finalyearProj\\pdf_analysis\\inputs_healthHazard\\"
#outputfilepath = "C:\\Users\\ekrigos\\Desktop\\DataS\\REVA\\finalyearProj\\pdf_analysis\\outputs_text\\"


def convert_to_text(inputfilepath, filename):
    ''' 
    Part #1 : Converting PDF to images 
    '''
 
    
    PDF_file = inputfilepath + filename
    # Store all the pages of the PDF in a variable 
    print("PDF_file is")
    print(PDF_file)
    # Store all the pages of the PDF in a variable 
    pages = convert_from_path(PDF_file, 500) 
    
    # Counter to store images of each page of PDF to image 
    image_counter = 1
    # Iterate through all the pages stored above 
    for page in pages: 
      
        # Declaring filename for each page of PDF as JPG 
        # For each page, filename will be: 
        # PDF page 1 -> page_1.jpg 
        # PDF page 2 -> page_2.jpg 
        # PDF page 3 -> page_3.jpg 
        # .... 
        # PDF page n -> page_n.jpg 
        filename_jpg = filename + '_Page#_' +str(image_counter)
          
        # Save the image of the page in system 
        outputfilename_jpg = inputfilepath + filename_jpg +".jpg"
        page.save(outputfilename_jpg, 'JPEG') 
      
        # Increment the counter to update filename 
        image_counter = image_counter + 1
        
        
    #Part #2 - Recognizing text from the images using OCR 
        
    # Variable to get count of total number of pages 
    filelimit = image_counter-1
    # Creating a text file to write the output 
    outfile = PDF_file + '.txt'
    print("outfile is")
    print(outfile)
      
    # Open the file in append mode so that  
    # All contents of all images are added to the same file 
    f = open(outfile, "a")
    # Iterate from 1 to total number of pages 
    #i=1
    for i in range(1, filelimit + 1): 
      
        # Set filename to recognize text from 
        # Again, these files will be: 
        # page_1.jpg 
        # page_2.jpg 
        # .... 
        # page_n.jpg 
        jpg_filename = inputfilepath + filename + "_Page#_"+str(i)+".jpg"
        print("jpg_filename is")
        print(jpg_filename)
              
        # Recognize the text as string in image using pytesserct 
        text = str(((pytesseract.image_to_string(Image.open(jpg_filename))))) 
      
        # The recognized text is stored in variable text 
        # Any string processing may be applied on text 
        # Here, basic formatting has been done: 
        # In many PDFs, at line ending, if a word can't 
        # be written fully, a 'hyphen' is added. 
        # The rest of the word is written in the next line 
        # Eg: This is a sample text this word here GeeksF- 
        # orGeeks is half on first line, remaining on next. 
        # To remove this, we replace every '-\n' to ''. 
        text = text.replace('-\n', '')     
      
        # Finally, write the processed text to the file. 
        f.write(text) 
        i = i+1
      
    # Close the file after writing all the text. 
    f.close() 
    
    


for filename in os.listdir(inputfilepath):
    if filename.endswith(".pdf"): 
         # print(os.path.join(directory, filename))
        #print(filename)
        #filename = "Q1_wipro_2008_1.pdf"
        #print(filename)
        convert_to_text(inputfilepath, filename)
        
        