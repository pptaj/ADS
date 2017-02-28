
# coding: utf-8

# In[31]:

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
import boto
import boto.s3
from boto.s3.key import Key
import zipfile


def amazon_upload(aws_access_key,aws_secret_key): 
    
    bucket_name = aws_access_key.lower() 
    

    
    conn = boto.connect_s3(aws_access_key,aws_secret_key)

    bucket = conn.lookup(bucket_name)
    if bucket is None:
        bucket = conn.create_bucket(bucket_name, location=boto.s3.connection.Location.DEFAULT)

    testfile = "Files.zip"
    def percent_cb(complete, total):
        sys.stdout.write('.')
        sys.stdout.flush()

    k = Key(bucket)
    k.key = testfile
    k.set_contents_from_filename(testfile,
    cb=percent_cb, num_cb=10)

def validate_aws_keys(aws_access_key,aws_access_read):
    try:
        bucket_name = aws_access_key.lower() 
        conn = boto.connect_s3(aws_access_key,aws_secret_key)
        bucket = conn.lookup(bucket_name)
        if bucket is None:
            bucket = conn.create_bucket(bucket_name, location=boto.s3.connection.Location.DEFAULT)
        print("VALID AWS PAIR")
        return True
    except:
        print("NOT A VALID AWS PAIR")
        return False
        

#10 K = 0001652044-17-000008, 
#1652044



def get_logger():
    create_directory("Files")
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
#       Stream Handler
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

def zip_folder(folder_path, output_path):
    """Zip the contents of an entire folder (with that folder included
    in the archive). Empty subfolders will be included in the archive
    as well.
    """
    parent_folder = os.path.dirname(folder_path)
    # Retrieve the paths of the folder contents.
    contents = os.walk(folder_path)

    zip_file = zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED)
    for root, folders, files in contents:
        # Include all subfolders, including empty ones.
        for folder_name in folders:
            absolute_path = os.path.join(root, folder_name)
            relative_path = absolute_path.replace(parent_folder + '\\', '')
            zip_file.write(absolute_path, relative_path)
        for file_name in files:
            absolute_path = os.path.join(root, file_name)
            relative_path = absolute_path.replace(parent_folder + '\\', '')
            zip_file.write(absolute_path, relative_path)
            
    
def create_csv10k(cik,document_accession_number,url,aws_access_key,aws_secret_key):
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
                cols = table.find_all('td')
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
        logger.info(".csv Files Created")
        
        #Zipping files
        zip_folder('Files', 'Files.zip')
        logger.info("Files Zipped")
        
        #Uploading Files to S3
        
        amazon_upload(aws_access_key,aws_secret_key)
        logger.info("Files Uploaded to S3")
        
    except:
        print("Something went wrong with the 10-K Page")
        print(sys.exc_info())
        pass

    #intitalize row and column numbers
    
def create_directory(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
        
def create_csv_10Q(cik,document_accession_number,url,aws_access_key,aws_secret_key):
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
        
         #Zipping files
        zip_folder('Files', 'Files.zip')
        logger.info("Files Zipped")
        
        #Uploading Files to S3
        
        amazon_upload(aws_access_key,aws_access_read)
        logger.info("Files Uploaded to S3")
        
    except:
        logger.error("Something went wrong with the 10-Q Page")
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
aws_access_read = ""
aws_secret_read = ""

with open("config.txt") as configfile:
    for line in configfile:
        name, val = line.partition("=")[::2]
        if (name=="cik"):
            cik_read = val
        elif (name=="accession_number"):
            accn_num_read = val
        elif (name=="aws_access_key"):
            aws_access_read = val
        elif (name=="aws_secret_key"):
            aws_secret_read = val
            
sys.stdout.write("\rProgress : %d%%" % 10)
time.sleep(1)

logger.info("Your CIK IS "+ cik_read.strip()+ " and Accession Number is " + accn_num_read.strip())

# cik = input("Please enter CIK: ")
# document_accession_number = input("Please enter accession number: ")
cik = cik_read.strip()
document_accession_number = accn_num_read.strip()
aws_access_key = aws_access_read.strip()
aws_secret_key = aws_secret_read.strip()


if not (aws_access_key == "" or aws_access_read == ""):
    
    
    if(validate_aws_keys(aws_access_key,aws_access_read) == True):
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
                create_csv_10Q(cik,document_accession_number, s, aws_access_key, aws_secret_key)
                sys.stdout.write("\rProgress : %d%%" % 99)
                time.sleep(1)
            elif(filing_flag == "10-K"):
                create_csv10k(cik,document_accession_number, s, aws_access_key, aws_secret_key)
                sys.stdout.write("\rProgress : %d%%" % 99)
                time.sleep(1)
            else:
                logger.error("No 10-K or 10-Q filing found for given CIK and Accession number")
            logger.info("Program Ended")

        except:
            logger.error("The cik and accession number pair doesn't exist")
            logger.info("Program Ended With Error")
            pass
        finally: 
        #     Removing Handler, Shutting Down Logger and Ending Progress Bar
            logger.removeHandler("handler")
            logging.shutdown()
            sys.stdout.write("\rProgress : %d%%" % 100)

            sys.stdout.flush()

    else:
        print("Please insert valid aws keys in config.txt")
        logger.removeHandler("handler")
        logging.shutdown()
        sys.stdout.write("\rProgress : %d%%" % 100)
        sys.stdout.flush()
else:
    print("Please insert valid aws keys in config.txt")
    logger.removeHandler("handler")
    logging.shutdown()
    sys.stdout.write("\rProgress : %d%%" % 100)
    sys.stdout.flush()
        
    

