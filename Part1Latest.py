
# coding: utf-8

# In[80]:

import urllib.response
import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import os
import re
from urllib.request import urlopen
import csv
import string
from string import punctuation
def create_csv(url):
    html = urlopen(url)
    soup = BeautifulSoup(html,"lxml")
    all_tables = soup.find_all("table", border=1)
    type(all_tables)
    tables = []
    for x in all_tables:
        tables.append(x)
    i=0
    for table in tables:
        data = []
        i= i + 1
        all_rows =  table.find_all('tr')
        for row in all_rows:
            cols = row.find_all('td')
            cols = [(''.join(ch.strip('[\n,$]') for ch in ele.text)).strip() for ele in cols]
            #print(cols)
            data.append([ele for ele in cols if ele])
        write_file = open('/home/sneha/Projects /ADS/RetrievedDocs/'+str(i)+ '.csv', 'w')
        for row in data:
            for column in row:
                write_file.write(column)
                write_file.write(',')
            write_file.write('\n')
        write_file.close()   
    
    #intitalize row and column numbers
cik = input("Please enter CIK: ")
document_accession_number = input("Please enter accession number: ")
document_accession_number_without_dashes = re.sub('[-]', '', document_accession_number)
url = "https://www.sec.gov/Archives/edgar/data/" + str(int(cik)) + "/" + document_accession_number_without_dashes + "/"
url = url + document_accession_number +"-index.html"
html = urlopen(url)
soup = BeautifulSoup(html,'html.parser')
cells = soup.findAll('td')
s = "https://www.sec.gov"
for cell in cells :
    if cell.get_text().find('10-Q') > -1 : 
        list = cell.find_next_sibling("td").find('a')
        #print("Q"+str(list))
    elif cell.get_text().find('10-K') > -1 : 
        list = cell.find_previous_sibling("td").find('a')
        #print("K"+str(list))
    if list is not None:
        if 'href' in list.attrs:
            result = list['href']
            s+=result
            #print(s)
            break
create_csv(s) 


# In[ ]:

def create_csv(url):
    html = urlopen(url)
    soup = BeautifulSoup(html,"lxml")
    all_tables = soup.find_all("table", border=1)
    type(all_tables)
    tables = []
    for x in all_tables:
        tables.append(x)
    i=0
    for table in tables:
        data = []
        i= i + 1
        all_rows =  table.find_all('tr')
        for row in all_rows:
            cols = row.find_all('td')
            cols = [(''.join(ch.strip('[\n,$]') for ch in ele.text)).strip() for ele in cols]
            #print(cols)
            data.append([ele for ele in cols if ele])
        write_file = open('/home/sneha/Projects /ADS/RetrievedDocs/'+str(i)+ '.csv', 'w')
        for row in data:
            for column in row:
                write_file.write(column)
                write_file.write(',')
            write_file.write('\n')
        write_file.close()   
    #intitalize row and column numbers
    


# In[ ]:




# In[ ]:




# In[ ]:



