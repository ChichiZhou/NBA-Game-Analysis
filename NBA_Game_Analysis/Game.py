import pandas as pd
from Event import Event
from Team import Team
from Constant import Constant


class Game:

	def __init__(self, path_to_json):
		self.home_team = None
		self.guest_team = None
		self.event = None
		self.path_to_json = path_to_json


	def read_json(self):
		data_frame = pd.read_json(self.path_to_json)
		event = data_frame['events']
		self.event = Event(event)
		self.home_team = Team(event['home']['teamid'])
		self.guest_team = Team(event['visitor']['teamid'])
	def start(self):
		self.event.final_show()
