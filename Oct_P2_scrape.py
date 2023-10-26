# Importing the required libraries
import xml.etree.ElementTree as Xet
import pandas as pd
import xml.dom.minidom
import requests
import json
  
# Parsing previously downloaded XML file
xmlparse = xml.dom.minidom.parse('Oct_sos_download.xml') #--UPDATED-- 9/25/23
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
pretty_time = "Last Updated on Oct. " + str(pretty_day) + " at " + str(pretty_hour) + ":" + str(pretty_minute) + am_pm
notes = pretty_time

cols = ["Candidate", "Votes", "Voteshare"]
rows = []

Morales = Richard = Morales_VS = Richard_VS = TotalVotes = 0

precincts_total = 0
precincts_reporting = 0
early_voting = "not included."

for x in Race:
    ID = x.getAttribute("ID")
    precinct_vote_count = 0

    if ID == '64020': # --UPDATED-- with race ID for Oct. P2 on 9/25/23
        ID = 'Parish Council D-2'
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
                case '118783': #--UPDATED-- for Morales on 9/25/23
                    Morales = Morales + int(Votes)
                case '119164': #--UPDATED-- for Richard on 9/25/23
                    Richard = Richard + int(Votes)
            precinct_vote_count = precinct_vote_count + int(Votes)

        if Ward != "Early Voting":
            precincts_total = precincts_total + 1
        if precinct_vote_count > 0 and Ward != "Early Voting":
            precincts_reporting = precincts_reporting + 1
        if precinct_vote_count > 0 and Ward == "Early Voting":
            early_voting = "included."
            
TotalVotes = Morales + Richard
if TotalVotes != 0:
    Morales_VS = Morales / TotalVotes * 100
    Richard_VS = Richard / TotalVotes * 100

rows.append({"Candidate": "Sidney Morales",
        "Votes": Morales, 
        "Voteshare": Morales_VS})        
rows.append({"Candidate": "Donald Richard",
        "Votes": Richard, 
        "Voteshare": Richard_VS})
#Add total result to array
                
Oct_P2_df = pd.DataFrame(rows, columns=cols)
# Writing dataframe to csv
Oct_P2_df.to_csv('Oct_P2_results.csv')

# Creating metadata json file
notes = notes + "with " + str(precincts_reporting) + " out of " + str(precincts_total) + " precincts reporting. Early voting " + early_voting
dictionary = {
	"annotate" : {
		"notes" : notes
	}
}
json_object = json.dumps(dictionary, indent=4)
with open('Oct_P2_results.json', "w") as outfile:
	outfile.write(json_object)
