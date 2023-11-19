# Importing the required libraries
import xml.etree.ElementTree as Xet
import pandas as pd
import numpy as np
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

city_reporting = 0
city_list = [42,23,97,77,17,9,88,54,62,20,12,89,67,10,39,38,31,53,40,7,16,45,72,78,109,86,52,41,70,66,76,18,69,60,59,74,47,33,104,113,44,43,6,112,32,56,63,64,57,24,15,13,105,87,117,55,25,98,81,91,121,49,75,95,85,14,83,90,84,96,92,61,19,68,51,22,94,80,120,11,21,34,48,46,65,58,82,93,73,115,79,30,127,126,125,128]

# Prepping SWING precincts array for print() reporting
i = 0
precincts = []
while i < 137:
	precincts.append("-")
	i = i + 1
swing_numbers = [32, 41, 48, 75, 77, 92, 113, 123]
for a in swing_numbers:
	precincts[a] = "Not reporting"

runoff = ["No Precinct 0","Josh Guillory","Josh Guillory","Josh Guillory","Monique Blanco Boulet","Monique Blanco Boulet","Josh Guillory","Monique Blanco Boulet","Monique Blanco Boulet","Monique Blanco Boulet","Josh Guillory","Monique Blanco Boulet","Monique Blanco Boulet","Monique Blanco Boulet","Monique Blanco Boulet","Monique Blanco Boulet","Monique Blanco Boulet","Monique Blanco Boulet","Monique Blanco Boulet","Monique Blanco Boulet","Monique Blanco Boulet","Monique Blanco Boulet","Monique Blanco Boulet","Monique Blanco Boulet","Monique Blanco Boulet","Josh Guillory","Monique Blanco Boulet","Josh Guillory","Josh Guillory","Josh Guillory","Josh Guillory","Josh Guillory","Josh Guillory","Josh Guillory","Josh Guillory","Josh Guillory","Josh Guillory","Josh Guillory","Jan Swift","Monique Blanco Boulet","Josh Guillory","Josh Guillory","Josh Guillory","Josh Guillory","Josh Guillory","Josh Guillory","Josh Guillory","Josh Guillory","Josh Guillory","Jan Swift","No Precinct 50","Monique Blanco Boulet","Monique Blanco Boulet","Monique Blanco Boulet","Monique Blanco Boulet","Monique Blanco Boulet","Monique Blanco Boulet","Monique Blanco Boulet","Monique Blanco Boulet","Monique Blanco Boulet","Monique Blanco Boulet","Monique Blanco Boulet","Monique Blanco Boulet","Monique Blanco Boulet","Josh Guillory","Monique Blanco Boulet","Monique Blanco Boulet","Josh Guillory","Monique Blanco Boulet","Jan Swift","Jan Swift","Josh Guillory","Jan Swift","Monique Blanco Boulet","Jan Swift","Josh Guillory","Josh Guillory","Josh Guillory","Josh Guillory","Josh Guillory","Josh Guillory","Josh Guillory","Josh Guillory","Josh Guillory","Josh Guillory","Josh Guillory","Josh Guillory","Josh Guillory","Josh Guillory","Josh Guillory","Jan Swift","Josh Guillory","Josh Guillory","Josh Guillory","Josh Guillory","Josh Guillory","Josh Guillory","Josh Guillory","Josh Guillory","Monique Blanco Boulet","Josh Guillory","Josh Guillory","Josh Guillory","Josh Guillory","Josh Guillory","Josh Guillory","Josh Guillory","Josh Guillory","Josh Guillory","Josh Guillory","Josh Guillory","Josh Guillory","Josh Guillory","Josh Guillory","Josh Guillory","Josh Guillory","Josh Guillory","Josh Guillory","Josh Guillory","Josh Guillory","Josh Guillory","Josh Guillory","Josh Guillory","Josh Guillory","Josh Guillory","Josh Guillory","Josh Guillory","Josh Guillory","Josh Guillory","Josh Guillory","Josh Guillory","Josh Guillory","No Precinct 132","Josh Guillory","Josh Guillory","Josh Guillory","Josh Guillory"]


# Prepping PRECINCTS for pandas dataframe
cols = ["ID", "Parish", "Ward", "Precinct", "Boulet", "Guillory", "Total", "Boulet_VS", "Guillory_VS", "Winner_num", "Winner_name","Runoff_winner","Flipped_to"]
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
		elif Precinct == '':
			Precinct = 0
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
			if Precinct in city_list:
				city_reporting += 1
		if PrecinctVotes > 0 and Ward == "Early Voting":
			early_voting = "included."
		
		# Reset precinct winner
		WinVote = 0
		Winner_name = "-"
		Winner_num = 0
		flipped = "Not yet reporting"
		
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
				precincts[Precinct] = "Monique Blanco Boulet"
			elif Guillory > Boulet:
				WinVote = Guillory
				Winner_num = 3
				Winner_name = "Josh Guillory"
				precincts[Precinct] = "Josh Guillory"
			elif Boulet == Guillory:
				Winner_num = 2
				Winner_name = "Tie" 
				precincts[Precinct] = "Tie"
				
			if Winner_name == runoff[int(Precinct)]:
				flipped = "Did not flip"
			else: 
				flipped = "Flipped to " + Winner_name

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
				"Winner_name": Winner_name,
				"Runoff_winner": runoff[int(Precinct)],
				"Flipped_to": flipped})
				
# Write PRECINCT array to PRECINCT dataframe, then PRECINCT csv					
Nov_MP_precincts_df = pd.DataFrame(rows, columns=cols)
Nov_MP_precincts_df.to_csv('Nov_MP_Precinct_results.csv')


# Calculate SWING precinct results and print to terminal
Boulet_Swings = 0
Guillory_Swings = 0
swingers_reporting = 0
for a in swing_numbers:
	if precincts[a] == "Monique Blanco Boulet":
		Boulet_Swings +=  1
		swingers_reporting += 1
	elif precincts[a] == "Josh Guillory":
		Guillory_Swings +=  1
		swingers_reporting += 1
	elif precincts[a] == "Tie":
		swingers_reporting += 1
	print("Precinct", a, ":", precincts[a])
print(swingers_reporting, "out of 8 swing precincts in:" , Boulet_Swings, "for Boulet,", Guillory_Swings, 
	"for Guillory.")

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
print(str(precincts_reporting) + " of 134 precincts in. Boulet at " + str(Boulet_VS) + " and Guillory at " + str(Guillory_VS))

# Write TOTALS array to TOTALS dataframe, then TOTALS csv
Nov_MP_totals_df = pd.DataFrame(total_rows, columns=total_cols)
Nov_MP_totals_df.to_csv('Nov_MP_Totals_results.csv')

# Create PARISHWIDE metadata json file
notes = notes + "with " + str(precincts_reporting) + " out of " + str(precincts_total) + " precincts reporting. Early voting " + early_voting
dictionary = {
	"annotate" : {
		"notes" : notes
	}
}
json_object = json.dumps(dictionary, indent=4)
with open('Nov_MP_metadata.json', "w") as outfile:
	outfile.write(json_object)


# Create CITY metadata json file
city_notes = pretty_time + "with " + str(precincts_reporting) + " out of 96 precincts reporting."
dictionary = {
	"annotate" : {
		"notes" : city_notes
	}
}
json_object = json.dumps(dictionary, indent=4)
with open('Nov_MP_CITY_metadata.json', "w") as outfile:
	outfile.write(json_object)