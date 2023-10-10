# Importing the required libraries
import xml.etree.ElementTree as Xet
import pandas as pd
import xml.dom.minidom
import requests
import json
  
# Parsing previously downloaded XML file
xmlparse = xml.dom.minidom.parse('sos_download.xml') #--UPDATED-- 9/25/23
# root = xmlparse.getroot()
# print('here')
Race = xmlparse.getElementsByTagName("Race")

# Storing SoS results timestamp
version_timestamp = xmlparse.getElementsByTagName("VersionDateTime")[0]
version_timestamp = version_timestamp.childNodes[0]
temp_time = version_timestamp.nodeValue
pretty_day = temp_time[8:10]
pretty_hour = temp_time[11:13]
pretty_minute = temp_time[14:16]
am_pm = ""
# Parsing timestamp into update message
if int(pretty_hour) == 0: 
	am_pm = " a.m. "
	pretty_hour = "12"
elif int(pretty_hour) < 12:
	am_pm = " a.m. "
elif int(pretty_hour) == 12:
	am_pm = " p.m. "
elif int(pretty_hour) > 12:
	am_pm = " p.m. "
	pretty_hour = int(pretty_hour) - 12
pretty_time = "Last Updated on Oct. " + pretty_day + " at " + pretty_hour + ":" + pretty_minute + am_pm
notes = pretty_time

cols = ["Candidate", "Votes"]
rows = []

Boulet = Guillory = Swift = TotalVotes = 0

precincts_total = 0
precincts_reporting = 0
early_voting = "not included."

for x in Race:
    ID = x.getAttribute("ID")
    precinct_vote_count = 0
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
            if Votes == "": 
                Votes = 0                
            precinct_vote_count = precinct_vote_count + int(Votes)
            match CID:
                case '118969': #--UPDATED-- for Boulet on 9/25/23
                    Boulet = Boulet + int(Votes)
                case '119045': #--UPDATED-- for Guillory on 9/25/23
                    Guillory = Guillory + int(Votes)
                case '119494': #--UPDATED-- for Swift on 9/25/23
                    Swift = Swift + int(Votes)
        if Ward != "Early Voting":
            precincts_total = precincts_total + 1
        if precinct_vote_count > 0 and Ward != "Early Voting":
            precincts_reporting = precincts_reporting + 1
        if precinct_vote_count > 0 and Ward == "Early Voting":
            early_voting = "included."
            
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


# Creating metadata json file
notes = notes + "with " + str(precincts_reporting) + " out of " + str(precincts_total) + " precincts reporting. Early voting " + early_voting
dictionary = {
	"annotate" : {
		"notes" : notes
	}
}
json_object = json.dumps(dictionary, indent=4)
with open('Oct_MP_Totals_results.json', "w") as outfile:
	outfile.write(json_object)
