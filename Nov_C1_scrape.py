# Importing the required libraries
import xml.etree.ElementTree as Xet
import pandas as pd
import xml.dom.minidom
import requests
import json
  
# Parsing previously downloaded XML file
xmlparse = xml.dom.minidom.parse('Nov_sos_download.xml') #--UPDATED-- 10/26/23
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
pretty_time = "Last Updated on Nov. " + str(pretty_day) + " at " + str(pretty_hour) + ":" + str(pretty_minute) + am_pm
notes = pretty_time

cols = ["Candidate", "Votes", "Voteshare"]
rows = []

Broussard = Matthieu_Robichaux = Broussard_VS = Matthieu_Robichaux_VS = TotalVotes = 0

precincts_total = 0
precincts_reporting = 0
early_voting = "not included."

for x in Race:
    ID = x.getAttribute("ID")
    precinct_vote_count = 0

    if ID == '64754': # --UPDATED-- with race ID for Nov. C1 on 10/26/23
        ID = 'City Council D-1'
        Parish = x.getAttribute("Parish")
        Ward = x.getAttribute("Ward")
        Precinct = x.getAttribute("Precinct")
        #Gather precinct & race ID info
        
        candidate_count = no_vote_candidates = 0
        Choice = x.getElementsByTagName("Choice") #'Choice' is SoS for candidate/ballot option
        for a in Choice:
            candidate_count = candidate_count + 1
            CID = a.getAttribute("ID")
            # print(CID)
            Votes = a.getAttribute("VoteTotal")
            if Votes == "": 
                no_vote_candidates = no_vote_candidates + 1
                Votes = 0
            match CID:
                case '120237': #--UPDATED-- for Broussard on 10/26/23
                    Broussard = Broussard + int(Votes)
                case '120238': #--UPDATED-- for Matthieu-Robichaux on 10/26/23
                    Matthieu_Robichaux = Matthieu_Robichaux + int(Votes)
            precinct_vote_count = precinct_vote_count + int(Votes)

        if Ward != "Early Voting":
            precincts_total = precincts_total + 1
        
        if candidate_count > no_vote_candidates and Ward != "Early Voting":
            precincts_reporting = precincts_reporting + 1
        if candidate_count > no_vote_candidates and Ward == "Early Voting":
            early_voting = "included."
            
TotalVotes = Broussard + Matthieu_Robichaux
if TotalVotes != 0:
    Broussard_VS = Broussard / TotalVotes * 100
    Matthieu_Robichaux_VS = Matthieu_Robichaux / TotalVotes * 100
    
rows.append({"Candidate": "Elroy Broussard",
        "Votes": Broussard,
        "Voteshare": Broussard_VS})        
rows.append({"Candidate": "Melissa Matthieu-Robichaux",
        "Votes": Matthieu_Robichaux,
        "Voteshare": Matthieu_Robichaux_VS})
#Add total result to array
                
Nov_C1_df = pd.DataFrame(rows, columns=cols)
# Writing dataframe to csv
Nov_C1_df.to_csv('Nov_C1_results.csv')

# Creating metadata json file
notes = notes + "with " + str(precincts_reporting) + " out of " + str(precincts_total) + " precincts reporting. Early voting " + early_voting
dictionary = {
	"annotate" : {
		"notes" : notes
	}
}
json_object = json.dumps(dictionary, indent=4)
with open('Nov_C1_metadata.json', "w") as outfile:
	outfile.write(json_object)
