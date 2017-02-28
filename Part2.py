
# coding: utf-8

# In[11]:

#Generate links foreach quarter
def qtr1_url(year):
    for i in range(1,4):
       url.append("http://www.sec.gov/dera/data/Public-EDGAR-log-file-data/" + str(year) + "/"+"Qtr1/"+"log"+str(year)+"0"+str(i)+"01.zip")
       
def qtr2_url(year):
    for i in range(4,7):
       url.append("http://www.sec.gov/dera/data/Public-EDGAR-log-file-data/" + str(year) + "/"+"Qtr2/"+"log"+str(year)+"0"+str(i)+"01.zip")
def qtr3_url(year):
    for i in range(7,10):
       url.append("http://www.sec.gov/dera/data/Public-EDGAR-log-file-data/" + str(year) + "/"+"Qtr3/"+"log"+str(year)+"0"+str(i)+"01.zip")
      
def qtr4_url(year):
    for i in range(10,13):
       url.append("http://www.sec.gov/dera/data/Public-EDGAR-log-file-data/" + str(year) + "/"+"Qtr4/"+"log"+str(year)+str(i)+"01.zip")
 
     
        
 


# In[12]:

def get_logger():
    create_directory("Files2")
    loglevel = logging.INFO            # DEBUG, CRITICAL, WARNING, ERROR
    logger = logging.getLogger("Application_Logs")
    logger2 = logging.getLogger("Application_Logs_Stream")
    if not getattr(logger, 'handler_set', None):
        logger.setLevel(logging.INFO)
#         Logfile handler
        handler = logging.FileHandler('Files2/logs.log')
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


# In[13]:

def create_directory(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)


# In[ ]:




# In[ ]:

import urllib.response
import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import os
import re
from urllib.request import urlopen
import logging
import requests, zipfile, io, sys, time
#http://www.sec.gov/dera/data/Public-EDGAR-log-file-data/2003/Qtr1/log20030101.zip
     
logger = get_logger()
logger.info("Starting Program")
sys.stdout.write("\rProgress : %d%%" % 0)
time.sleep(1)
sys.stdout.write("\rProgress : %d%%" % 1)
time.sleep(1)

year_read = ""
year = 0

with open("config.txt") as configfile:
    for line in configfile:
        name, val = line.partition("=")[::2]
        if (name=="year"):
            year_read = val
year = year_read.strip()

try:
    year = int(year)
    if(year>=2003 and year<=2016):    
        sys.stdout.write("\rProgress : %d%%" % 10)
        time.sleep(1)

        

        sys.stdout.write("\rProgress : %d%%" % 10)
        time.sleep(1)
        #Data available only till: Qtr1,2016
        url = []

        if year == "2016":
            qtr1_url(year)
        #Any other year excep for 2016, all four quarters    
        else:
            logger.info("Generating Links for log files")
            sys.stdout.write("\rProgress : %d%%" % 15)
            qtr1_url(year)
            sys.stdout.write("\rProgress : %d%%" % 20)
            qtr2_url(year)
            sys.stdout.write("\rProgress : %d%%" % 25)
            qtr3_url(year)
            sys.stdout.write("\rProgress : %d%%" % 30)
            qtr4_url(year)

        #print(url[5])
        #Extract all files into folder
        i = 30
        logger.info("Downloading and Extracting Log files")
        print("\nIt may take some time")
        for link in url:
            r = requests.get(link)
            z = zipfile.ZipFile(io.BytesIO(r.content))
            z.extractall(path="Files2/"+str(year))
            i+=5
            sys.stdout.write("\rProgress : %d%%" % i)
        logger.info("Downloading Completed") 
        logger.removeHandler("handler")
        logging.shutdown()
        sys.stdout.write("\rProgress : %d%%" % 100)
        sys.stdout.flush()
    else:
        print("Not a valid year")
        logger.removeHandler("handler")
        logging.shutdown()
        sys.stdout.write("\rProgress : %d%%" % 100)
        sys.stdout.flush()
except:
    print("exception Not a valid year")
    logger.removeHandler("handler")
    logging.shutdown()
    sys.stdout.write("\rProgress : %d%%" % 100)
    sys.stdout.flush()

