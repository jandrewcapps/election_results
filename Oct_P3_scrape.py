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

Hughes = Monts = Stansbury = TotalVotes = 0

for x in Race:
    ID = x.getAttribute("ID")
    if ID == '64021': # --UPDATED-- with race ID for Oct. P2 on 9/25/23
        ID = 'Parish Council D-3'
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
                case '120102': #--UPDATED-- for Hughes on 9/25/23
                    Hughes = Hughes + int(Votes)
                case '120051': #--UPDATED-- for Monts on 9/25/23
                    Monts = Monts + int(Votes)
                case '118701': #--UPDATED-- for Stansbury on 9/25/23
                    Monts = Monts + int(Votes)
        TotalVotes = TotalVotes + Hughes + Monts + Stansbury
        #Gather precinct vote totals for each candidate 

rows.append({"Candidate": "Hughes",
        "Votes": Hughes})        
rows.append({"Candidate": "Monts",
        "Votes": Monts})
rows.append({"Candidate": "Stansbury",
        "Votes": Stansbury})
#Add total result to array
                
Oct_P3_df = pd.DataFrame(rows, columns=cols)
# Writing dataframe to csv
Oct_P3_df.to_csv('Oct_P3_results.csv')

