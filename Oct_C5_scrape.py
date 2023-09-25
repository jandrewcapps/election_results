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

Boudreaux = Ross = TotalVotes = 0

for x in Race:
    ID = x.getAttribute("ID")
    if ID == '64006': # --UPDATED-- with race ID for Oct. C4 on 9/25/23
        ID = 'City Council D-5'
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
                case '119690': #--UPDATED-- for Boudreaux on 9/25/23
                    Boudreaux = Boudreaux + int(Votes)
                case '120059': #--UPDATED-- for Ross on 9/25/23
                    Ross = Ross + int(Votes)
        TotalVotes = TotalVotes + Boudreaux + Ross
        #Gather precinct vote totals for each candidate 

rows.append({"Candidate": "Boudreaux",
        "Votes": Boudreaux})        
rows.append({"Candidate": "Ross",
        "Votes": Ross})
#Add total result to array
                
Oct_C5_df = pd.DataFrame(rows, columns=cols)
# Writing dataframe to csv
Oct_C5_df.to_csv('Oct_C5_results.csv')

