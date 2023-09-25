# Importing the required libraries
import xml.etree.ElementTree as Xet
import pandas as pd
import xml.dom.minidom
import requests
  
# Parsing previously downloaded XML file
xmlparse = xml.dom.minidom.parse('sos_download.xml') #--UPDATED-- 9/25/23
# root = xmlparse.getroot()
# print('here')
Race = xmlparse.getElementsByTagName("Race")

cols = ["Candidate", "Votes"]
rows = []

Morales = Richard = TotalVotes = 0

for x in Race:
    ID = x.getAttribute("ID")
    if ID == '64020': # --UPDATED-- with race ID for Oct. P2 on 9/25/23
        ID = 'Parish Council D-2'
        Parish = x.getAttribute("Parish")
        Ward = x.getAttribute("Ward")
        Precinct = x.getAttribute("Precinct")
        #Gather precinct & race ID info
        
        Choice = x.getElementsByTagName("Choice") #'Choice' is SoS for candidate/ballot option
        for a in Choice:
            CID = a.getAttribute("ID")
            # print(CID)
            Votes = a.getAttribute("VoteTotal")
            if Votes == "": Votes = 0
            match CID:
                case '118783': #--UPDATED-- for Morales on 9/25/23
                    Morales = Morales + int(Votes)
                case '119164': #--UPDATED-- for Richard on 9/25/23
                    Richard = Richard + int(Votes)
        TotalVotes = TotalVotes + Morales + Richard
        #Gather precinct vote totals for each candidate 

rows.append({"Candidate": "Morales",
        "Votes": Morales})        
rows.append({"Candidate": "Richard",
        "Votes": Richard})
#Add total result to array
                
Oct_P2_df = pd.DataFrame(rows, columns=cols)
# Writing dataframe to csv
Oct_P2_df.to_csv('Oct_P2_results.csv')

