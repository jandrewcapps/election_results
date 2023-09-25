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

Gabriel = Rubin = Williams = TotalVotes = 0

for x in Race:
    ID = x.getAttribute("ID")
    if ID == '64023': # --UPDATED-- with race ID for Oct. P2 on 9/25/23
        ID = 'Parish Council D-5'
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
                case '119926': #--UPDATED-- for Gabriel on 9/25/23
                    Gabriel = Gabriel + int(Votes)
                case '119263': #--UPDATED-- for Rubin on 9/25/23
                    Rubin = Rubin + int(Votes)
                case '119614': #--UPDATED-- for Williams on 9/25/23
                    Rubin = Rubin + int(Votes)
        TotalVotes = TotalVotes + Gabriel + Rubin + Williams
        #Gather precinct vote totals for each candidate 

rows.append({"Candidate": "Gabriel",
        "Votes": Gabriel})        
rows.append({"Candidate": "Rubin",
        "Votes": Rubin})
rows.append({"Candidate": "Williams",
        "Votes": Williams})
#Add total result to array
                
Oct_P5_df = pd.DataFrame(rows, columns=cols)
# Writing dataframe to csv
Oct_P5_df.to_csv('Oct_P5_results.csv')

