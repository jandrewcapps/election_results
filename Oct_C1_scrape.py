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

Broussard = Hardy = Harrison = Matthieu_Robichaux = TotalVotes = 0

for x in Race:
    ID = x.getAttribute("ID")
    if ID == '64002': # --UPDATED-- with race ID for Oct. C1 on 9/25/23
        ID = 'City Council D-1'
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
                case '118764': #--UPDATED-- for Broussard on 9/25/23
                    Broussard = Broussard + int(Votes)
                case '118990': #--UPDATED-- for Hardy on 9/25/23
                    Hardy = Hardy + int(Votes)
                case '118719': #--UPDATED-- for Harrison on 9/25/23
                    Harrison = Harrison + int(Votes)
                case '119667': #--UPDATED-- for Matthieu-Robichaux on 9/25/23
                	Matthieu_Robichaux = Matthieu_Robichaux + int(Votes)
        TotalVotes = TotalVotes + Broussard + Hardy + Harrison + Matthieu_Robichaux       
        #Gather precinct vote totals for each candidate 

rows.append({"Candidate": "Broussard",
        "Votes": Broussard})        
rows.append({"Candidate": "Hardy",
        "Votes": Hardy})
rows.append({"Candidate": "Harrison",
        "Votes": Harrison})
rows.append({"Candidate": "Matthieu-Robichaux",
        "Votes": Matthieu_Robichaux})
#Add total result to array
                
Oct_C1_df = pd.DataFrame(rows, columns=cols)
# Writing dataframe to csv
Oct_C1_df.to_csv('Oct_C1_results.csv')

