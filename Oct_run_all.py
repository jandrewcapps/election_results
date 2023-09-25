# Import to run py scripts
import os

# Importing the required libraries
import xml.etree.ElementTree as Xet
import xml.dom.minidom
import requests

URL = "https://voterportal.sos.la.gov/api/MediaRequests/PrecinctVotes/2023-10-14/fmy5i4ikXTSxn2XaK5oB/yJCDurb0Q3XeVDIjkqBUtLCDl38FFtCYJVcGfM14"
#--UPDATED-- for 10/14/23 election on 9/25/23

response = requests.get(URL)
with open('yJCDurb0Q3XeVDIjkqBUtLCDl38FFtCYJVcGfM14.xml', 'wb') as file: #--UPDATED-- 9/25/23
    file.write(response.content)

os.system('python3 Oct_MP_scrape.py')
os.system('python3 Oct_C1_scrape.py')

