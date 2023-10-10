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
pretty_time = "Last Updated on Oct. " + str(pretty_day) + " at " + str(pretty_hour) + ":" + str(pretty_minute) + am_pm
notes = pretty_time

precincts_reporting = 0

# Prepping for pandas dataframe
cols = ["ID", "Parish", "Ward", "Precinct", "Boulet", "Guillory",
				"Swift", "Total", "Winner_num", "Winner_name"]
rows = []

for x in Race:
	ID = x.getAttribute("ID")
	
	if ID == '64007': # --UPDATED-- with race ID for Oct. MP on 9/25/23
		ID = 'Lafayette Mayor-President'
		Parish = x.getAttribute("Parish")
		Ward = x.getAttribute("Ward")
		Precinct = x.getAttribute("Precinct")
		if Precinct != '':
			Precinct = int(Precinct)
			#Gather precinct & race ID info
			
			Boulet = Guillory = Swift = 0
			Choice = x.getElementsByTagName("Choice") #'Choice' is SoS for candidate/ballot option
			for a in Choice:
				CID = a.getAttribute("ID")
				# print(CID)
				Votes = a.getAttribute("VoteTotal")
				if Votes == "": Votes = 0
				match CID:
					case '118969': #--UPDATED-- for Boulet on 9/25/23
						Boulet = int(Votes)
					case '119045': #--UPDATED-- for Guillory on 9/25/23
						Guillory = int(Votes)
					case '119494': #--UPDATED-- for Swift on 9/25/23
						Swift = int(Votes)
			TotalVotes = Boulet+Guillory+Swift		
			if TotalVotes > 0:
				precincts_reporting = precincts_reporting + 1
			#Gather precinct vote totals for each candidate
			
			WinVote = 0
			Winner_name = ""
			Winner_num = 0
			
			if TotalVotes == 0:
				Winner_name = "Not yet reporting"
			
			elif TotalVotes > 0:
				if Boulet > WinVote:
					WinVote = Boulet
					Winner_num = 1
					Winner_name = "Monique Blanco Boulet"
				if Guillory > WinVote:
					WinVote = Guillory
					Winner_num = 3
					Winner_name = "Josh Guillory"
				if Swift > WinVote:
					WinVote = Swift
					Winner_num = 2
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
Oct_MP_df.to_csv('Oct_MP_Precinct_results.csv')

# Creating metadata json file
notes = notes + "with " + str(precincts_reporting) + " out of 134 precincts reporting. Early voting not included."
dictionary = {
	"annotate" : {
		"notes" : notes
	}
}
json_object = json.dumps(dictionary, indent=4)
with open('Oct_MP_Precinct_results.json', "w") as outfile:
	outfile.write(json_object)
