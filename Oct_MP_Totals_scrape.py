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

Boulet = Guillory = Swift = TotalVotes = 0

for x in Race:
    ID = x.getAttribute("ID")
    if ID == '64007': # --UPDATED-- with race ID for Oct. MP on 9/25/23
        ID = 'Lafayette Mayor-President'
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
                case '118969': #--UPDATED-- for Boulet on 9/25/23
                    Boulet = Boulet + int(Votes)
                case '119045': #--UPDATED-- for Guillory on 9/25/23
                    Guillory = Guillory + int(Votes)
                case '119494': #--UPDATED-- for Swift on 9/25/23
                    Swift = Swift + int(Votes)
        TotalVotes = TotalVotes + Boulet + Guillory + Swift
        #Gather precinct vote totals for each candidate 

rows.append({"Candidate": "Boulet",
        "Votes": Boulet})        
rows.append({"Candidate": "Guillory",
        "Votes": Guillory})
rows.append({"Candidate": "Swift",
        "Votes": Swift})
#Add total result to array
                
Oct_MP_df = pd.DataFrame(rows, columns=cols)
# Writing dataframe to csv
Oct_MP_df.to_csv('Oct_MP_Totals_results.csv')

