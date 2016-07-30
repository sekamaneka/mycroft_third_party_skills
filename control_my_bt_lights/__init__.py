from os.path import dirname
import os

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger

__author__= 'best'
LOGGER = getLogger(__name__)

class ColorSkill(MycroftSkill):
	def __init__(self):
		super(ColorSkill, self).__init__(name="ColorSkill")


	def initialize(self):
    		self.load_data_files(dirname(__file__))

		red_intent = IntentBuilder("RedIntent").require("red").build()
		self.register_intent(red_intent, self.handle_red_intent)
		
		blue_intent = IntentBuilder("BlueIntent").require("blue").build()
                self.register_intent(blue_intent, self.handle_blue_intent)
		
		green_intent = IntentBuilder("GreenIntent").require("green").build()
                self.register_intent(green_intent, self.handle_green_intent)
		
		on_intent = IntentBuilder("OnIntent").require("on").build()
                self.register_intent(on_intent, self.handle_on_intent)
		
		off_intent = IntentBuilder("OffIntent").require("off").build()
		self.register_intent(off_intent, self.handle_off_intent)

	def handle_red_intent(self, message):
		os.system('sudo gatttool -b 68:9E:19:16:64:33 --char-write-req -a 0x002d -n 0000ff00')
    		self.speak_dialog("speaksies")
	def handle_blue_intent(self, message):
		os.system('sudo gatttool -b 68:9E:19:16:64:33 --char-write-req -a 0x002d -n ff000000')
                self.speak_dialog("speaksies")
	def handle_green_intent(self, message):
                os.system('sudo gatttool -b 68:9E:19:16:64:33 --char-write-req -a 0x002d -n 00ff0000')
                self.speak_dialog("speaksies")
	def handle_off_intent(self, message):
                os.system('sudo gatttool -b 68:9E:19:16:64:33 --char-write-req -a 0x002d -n 00000000')
                self.speak_dialog("speaksies")
	def handle_on_intent(self, message):
                os.system('sudo gatttool -b 68:9E:19:16:64:33 --char-write-req -a 0x002d -n ffffffff')
                self.speak_dialog("speaksies")

	def stop(self):
    		pass

def create_skill():
	return ColorSkill()

