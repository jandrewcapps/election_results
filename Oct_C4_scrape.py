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

Hooks = LeBlanc = TotalVotes = 0

for x in Race:
    ID = x.getAttribute("ID")
    if ID == '64005': # --UPDATED-- with race ID for Oct. C4 on 9/25/23
        ID = 'City Council D-4'
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
                case '119424': #--UPDATED-- for Hooks on 9/25/23
                    Hooks = Hooks + int(Votes)
                case '119344': #--UPDATED-- for LeBlanc on 9/25/23
                    LeBlanc = LeBlanc + int(Votes)
        TotalVotes = TotalVotes + Hooks + LeBlanc
        #Gather precinct vote totals for each candidate 

rows.append({"Candidate": "Hooks",
        "Votes": Hooks})        
rows.append({"Candidate": "LeBlanc",
        "Votes": LeBlanc})
#Add total result to array
                
Oct_C4_df = pd.DataFrame(rows, columns=cols)
# Writing dataframe to csv
Oct_C4_df.to_csv('Oct_C4_results.csv')

