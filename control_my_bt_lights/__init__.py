from os.path import dirname
import os
import binascii 
from colour import Color
import subprocess
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
                self.load_regex_files(dirname(__file__))

 		color_intent = IntentBuilder("ColorIntent").require("change").require("LampColor").build()
                self.register_intent(color_intent, self.handle_color_intent)

#		on_intent = IntentBuilder("OnIntent").require("on").build()
#                self.register_intent(on_intent, self.handle_on_intent)
#		
#		off_intent = IntentBuilder("OffIntent").require("off").build()
#		self.register_intent(off_intent, self.handle_off_intent)

		party_intent = IntentBuilder("PartyIntent").require("party").build()
                self.register_intent(party_intent, self.handle_party_intent)

        def handle_color_intent(self, message):
		lampColor = message.metadata.get("LampColor", None)
		try:
			hex_value = Color(lampColor).hex
			#transforming from 3 hex to 6 hex if needed
			#and mapping RGB to BGR
			if len(hex_value)==4:
				hex_value = hex_value[3]+hex_value[3]+hex_value[2]+hex_value[2]+hex_value[1]+hex_value[1]
			else:
				hex_value = hex_value[5]+hex_value[6]+hex_value[3]+hex_value[4]+hex_value[1]+hex_value[2]
				LOGGER.info(hex_value)
                	subprocess.call(["sudo", "gatttool", "-b", "68:9E:19:16:64:33", "--char-write-req", "-a", "0x002d", "-n", hex_value])
               		self.speak_dialog("speaksies")
		except:
               		LOGGER.info(lampColor)

	def handle_party_intent(self, message):	
		for i in range(100):
			r = binascii.b2a_hex(os.urandom(4))
			cmd = "sudo gatttool -b 68:9E:19:16:64:33 --char-write-req -a 0x002d -n " + "00" + r
			os.system(cmd)
			cmd = "sudo gatttool -b 68:9E:19:16:64:33 --char-write-req -a 0x002d -n " + r + "00"
			os.system(cmd)
			cmd = "sudo gatttool -b 68:9E:19:16:64:33 --char-write-req -a 0x002d -n " + r[:2] + "00" + r[2:]
			os.system(cmd)

#	def handle_off_intent(self, message):
#                os.system('sudo gatttool -b 68:9E:19:16:64:33 --char-write-req -a 0x002d -n 00000000')
#                self.speak_dialog("speaksies")
#	def handle_on_intent(self, message):
#                os.system('sudo gatttool -b 68:9E:19:16:64:33 --char-write-req -a 0x002d -n ffffffff')
#                self.speak_dialog("speaksies")

	def stop(self):
    		pass

def create_skill():
	return ColorSkill()

