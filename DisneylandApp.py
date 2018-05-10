from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.core.image import Image
from kivy.properties import StringProperty
from kivy.logger import Logger


import time
import disneyland

class DisneylandApp(BoxLayout):

	updateTime = 600
	oldRunTime = 0


	def __init__(self, **kwargs):
		super(DisneylandApp, self).__init__(**kwargs)


	def update(self, *args):
		if args[0] > self.oldRunTime + self.updateTime:
			self.oldRunTime = args[0]
			self.updateData()

	def setup(self):
		for child in self.children:
			setupFN = getattr(child, "setup", None)
			if callable(setupFN):
				child.setup()

		self.updateData()

	def updateData(self):
		data = disneyland.get_wait_times()
		hours = disneyland.get_hours()
		for child in self.children:
			updateFN = getattr(child, "updateTimes", None)
			if callable(updateFN):
				child.updateTimes(data)
			hoursFN = getattr(child, "updateHours", None)
			if callable(hoursFN):
				child.updateHours(hours)

class RideTime(RelativeLayout):

	waitTime = StringProperty()
	rideName = StringProperty()

	def __init__(self, **kwargs):
		super(RideTime, self).__init__(**kwargs)

		
		self.waitTime = "Indy: Forever"

	def setup(self):
		self.rideName = disneyland.names[self.rideName]

	def updateTimes(self, data):
		if self.rideName in data.keys():
			self.waitTime = disneyland.displayNames[self.rideName] + ": "+str(data[self.rideName])
		else:
			self.waitTime = disneyland.displayNames[self.rideName] + ": N/A"

class Hours(RelativeLayout):
	hours = StringProperty()
	park = StringProperty()
	parkCode = ""

	def __init__(self, **kwargs):
		super(Hours, self).__init__(**kwargs)

		hours = "Test"

	def setup(self):
		print("Park setup run")
		if self.park == "DCA":
			self.parkCode = "DCA"
			self.park = "California Adventure"
		if self.park == "DL":
			self.parkCode = "DL"
			self.park = "Disneyland"
		print(self.park)

	def updateHours(self,data):
		if self.parkCode == "DL":
			self.hours = data[0]
		if self.parkCode == "DCA":
			self.hours = data[1]
		print(self.park + self.hours)

