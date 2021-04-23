import pandas as pd
import re
import pdfplumber
import os

titles_list = []
abstracts_list = []
keywords_list = []



pdf_files = []

#This get the directory to our pdf files
workingDir = os.getcwd()
neededDir = workingDir 

allDir = os.listdir(neededDir)
for files in allDir:
    if files.endswith('pdf'):   #This condition look for those that ends with pdf in the directory and append it to a list
        pdf_files.append(files) 


#This function takes the pdf files and extract it using Module PDFPLUMBER
def extract_text(pdf_file):
    
    pdf = pdfplumber.open(pdf_file)  
    pages = pdf.pages

    text = ' '
    
    #loop through all pages and append its data to a variable text
    for i,pg in enumerate(pages):

        text += str(pages[i].extract_text()) 

    # print(text)
    #Split the text with regular expression [ 1  Introduction or 1. Introduction ]
    item_details  = re.split(r'((1  Introduction|1. Introduction|I. INTRODUCTION|Being))',text) 
    keywords = item_details[0]

    #Split the text with regular expression of word 'Abstract' and clean it to get title
    titles = re.split(r'(Abstract|Florida State University)',keywords)
    titles = titles[0].split('\n')

    if len(titles) == 6:
        title = ' '.join(titles[2:4]).strip()
        titles_list.append(title)
    
    elif len(titles) > 9:
        title = ' '.join(titles[6:8]).strip()
        titles_list.append(title)
    
    else:
        title = ' '.join(titles[:2]).strip()
        titles_list.append(title)
    # print(title)
    
    #Split the text with regular expression of word 'Keywords:' and clean it to get keywords
    n_keywords = re.split(r'(Keywords:|Index Terms—)',keywords)
    keywords = n_keywords[-1].strip()
    keywords_list.append(keywords)
    # print(keywords)
    
    #Split the text with regular expression of word 'Abstract' and clean it to get title
    abstract = n_keywords[0]
    abstract = re.split(r'(Abstract|Florida State University)',abstract)
    abstract = abstract[-1].strip(': ')
    abstracts_list.append(abstract.strip('\n'))
    # print(abstract)

    write_to_excel(titles_list, keywords_list, abstracts_list)
def write_to_excel(titles, keywords, abstracts):

    #This is the table values as key and our list of table value as the dictionary value 
    datas  = {'Article Title': titles, 'Keywords': keywords, 'Abstract': abstracts} 
    # print(datas)

        
    df = pd.DataFrame.from_dict(datas)      #dataframe of our datas values write to a csv file
    df.to_excel('pdf_file.xlsx', index=False)
    print('done')
    
#This loop through the list of pdf files and pick each pdf item and pass it to the function
for pdf_file in pdf_files:
    extract_text(pdf_file)
