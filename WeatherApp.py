from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.core.image import Image
from kivy.properties import StringProperty
from kivy.logger import Logger


import time
import jsonRequests

import weatherCodes

class WeatherApp(RelativeLayout):

	location="Orange,CA"
	updateTime = 300
	oldRunTime = 0

	currentConditions = StringProperty()
	forecastString = StringProperty()

	day1 = StringProperty()
	day2 = StringProperty()
	day3 = StringProperty()
	day4 = StringProperty()
	day5 = StringProperty()

	def __init__(self, **kwargs):
		super(WeatherApp, self).__init__(**kwargs)

		self.currentConditions = "100 F | Thunder"
		self.forecastString = "100 / 500 Thunder"


	def setup(self):
		self.updateData()


	def update(self, *args):
		if args[0] > self.oldRunTime + self.updateTime:
			self.updateData()
			self.oldRunTime = args[0]

	def updateData(self):
		baseurl = "https://query.yahooapis.com/v1/public/yql?q="
		query = 'select * from weather.forecast where woeid in (select woeid from geo.places(1) where text="'+self.location+'")'
		form = "&format=json"
		r = jsonRequests.getResponse(baseurl + query + form)
		
		if r.status:
			item = r["query"]["results"]["channel"]["item"]
			condition = item["condition"]
			forecasts = item["forecast"]

			todayFC = forecasts[0]

			self.forecastString = todayFC["high"] + " / " + todayFC["low"] + " " + weatherCodes.codes[todayFC["code"]]

			self.currentConditions = condition["temp"] + " | " + weatherCodes.codes[condition["code"]]

			self.day1 = forecasts[1]["day"] + " | " + forecasts[1]["high"] + " / " + forecasts[1]["low"] + " " + weatherCodes.codes[forecasts[1]["code"]]
			self.day2 = forecasts[2]["day"] + " | " + forecasts[2]["high"] + " / " + forecasts[2]["low"] + " " + weatherCodes.codes[forecasts[2]["code"]]
			self.day3 = forecasts[3]["day"] + " | " + forecasts[3]["high"] + " / " + forecasts[3]["low"] + " " + weatherCodes.codes[forecasts[3]["code"]]
			self.day4 = forecasts[4]["day"] + " | " + forecasts[4]["high"] + " / " + forecasts[4]["low"] + " " + weatherCodes.codes[forecasts[4]["code"]]
			self.day5 = forecasts[5]["day"] + " | " + forecasts[5]["high"] + " / " + forecasts[5]["low"] + " " + weatherCodes.codes[forecasts[5]["code"]]

		else:
			Logger.Error("WeatherApp: Had trouble getting weather.")

	