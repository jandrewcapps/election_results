# Import to run py scripts
import os

# Importing the required XML libraries
import xml.etree.ElementTree as Xet
import xml.dom.minidom
import requests

#import for timestamp
import time
from time import strftime


URL = "https://voterportal.sos.la.gov/api/MediaRequests/PrecinctVotes/2023-10-14/fmy5i4ikXTSxn2XaK5oB/yJCDurb0Q3XeVDIjkqBUtLCDl38FFtCYJVcGfM14"
#--UPDATED-- for 10/14/23 election on 9/25/23

response = requests.get(URL)
with open('sos_download.xml', 'wb') as file: #--UPDATED-- 9/25/23
    file.write(response.content)

os.system('python3 Oct_MP_Precinct_scrape.py')
os.system('python3 Oct_MP_Totals_scrape.py')
os.system('python3 Oct_C1_scrape.py')
os.system('python3 Oct_C2_scrape.py')
os.system('python3 Oct_C4_scrape.py')
os.system('python3 Oct_C5_scrape.py')
os.system('python3 Oct_P2_scrape.py')
os.system('python3 Oct_P3_scrape.py')
os.system('python3 Oct_P5_scrape.py')

print ("Last run at: ")
print (strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
