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
# End pretty time function

Boulet = Guillory = Boulet_VS = Guillory_VS = Boulet_Tot = Guillory_Tot = TotalVotes = 0 #--UPDATED-- 10/26/23
precincts_total = 134
precincts_reporting = 0
early_voting = "not included."

# Prepping PRECINCTS for pandas dataframe
cols = ["ID", "Parish", "Ward", "Precinct", "Boulet", "Guillory", "Total", "Boulet_VS", "Guillory_VS", "Winner_num", "Winner_name"]
rows = []

# Prepping TOTALS for pandas dataframe
total_cols = ["Candidate", "Votes", "Voteshare"]
total_rows = []


# Iterating through Precinct results from SoS download
for x in Race:
	ID = x.getAttribute("ID")
	
	if ID == '64755': # --UPDATED-- with race ID for Nov. MP on 10/26/23
		ID = 'Lafayette Mayor-President'
		Parish = x.getAttribute("Parish")
		Ward = x.getAttribute("Ward")
		Precinct = x.getAttribute("Precinct")
		if Precinct != '':
			Precinct = int(Precinct)
			#Gather precinct & race ID info
			
			Boulet = Guillory = 0
			Choice = x.getElementsByTagName("Choice") #'Choice' is SoS for candidate/ballot option
			for a in Choice:
				CID = a.getAttribute("ID")
				# print(CID)
				Votes = a.getAttribute("VoteTotal")
				if Votes == "": Votes = 0
				match CID:
					case '120239': #--UPDATED-- for Boulet on 10/26/23
						Boulet = int(Votes)
						Boulet_Tot = Boulet_Tot + Boulet
					case '120240': #--UPDATED-- for Guillory on 10/26/23
						Guillory = int(Votes)
						Guillory_Tot = Guillory_Tot + Guillory
			
			# Sum votes within precinct and add to parishwide total vote count
			PrecinctVotes = Boulet + Guillory		
			
			# Check for precinct reporting and Early Voting status
			if PrecinctVotes > 0 and Ward != "Early Voting":
				precincts_reporting = precincts_reporting + 1
			
			# Reset precinct winner
			WinVote = 0
			Winner_name = ""
			Winner_num = 0
			
			# Determine new precinct winner or not reporting
			Boulet_VS = 0
			Guillory_VS = 0
			if PrecinctVotes == 0:
				Winner_name = "Not yet reporting"
			elif PrecinctVotes > 0:
				Boulet_VS = Boulet / PrecinctVotes
				Guillory_VS = Guillory / PrecinctVotes
				if Boulet > Guillory:
					WinVote = Boulet
					Winner_num = 1
					Winner_name = "Monique Blanco Boulet"
				elif Guillory > Boulet:
					WinVote = Guillory
					Winner_num = 3
					Winner_name = "Josh Guillory"
				elif Boulet == Guillory:
					Winner_num = 2
					Winner_name = "Tie"		   

			#Add precinct result to PRECINCT array
			rows.append({"ID": ID,
					"Parish": Parish,
					"Ward": Ward,
					"Precinct": Precinct,
					"Boulet": Boulet,
					"Guillory": Guillory,
					"Total": PrecinctVotes,
					"Boulet_VS": Boulet_VS,
					"Guillory_VS": Guillory_VS,
					"Winner_num": Winner_num,
					"Winner_name": Winner_name})
					
# Write PRECINCT array to PRECINCT dataframe, then PRECINCT csv					
Nov_MP_precincts_df = pd.DataFrame(rows, columns=cols)
Nov_MP_precincts_df.to_csv('Nov_MP_Precinct_results.csv')

# Determine Parishwide voteshares
TotalVotes = Boulet_Tot + Guillory_Tot
if TotalVotes > 0:
    Boulet_VS = (Boulet_Tot / TotalVotes) * 100
    Guillory_VS = (Guillory_Tot / TotalVotes) * 100

# Add parishwide results to TOTALS array
total_rows.append({"Candidate": "Monique Blanco Boulet",
		"Votes": Boulet_Tot,
		"Voteshare": Boulet_VS})		
total_rows.append({"Candidate": "Josh Guillory",
		"Votes": Guillory_Tot,
		"Voteshare": Guillory_VS})

# Write TOTALS array to TOTALS dataframe, then TOTALS csv
Nov_MP_totals_df = pd.DataFrame(total_rows, columns=total_cols)
Nov_MP_totals_df.to_csv('Nov_MP_Totals_results.csv')

# Create metadata json file
notes = notes + "with " + str(precincts_reporting) + " out of " + str(precincts_total) + " precincts reporting. Early voting " + early_voting
dictionary = {
	"annotate" : {
		"notes" : notes
	}
}
json_object = json.dumps(dictionary, indent=4)
with open('Nov_MP_metadata.json', "w") as outfile:
	outfile.write(json_object)
