# Import to run py scripts
import os

# Importing the required XML libraries
import xml.etree.ElementTree as Xet
import xml.dom.minidom
import requests


# Downloading SoS results file
URL = "https://voterportal.sos.la.gov/api/MediaRequests/PrecinctVotes/2023-11-18/fmy5i4ikXTSxn2XaK5oB/yJCDurb0Q3XeVDIjkqBUtLCDl38FFtCYJVcGfM14"
    #--UPDATED-- for 11/18/23 election on 10/26/23
response = requests.get(URL)
with open('Nov_sos_download.xml', 'wb') as file: #--UPDATED-- 10/26/23
    file.write(response.content)
    
# Parsing downloaded SoS results file
xmlparse = xml.dom.minidom.parse('Nov_sos_download.xml') #--UPDATED-- 10/26/23

# Storing SoS results timestamp
version_timestamp = xmlparse.getElementsByTagName("VersionDateTime")[0]
version_timestamp = version_timestamp.childNodes[0]
temp_time = version_timestamp.nodeValue
pretty_day = temp_time[8:10]
pretty_hour = temp_time[11:13]
pretty_minute = temp_time[14:16]
am_pm = ""

# Parsing timestamp into pretty time format
if int(pretty_hour) == 0: 
	am_pm = " a.m. "
	pretty_hour = "12"
elif int(pretty_hour) < 12:
	am_pm = " a.m. "
elif int(pretty_hour) == 12:
	am_pm = " p.m. "
elif int(pretty_hour) > 12:
	am_pm = " p.m. "
	pretty_hour = int(pretty_hour) - 12

# Creating timestamp string
pretty_time = "SoS Results as of: Nov. " + str(pretty_day) + " at " + str(pretty_hour) + ":" + str(pretty_minute) + am_pm
print (pretty_time)

# Running scrape scripts for selected races
os.system('python3 Nov_MP_scrape.py') #--UPDATED-- 10/26/23
os.system('python3 Nov_C1_scrape.py')

# End notice
print ("###")

