##Disneyland.py
##Contains the class that handles getting info from Disneyland servers.

import requests,json,time

def get_access_token():
	r = requests.post('https://authorization.go.com/token',data={"grant_type":"assertion","assertion_type":"public","client_id":"WDPRO-MOBILE.MDX.WDW.ANDROID-PROD"})
	json_data = json.loads(r.text)
	access_token = json_data["access_token"]
	return access_token

def get_hours():
	access_token = get_access_token()

	url = "https://api.wdpro.disney.go.com/global-pool-override-A/facility-service/schedules/"

	disney_code = "330339"
	dca_code = "336894"

	r2_d2 = requests.get(url + disney_code,
						headers={"Authorization":"BEARER "+access_token,
							   "Accept":"application/json;apiversion=1",
							   "X-Conversation-Id":"WDPRO-MOBILE.MDX.CLIENT-PROD",
							   "X-App-Id":"WDW-MDX-ANDROID-3.4.1"
							   }
						)
	jsonData = json.loads(r2_d2.text)

	disney_time = "Unknown"
	dca_time = "Unknown"

	day = time.strftime("%Y-%m-%d")
	for schedule in jsonData["schedules"]:
		if schedule["date"] == day and schedule["type"] == "Operating":
			openTime = time.strptime(schedule["startTime"],"%H:%M:%S")
			closeTime = time.strptime(schedule["endTime"], "%H:%M:%S")
			o = time.strftime("%I:%M %p",openTime).lstrip("0")
			c = time.strftime("%I:%M %p",closeTime).lstrip("0")
			disney_time = o + " - " + c

	c3po = requests.get(url + dca_code,
						headers={"Authorization":"BEARER "+access_token,
							   "Accept":"application/json;apiversion=1",
							   "X-Conversation-Id":"WDPRO-MOBILE.MDX.CLIENT-PROD",
							   "X-App-Id":"WDW-MDX-ANDROID-3.4.1"
							   }
						)
	jsonData = json.loads(c3po.text)

	day = time.strftime("%Y-%m-%d")
	for schedule in jsonData["schedules"]:
		if schedule["date"] == day and schedule["type"] == "Operating":
			openTime = time.strptime(schedule["startTime"],"%H:%M:%S")
			closeTime = time.strptime(schedule["endTime"], "%H:%M:%S")
			o = time.strftime("%I:%M %p",openTime).lstrip("0")
			c = time.strftime("%I:%M %p",closeTime).lstrip("0")
			dca_time = o + " - " + c

	return (disney_time, dca_time)

def get_wait_times():
	access_token = get_access_token()
	
	#Get data for Disneyland.
	r2_d2 = requests.get("https://api.wdpro.disney.go.com/facility-service/theme-parks/330339/wait-times",
					  headers={"Authorization":"BEARER "+access_token,
							   "Accept":"application/json;apiversion=1",
							   "X-Conversation-Id":"WDPRO-MOBILE.MDX.CLIENT-PROD",
							   "X-App-Id":"WDW-MDX-ANDROID-3.4.1"
							   }
					  )
	data = json.loads(r2_d2.text.replace(u"\xa0","").replace(u"\xe2","-"))
	outDict = {}
	for entry in data["entries"]:
		name = entry["name"]
		wt = entry["waitTime"]
		t = ""
		if wt["status"]=="Closed":
			t = "Closed"
		else:
			if "postedWaitMinutes" in wt:
				outDict[name] = wt["postedWaitMinutes"]
	#Get data for California Adventure.
	c3po = requests.get("https://api.wdpro.disney.go.com/facility-service/theme-parks/336894/wait-times",
					  headers={"Authorization":"BEARER "+access_token,
							   "Accept":"application/json;apiversion=1",
							   "X-Conversation-Id":"WDPRO-MOBILE.MDX.CLIENT-PROD",
							   "X-App-Id":"WDW-MDX-ANDROID-3.4.1"
							   }
					  )
	data = json.loads(c3po.text.replace(u"\xa0","").replace(u"\xe2","-"))
	for entry in data["entries"]:
		name = entry["name"]
		wt = entry["waitTime"]
		t = ""
		if wt["status"]=="Closed":
			t = "Closed"
		else:
			if "postedWaitMinutes" in wt:
				outDict[name] = wt["postedWaitMinutes"]
	
	return outDict

names = {
		"guardians":"Guardians of the Galaxy - Mission: BREAKOUT!",
		"buzz":"Buzz Lightyear Astro Blasters",
		"thunder":"Big Thunder Mountain Railroad",
		"monorail":"Disneyland Monorail",
		"dumbo":"Dumbo the Flying Elephant",
		"tiki":"Enchanted Tiki Room",
		"nemo":"Finding Nemo Submarine Voyage",
		"gadget":"Gadget's Go Coaster",
		"grizzly":"Grizzly River Run",
		"haunted":"Haunted Mansion",
		"indy":"Indiana Jones Adventure",
		"tea":"Mad Tea Party",
		"toad":"Mr. Toad's Wild Ride",
		"peter":"Peter Pan's Flight",
		"pinocchio":"Pinocchio's Daring Journey",
		"pirates":"Pirates of the Caribbean",
		"space":"Space Mountain",
		"splash":"Splash Mountain",
		"star":"Star Tours- The Adventures Continue",
		"small":"\"it's a small world\"",
		"alice":"Alice in Wonderland",
		"screamin":"California Screamin'",
		"screaming":"California Screamin'",
		"grizzly":"Grizzly River Run",
		"soarin":"Soarin' Around The World",
		"soaring":"Soarin' Around The World",
		"mania":"Toy Story Midway Mania!",
		"midway":"Toy Story Midway Mania!",
		"racers":"Radiator Springs Racers",
		"sky school":"Goofy's Sky School"
		}
displayNames = {'Big Thunder Mountain Railroad': "Thunder Mountain",
				 'Toy Story Midway Mania!': "Toy Story",
				 'Indiana Jones Adventure': "Indiana Jones",
				 'Casey Jr. Circus Train': "Circus Train",
				 'Finding Nemo Submarine Voyage': "Finding Nemo",
				 'Mad Tea Party': "Tea Cups",
				 'Astro Orbitor': "Astro Orbitor",
				 "Francis' Ladybug Boogie": "Ladybug Boogie",
				 "Mr. Toad's Wild Ride": "Mr. Toad's Wild Ride",
				 '"it\'s a small world" Holiday': "Small World",
				 "California Screamin'": "California Screamin'",
				 'Redwood Creek Challenge Trail': "Challenge Trail",
				 "Soarin' Around The World": "Soarin'",
				 'Star Tours- The Adventures Continue': "Star Tours",
				 'Haunted Mansion Holiday': "Haunted Mansion",
				 'Haunted Mansion': "Haunted Mansion",
				 "Mater's Jingle Jamboree": "Mater's Junkyard Jamboree",
				 "Mater's Junkyard Jamboree": "Mater's Junkyard Jamboree",
				 'Storybook Land Canal Boats': "Storybook Land Canal Boats",
				 "Roger Rabbit's Car Toon Spin": "Roger Rabit",
				 "Luigi's Joy to the Whirl": "Luigi's...something",
				 'Dumbo the Flying Elephant': "Dumbo",
				 'Grizzly River Run': "Grizzly River Run",
				 'Red Car Trolley': "Red Car Trolley",
				 "Pinocchio's Daring Journey": "Pinocchio",
				 "Flik's Flyers": "Flik's Flyers",
				 "Mickey's House and Meet Mickey": "Meet Mickey",
				 'Buzz Lightyear Astro Blasters': "Astro Blasters",
				 'Disneyland Railroad': "Disneyland Railroad",
				 'Guardians of the Galaxy - Mission: BREAKOUT!': "Guardians",
				 'The Many Adventures of Winnie the Pooh': "Winnie the Pooh",
				 "Peter Pan's Flight": "Peter Pan",
				 'Turtle Talk with Crush': "Turtle Talk",
				 'Space Mountain': "Space Mountain",
				 'Hyperspace Mountain': "Space Mountain",
				 "The Little Mermaid - Ariel's Undersea Adventure": "The Little Mermaid",
				 'Pirates of the Caribbean': "Pirates",
				 'King Arthur Carrousel': "King Arthur Carousel",
				 "King Triton's Carousel": "King Triton's Carousel",
				 'Jungle Cruise': "Jungle Cruise",
				 'Silly Symphony Swings': "Silly Symphony Swings",
				 "Tuck and Roll's Drive 'Em Buggies": "Tuck and Roll",
				 'Monsters, Inc. Mike & Sulley to the Rescue!': "Monsters, Inc",
				 "Heimlich's Chew Chew Train": "Chew Chew Train",
				 'Radiator Springs Racers': "Radiator Racers",
				 "Gadget's Go Coaster": "Gadget's Go Coaster",
				 'Autopia': "Autopia",
				 'Alice in Wonderland': "Alice in Wonderland",
				 'Splash Mountain': "Splash Mountain",
				 "Jumpin' Jellyfish": "Jumpin' Jellyfish",
				 "Mickey's Fun Wheel": "Mickey's Fun Wheel",
				 'Disneyland Monorail': "Monorail",
				 'Matterhorn Bobsleds': "Matterhorn"}

if __name__ == "__main__":
	print(get_hours())