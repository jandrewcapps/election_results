# Importing the required libraries
import xml.etree.ElementTree as Xet
import pandas as pd
import xml.dom.minidom
import requests


URL = "https://voterportal.sos.la.gov/api/MediaRequests/PrecinctVotes/2022-11-08/fmy5i4ikXTSxn2XaK5oB/yJCDurb0Q3XeVDIjkqBUtLCDl38FFtCYJVcGfM14"

response = requests.get(URL)
with open('yJCDurb0Q3XeVDIjkqBUtLCDl38FFtCYJVcGfM14.xml', 'wb') as file:
    file.write(response.content)

  
# Parsing the XML file
xmlparse = xml.dom.minidom.parse('yJCDurb0Q3XeVDIjkqBUtLCDl38FFtCYJVcGfM14.xml')
# root = xmlparse.getroot()
# print('here')
Race = xmlparse.getElementsByTagName("Race")

cols = ["ID", "Parish", "Ward", "Precinct", "Boulet", "Guillory",
                "Swift", "Total", "Winner_num", "Winner_name"]
rows = []

for x in Race:
    ID = x.getAttribute("ID")
    if ID == '62013': #update with race ID for Oct. MP
        ID = 'Lafayette Mayor-President'
        Parish = x.getAttribute("Parish")
        Ward = x.getAttribute("Ward")
        Precinct = x.getAttribute("Precinct")
        #Gather precinct & race ID info
        
        Boulet=Guillory=Swift=0

        Choice = x.getElementsByTagName("Choice") #'Choice' is SoS for candidate/ballot option
        for a in Choice:
            CID = a.getAttribute("ID")
            # print(CID)
            Votes = a.getAttribute("VoteTotal")
            if Votes == "": Votes = 0
            match CID:
                case '117190': #Update for Boulet
                    Boulet = int(Votes)
                case '116147': #Update for Guillory
                    Guillory = int(Votes)
                case '117724': #Update for Swift
                    Swift = int(Votes)
        TotalVotes = Boulet+Guillory+Swift        
        #Gather precinct vote totals for each candidate
        
        WinVote = 0
        Winner_name = ""
        if TotalVotes > 0:
            if Boulet > WinVote:
                WinVote = Boulet
                Winner_num = 1
                Winner_name = "Monique Blanco Boulet"
            if Guillory > WinVote:
                WinVote = Guillory
                Winner_num = 2
                Winner_name = "Josh Guillory"
            if Swift > WinVote:
                WinVote = Swift
                Winner_num = 3
                Winner_name = "Jan Swift"
            if WinVote == Boulet:
                if Boulet == Guillory:
                    Winner_num = 0
                    Winner_name = "Tie"
                if Boulet == Swift:
                    Winner_num = 0
                    Winner_name = "Tie"
            if WinVote == Guillory:
                if Guillory == Swift:
                    Winner_num = 0
                    Winner_name = "Tie"                
        #Determine each precinct winner and identify potential tie cases    

        rows.append({"ID": ID,
                "Parish": Parish,
                "Ward": Ward,
                "Precinct": Precinct,
                "Boulet": Boulet,
                "Guillory": Guillory,
                "Swift": Swift,
                "Total": TotalVotes,
                "Winner_num": Winner_num,
                "Winner_name": Winner_name})
        #Add precinct result to array
                
Oct_MP_df = pd.DataFrame(rows, columns=cols)
# Writing dataframe to csv
Oct_MP_df.to_csv('Oct_MP_results.csv')

