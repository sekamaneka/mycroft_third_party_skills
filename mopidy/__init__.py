import time
from os.path import dirname
import os
import subprocess
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
		self.load_regex_files(dirname(__file__))

		play_intent = IntentBuilder("PlayIntent").require("PlayMusic").build()
                self.register_intent(play_intent, self.handle_play_intent)

		pause_intent = IntentBuilder("PauseIntent").require("PauseMusic").build()
                self.register_intent(pause_intent, self.handle_pause_intent)

		next_song_intent = IntentBuilder("NextSongIntent").require("NextSong").build()
                self.register_intent(next_song_intent, self.handle_next_song_intent)

		lower_volume_intent = IntentBuilder("LowerVolumeIntent").require("LowerVolume").build()
                self.register_intent(lower_volume_intent, self.handle_lower_volume_intent)

		raise_volume_intent = IntentBuilder("RaiseVolumeIntent").require("RaiseVolume").build()
                self.register_intent(raise_volume_intent, self.handle_raise_volume_intent)
		
		find_add_intent = IntentBuilder("FindAddIntent").require("Play").optionally("Songname").build()
                self.register_intent(find_add_intent, self.handle_find_add_intent)


	def handle_play_intent(self, message):	
		os.system('mpc play')	

	def handle_pause_intent(self, message):	
		os.system('mpc pause')	

	def handle_next_song_intent(self, message):	
		os.system('mpc next')	
	
	def handle_lower_volume_intent(self, message):	
		os.system('mpc volume -25')	

	def handle_raise_volume_intent(self, message):	
		os.system('mpc volume +25')	

	def handle_find_add_intent(self, message):
		#Songname is taken from the regex capture group after saying play			
		#It then gets all results but returns only the first to be added
		#The playlist gets cleared and it play only this one song
		#if i get annoyed by the mpc stdout		#devnull = open('/dev/null', 'w')
								#process = subprocess.call([""], stdout=devnull)

		songName = message.metadata.get("Songname", None)
		result = subprocess.check_output(["mpc", "find", "any", songName])
		first_result = result.split('\n')[0]	
		subprocess.call(["mpc", "clear", "--wait"])
		find_add_query = "yt:https://www.youtube.com/watch?v=" + first_result[-11:]
	        subprocess.call(["mpc", "insert", find_add_query]) 	
		subprocess.call(["mpc", "play"])

	def stop(self):
    		pass

def create_skill():
	return MusicSkill()

