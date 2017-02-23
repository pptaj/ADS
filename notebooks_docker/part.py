
# coding: utf-8

# In[2]:

#10 K = 0001652044-17-000008, 
#1652044

import time
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

#html = urlopen("https://www.sec.gov/Archives/edgar/data/1652044/000165204417000008/goog10-kq42016.htm")
    #html = urlopen("https://www.sec.gov/Archives/edgar/data/51143/000005114313000007/ibm13q3_10q.htm")

def create_csv10k(cik,document_accession_number, url):
    try:
        
        html = urlopen(url)
        soup = BeautifulSoup(html,"lxml")
        all_tables = soup.find_all("table")
        type(all_tables)

        tables = []
        req_tables = []
        for x in all_tables:
            tables.append(x)

        for table in tables:
            all_rows =  table.find_all('tr')
            for row in all_rows:
                cols = row.find_all('td')
                for col in cols:
                    if col.text.find('$') > -1 or col.text.find('%') > -1:
                        req_tables.append(table)
                        break

        print(len(req_tables))
        print(len(tables))        

        i=0
        for table in req_tables:
            data = []
            i= i + 1
            all_rows =  table.find_all('tr')
            for row in all_rows:
                cols = row.find_all('td')
                cols = [(''.join(ch.strip('[\n,$]') for ch in ele.text)).strip() for ele in cols]
                #print(cols)
                data.append([ele for ele in cols if ele])
            create_directory("Files")
            create_directory("Files/" +cik)
            create_directory("Files/" + cik + "/" +document_accession_number)
            dir = "Files/" + cik + "/" + document_accession_number
            write_file = open( dir+"/table_" + str(i) + '.csv', 'w')
            
            for row in data:
                for column in row:
                    write_file.write(column)
                    write_file.write(',')
                write_file.write('\n')
  
    except:
        print("Something went wrong with the 10-K Page")
        pass

    #intitalize row and column numbers

def create_csv_10Q(cik,document_accession_number, url):
    try:        
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
            create_directory("Files")
            create_directory("Files/" +cik)
            create_directory("Files/" + cik + "/" +document_accession_number)
            dir = "Files/" + cik + "/" + document_accession_number
            write_file = open( dir+"/table_" + str(i) + '.csv', 'w')
            for row in data:
                for column in row:
                    write_file.write(column)
                    write_file.write(',')
                write_file.write('\n')

    except:
        print("Something went wrong with the 10-Q Page")
        pass
        #intitalize row and column numbers

def create_directory(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    
# READ CIK, ACCESSION NUMBER AND AMAZON KEYS FROM config.txt
cik_read =""
accn_num_read =""
aws_read = ""
#aws_secret_access_key = ''

#bucket_name = AWS_ACCESS_KEY_ID.lower() + '-dump'
#conn = boto.connect_s3(aws_access_key_id, aws_secret_access_key)

with open("config.txt") as configfile:
    for line in configfile:
        name, val = line.partition("=")[::2]
        if (name=="cik"):
            cik_read = val
        elif (name=="accession_number"):
            accn_num_read = val
        elif (name=="aws_read"):
            aws_read = val
        #elif (name=="AWS_SECRET_ACCESS_KEY"):
            #aws_secret_access_key = val
#bucket = conn.create_bucket(bucket_name, location=boto.s3.connection.Location.DEFAULT)

print("cik_read = "+ cik_read.strip()+ "accn_read = " + accn_num_read.strip())

# cik = input("Please enter CIK: ")
# document_accession_number = input("Please enter accession number: ")
cik = cik_read.strip()
document_accession_number = accn_num_read.strip()
aws_key = aws_read.strip()

#GENERATING THE URL
document_accession_number_without_dashes = re.sub('[-]', '', document_accession_number)
url = "https://www.sec.gov/Archives/edgar/data/" + str(int(cik)) + "/" + document_accession_number_without_dashes + "/"
url = url + document_accession_number +"-index.html"

try:
    
#     GENERATING URL TO GET 10-q or 10-k filing
    html = urlopen(url)
    soup = BeautifulSoup(html,'html.parser')
    cells = soup.findAll('td')

    filing_flag = "NA"
    s = "https://www.sec.gov"
    for cell in cells :
        if cell.get_text().find('10-Q') > -1 :
            filing_flag = "10-Q"
            a = cell.find_next_sibling("td").find('a',href=True)
            if a is not None:
                if 'href' in a.attrs:
                    result = a['href']
                    s+=result
                    break
        
                    
    
    for cell in cells :
        if cell.get_text().find('10-K') > -1 :
            filing_flag = "10-K"
            a = cell.find_previous_sibling("td").find('a')
            if a is not None:
                if 'href' in a.attrs:
                    result = a['href']
                    s+=result
                    break

                    
# Calling Function to go in 10-Q or 10-K filing page and getting the table data into csv 
    if(filing_flag == "10-Q"):
        create_csv_10Q(cik,document_accession_number, s)
    elif(filing_flag == "10-K"):
        create_csv10k(cik,document_accession_number, s) 
    else:
        print("No 10-K or 10-Q filing found for given CIK and Accession number")
    print("Program Ended")
    
except:
    print("The cik and accession number pair doesn't exist")
    print("Program Ended With Error")
    pass


# In[3]:




# In[2]:




# In[1]:




# In[ ]:




# In[ ]:



