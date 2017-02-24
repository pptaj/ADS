
# coding: utf-8

# In[11]:

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
import zipfile
import os
import sys
import logging

def get_logger():
    loglevel = logging.INFO            # DEBUG, CRITICAL, WARNING, ERROR
    logger = logging.getLogger("Application_Logs")
    logger2 = logging.getLogger("Application_Logs_Stream")
    if not getattr(logger, 'handler_set', None):
        logger.setLevel(logging.INFO)
#         Logfile handler
        handler = logging.FileHandler('Files/logs.log')
        handler2 = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.addHandler(handler2)
        logger.setLevel(loglevel)
        logger.handler_set = True
#         Stream Handler
    if not getattr(logger, 'handler_set', None):
        logger2.setLevel(logging.INFO)
        handler2 = logging.StreamHandler()
        handler2.setFormatter(formatter)
        logger2.addHandler(handler2)
        logger2.setLevel(loglevel)
        logger2.handler_set = True
        
    return logger
#html = urlopen("https://www.sec.gov/Archives/edgar/data/1652044/000165204417000008/goog10-kq42016.htm")
    #html = urlopen("https://www.sec.gov/Archives/edgar/data/51143/000005114313000007/ibm13q3_10q.htm")

def create_csv10k(cik,document_accession_number, url):
    try:
        logger = get_logger()
        logger.info("Downloading 10-K Filing")
        html = urlopen(url)
        soup = BeautifulSoup(html,"lxml")
        logger.info("PARSING ALL TABLES in 10-K filing")
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
        
#         print(len(req_tables))
#         print(len(tables))        

        i=0
        logger.info("SAVING TABLES TO .csv file")
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
            write_file.close()
        logger.info(".csv FILES CREATED")
        #Zipping the files

    except:
        print("Something went wrong with the 10-K Page")
        print(sys.exc_info())
        pass

    #intitalize row and column numbers
    
def create_directory(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
def create_csv_10Q(cik,document_accession_number, url):
    try:
        logger = get_logger()
        logger.info("Downloading 10-Q Filing")
        html = urlopen(url)
        soup = BeautifulSoup(html,"lxml")
        logger.info("PARSING ALL TABLES in 10-Q filing")
        all_tables = soup.find_all("table", border=1)
        type(all_tables)
        tables = []
        for x in all_tables:
            tables.append(x)
        i=0
        logger.info("SAVING TABLES TO .csv file")
        for table in tables:
            data = []
            i= i + 1
            all_rows =  table.find_all('tr')
            
            for row in all_rows:
                cols = row.find_all('td')
                cols = [(''.join(ch.strip('[\n,$]') for ch in ele.text)).strip() for ele in cols]
                #print(cols)
                data.append([ele for ele in cols if ele])
            
            fileDir= os.path.dirname(os.path.realpath('_file'))
            
#             create_directory("Files")
#             create_directory("Files/" +cik)
#             create_directory("Files/" + cik + "/" +document_accession_number)
            dir = "Files/" + cik + "/" + document_accession_number
            write_file = open(os.path.join(fileDir,(dir)+"/table_" + str(i) + '.csv', 'w'))
    
    
#             write_file = open( os.path.join(fileDir,dir+"/table_" + str(i) + '.csv', 'w')
            
            for row in data:
                for column in row:
                    write_file.write(column)
                    write_file.write(',')
                write_file.write('\n')
            write_file.close()   
        logger.info(".csv FILES CREATED")
    except:
        logger.ERROR("Something went wrong with the 10-Q Page")
        pass
        #intitalize row and column numbers
        
# time.sleep(1)
sys.stdout.write("\rProgress : %d%%" % 0)
time.sleep(1)


sys.stdout.write("\rProgress : %d%%" % 2)
time.sleep(1)
# Adding logger
logger = get_logger()
logger.info("Reading Data From Config File")


sys.stdout.write("\rProgress : %d%%" % 5)    
time.sleep(1)
# READ CIK, ACCESSION NUMBER AND AMAZON KEYS FROM config.txt
cik_read =""
accn_num_read =""
aws_read = ""
with open("config.txt") as configfile:
    for line in configfile:
        name, val = line.partition("=")[::2]
        if (name=="cik"):
            cik_read = val
        elif (name=="accession_number"):
            accn_num_read = val
        elif (name=="aws_key"):
            aws_read = val
            
sys.stdout.write("\rProgress : %d%%" % 10)
time.sleep(1)

logger.info("Your CIK IS "+ cik_read.strip()+ " and Accession Number is " + accn_num_read.strip())

# cik = input("Please enter CIK: ")
# document_accession_number = input("Please enter accession number: ")
cik = cik_read.strip()
document_accession_number = accn_num_read.strip()
aws_key = aws_read.strip()

#GENERATING THE URL
logger.info("GENERATING THE URL")
document_accession_number_without_dashes = re.sub('[-]', '', document_accession_number)
url = "https://www.sec.gov/Archives/edgar/data/" + str(int(cik)) + "/" + document_accession_number_without_dashes + "/"
url = url + document_accession_number +"-index.html"
sys.stdout.write("\rProgress : %d%%" % 35)
try:
    
#     GENERATING URL TO GET 10-q or 10-k filing
    logger.info("GENERATING URL TO GET 10-q or 10-k filing")
    html = urlopen(url)
    soup = BeautifulSoup(html,'html.parser')
    cells = soup.findAll('td')

    filing_flag = "NA"
    s = "https://www.sec.gov"
    for cell in cells :
        if cell.get_text().find('10-Q') > -1 :
            filing_flag = "10-Q"
            logger.info("10-Q FILING FOUND FOR YOUR CIK AND ACCESSION NUMBER PAIR")
            a = cell.find_next_sibling("td").find('a',href=True)
            if a is not None:
                if 'href' in a.attrs:
                    result = a['href']
                    s+=result
                    break
        
                    
    
    for cell in cells :
        if cell.get_text().find('10-K') > -1 :
            filing_flag = "10-K"
            logger.info("10-K FILING FOUND FOR YOUR CIK AND ACCESSION NUMBER PAIR")
            a = cell.find_previous_sibling("td").find('a')
            if a is not None:
                if 'href' in a.attrs:
                    result = a['href']
                    s+=result
                    break
# sys.stdout.write("\rProgress : %d%%" % 70)
                    
# Calling Function to go in 10-Q or 10-K filing page and getting the table data into csv 
    if(filing_flag == "10-Q"):
        create_csv_10Q(cik,document_accession_number, s)
        sys.stdout.write("\rProgress : %d%%" % 99)
        time.sleep(1)
    elif(filing_flag == "10-K"):
        create_csv10k(cik,document_accession_number, s)
        sys.stdout.write("\rProgress : %d%%" % 99)
        time.sleep(1)
    else:
        logger.ERROR("No 10-K or 10-Q filing found for given CIK and Accession number")
    logger.info("Program Ended")
    
except:
    logger.ERROR("The cik and accession number pair doesn't exist")
    logger.info("Program Ended With Error")
    pass
finally: 
#     Removing Handler, Shutting Down Logger and Ending Progress Bar
    logger.removeHandler("handler")
    logging.shutdown()
    sys.stdout.write("\rProgress : %d%%" % 100)
    
    sys.stdout.flush()


# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:



