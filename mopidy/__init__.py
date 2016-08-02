from os.path import dirname
import os
import binascii 
from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger

__author__= 'best'
LOGGER = getLogger(__name__)

class MusicSkill(MycroftSkill):
	def __init__(self):
		super(MusicSkill, self).__init__(name="MusicSkill")


	def initialize(self):
    		self.load_data_files(dirname(__file__))

		play_intent = IntentBuilder("PlayIntent").require("PlayMusic").build()
                self.register_intent(play_intent, self.handle_play_intent)

	def handle_play_intent(self, message):	
		os.system('mpc play')	
	def stop(self):
    		pass

def create_skill():
	return MusicSkill()

