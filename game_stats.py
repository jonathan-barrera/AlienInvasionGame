import json

class GameStats():
	"""Track statistics for Alien Invasion."""

	def __init__(self, ai_settings):
		"""Initialize statistics."""
		self.ai_settings = ai_settings
		self.reset_stats(ai_settings)

		# Start Alien Invasion in an active state.
		self.game_active = False

		# Import all-time high score
		self.f_name = 'alien_invasion_high_score.json'
		try:
			with open(self.f_name) as f_obj:
				self.high_score = json.load(f_obj)
		except FileNotFoundError:
			self.high_score = 0 
	
	def reset_stats(self, ai_settings):
		"""Initialize statistics that can change during the game."""
		self.ships_left = self.ai_settings.ship_limit
		self.score = 0
		self.level = 1
		ai_settings.initialize_dynamic_settings()

	def store_high_score(self):
		"""Save the high score in a json file."""
		with open(self.f_name, 'w') as f_obj:
				json.dump(self.score, f_obj)