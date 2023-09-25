# Importing the required libraries
import xml.etree.ElementTree as Xet
import pandas as pd
import xml.dom.minidom
import requests


URL = "https://voterportal.sos.la.gov/api/MediaRequests/PrecinctVotes/2023-10-14/fmy5i4ikXTSxn2XaK5oB/yJCDurb0Q3XeVDIjkqBUtLCDl38FFtCYJVcGfM14"
#--UPDATED-- for 10/14/23 election on 9/25/23

response = requests.get(URL)
with open('yJCDurb0Q3XeVDIjkqBUtLCDl38FFtCYJVcGfM14.xml', 'wb') as file: #--UPDATED-- 9/25/23
    file.write(response.content)

  
# Parsing the XML file
xmlparse = xml.dom.minidom.parse('yJCDurb0Q3XeVDIjkqBUtLCDl38FFtCYJVcGfM14.xml') #--UPDATED-- 9/25/23
# root = xmlparse.getroot()
# print('here')
Race = xmlparse.getElementsByTagName("Race")

cols = ["ID", "Parish", "Ward", "Precinct", "Broussard", "Hardy",
                "Harrison", "Matthieu_Robichaux", "Total", "Winner_num", "Winner_name"]
rows = []

for x in Race:
    ID = x.getAttribute("ID")
    if ID == '64002': # --UPDATED-- with race ID for Oct. C1 on 9/25/23
        ID = 'City Council D-1'
        Parish = x.getAttribute("Parish")
        Ward = x.getAttribute("Ward")
        Precinct = x.getAttribute("Precinct")
        #Gather precinct & race ID info
        
        Broussard=Hardy=Harrison=Matthieu_Robichaux=0

        Choice = x.getElementsByTagName("Choice") #'Choice' is SoS for candidate/ballot option
        for a in Choice:
            CID = a.getAttribute("ID")
            # print(CID)
            Votes = a.getAttribute("VoteTotal")
            if Votes == "": Votes = 0
            match CID:
                case '118764': #--UPDATED-- for Broussard on 9/25/23
                    Broussard = int(Votes)
                case '118990': #--UPDATED-- for Hardy on 9/25/23
                    Hardy = int(Votes)
                case '118719': #--UPDATED-- for Harrison on 9/25/23
                    Harrison = int(Votes)
                case '119667': #--UPDATED-- for Matthieu-Robichaux on 9/25/23
                	Matthieu_Robichaux = int(Votes)
        TotalVotes = Broussard + Hardy + Harrison + Matthieu_Robichaux       
        #Gather precinct vote totals for each candidate
        
        WinVote = 0
        Winner_name = ""
        Winner_num = 0
        if TotalVotes > 0:
            if Broussard > WinVote:
                WinVote = Broussard
                Winner_num = 1
                Winner_name = "Broussard"
            if Hardy > WinVote:
                WinVote = Hardy
                Winner_num = 2
                Winner_name = "Hardy"
            if Harrison > WinVote:
                WinVote = Harrison
                Winner_num = 3
                Winner_name = "Harrison"
            if Matthieu_Robichaux > WinVote:
                WinVote = Matthieu_Robichaux
                Winner_num = 4
                Winner_name = "Matthieu_Robichaux"
            if WinVote == Broussard:
                if Broussard == Hardy:
                    Winner_num = 0
                    Winner_name = "Tie"
                if Broussard == Harrison:
                    Winner_num = 0
                    Winner_name = "Tie"
                if Broussard == Matthieu_Robichaux:
                	Winner_num = 0
                	Winner_name = "Tie"
            if WinVote == Hardy:
                if Hardy == Harrison:
                    Winner_num = 0
                    Winner_name = "Tie" 
                if Hardy == Matthieu_Robichaux:
                	Winner_num = 0
                	Winner_name = "Tie"
            if WinVote == Harrison:
            	if Harrison == Matthieu_Robichaux:
            		Winner_num = 0
            		Winner_name = "Tie"               
        #Determine each precinct winner and identify potential tie cases    

        rows.append({"ID": ID,
                "Parish": Parish,
                "Ward": Ward,
                "Precinct": Precinct,
                "Broussard": Broussard,
                "Hardy": Hardy,
                "Harrison": Harrison, 
                "Matthieu_Robichaux": Matthieu_Robichaux,
                "Total": TotalVotes,
                "Winner_num": Winner_num,
                "Winner_name": Winner_name})
        #Add precinct result to array
                
Oct_C1_df = pd.DataFrame(rows, columns=cols)
# Writing dataframe to csv
Oct_C1_df.to_csv('Oct_C1_results.csv')

