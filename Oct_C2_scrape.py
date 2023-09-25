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

Arabie = Naquin = TotalVotes = 0

for x in Race:
    ID = x.getAttribute("ID")
    if ID == '64003': # --UPDATED-- with race ID for Oct. C2 on 9/25/23
        ID = 'City Council D-2'
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
                case '119430': #--UPDATED-- for Arabie on 9/25/23
                    Arabie = Arabie + int(Votes)
                case '119465': #--UPDATED-- for Naquin on 9/25/23
                    Naquin = Naquin + int(Votes)
        TotalVotes = TotalVotes + Arabie + Naquin
        #Gather precinct vote totals for each candidate 

rows.append({"Candidate": "Arabie",
        "Votes": Arabie})        
rows.append({"Candidate": "Naquin",
        "Votes": Naquin})
#Add total result to array
                
Oct_C2_df = pd.DataFrame(rows, columns=cols)
# Writing dataframe to csv
Oct_C2_df.to_csv('Oct_C2_results.csv')

