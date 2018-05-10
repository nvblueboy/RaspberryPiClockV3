from kivy.app import App
from kivy.config import Config
from kivy.uix.carousel import Carousel
from kivy.uix.image import AsyncImage
from kivy.clock import Clock
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import StringProperty
from kivy.logger import Logger

import time

import WeatherApp
import DisneylandApp


class RPIClock(RelativeLayout):
	def __init__(self, **kwargs):
		super(RPIClock, self).__init__(**kwargs)

	def setup(self):
		for child in self.children[0].children:
			setupFN = getattr(child, "setup", None)
			if callable(setupFN):
				child.setup()

	def update(self, *args):
		for child in self.children[0].children:
			updateFN = getattr(child, "update", None)
			if callable(updateFN):
				child.update(args)

class CarouselScreen(RelativeLayout):
	oldTime = 0
	runTime = 0
	frameStartTime = 0
	length = 8

	def __init__(self, **kwargs):
		super(CarouselScreen, self).__init__(**kwargs)

	def update(self, *args):
		if int(time.time()) != self.oldTime:
			self.oldTime = int(time.time())
			self.runTime += 1

			if self.runTime - self.frameStartTime >= self.length:
				self.ids.Carousel.load_next()
				self.frameStartTime = self.runTime

		for child in self.ids.Carousel.slides:
			updateFN = getattr(child, "update", None)
			if callable(updateFN):
				child.update(self.runTime)

	def setup(self):
		for child in self.ids.Carousel.slides:
			setupFN = getattr(child, "setup", None)
			if callable(setupFN):
				child.setup()

class TestApp(RelativeLayout):
	def __init__(self, **kwargs):
		super(TestApp, self).__init__(**kwargs)

class ClockScreen(RelativeLayout):

	hours = StringProperty()
	minutes = StringProperty()

	date = StringProperty()

	def __init__(self, **kwargs):
		super(ClockScreen, self).__init__(**kwargs)

		date = "5.9.18"

	def update(self, *args):
		self.hours = time.strftime("%I")
		self.minutes = time.strftime("%M")

		month = time.strftime("%m").lstrip("0")
		day = time.strftime("%d").lstrip("0")
		year = time.strftime("%y")

		self.date = month + "." + day + "." + year



class RPIClockApp(App):
	def build(self):
		Config.set('graphics','width','800')
		Config.set('graphics','height','480')

		#Set configuration settings.
		Config.set('kivy', 'log_level', 'info')
		Config.set('kivy', 'log_dir', "logs")
		Config.set('kivy', 'log_name', "log_%y_%m_%d_%H_%M_%S.txt")
		Config.set('kivy', 'log_enable', 1)
		Config.set('kivy', 'log_maxfile', 25)

		self.load_kv('RPIClock.kv')

		self.appWindow = RPIClock()

		Clock.schedule_interval(self.appWindow.update, .2)

		return self.appWindow

	def on_start(self, **kwargs):
		self.appWindow.setup()


if __name__ == "__main__":
	print("Loading app...")
	RPIClockApp().run()