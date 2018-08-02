class Settings():
	"""A class to store all settings for Alien Invasion."""

	def __init__(self):
		"""Initialize the game's static settings."""
		# Screen settings
		self.screen_width = 1200
		self.screen_height = 800
		self.bg_color = (230, 230, 230)

		# Ship settings
		self.ship_limit = 2

		# Bullet settings
		self.bullet_width = 3
		self.bullet_height = 15
		self.bullet_color = 60, 60, 60
		self.bullets_allowed = 10

		# Alien Bullet settings
		self.alien_bullet_color = 255, 30, 30

		# Alien settings
		self.fleet_drop_speed = 10

		# How quickly the game speeds up
		self.speedup_scale = 1.25

		# How quickly the alien point values increase
		self.score_scale = 1.5

		self.initialize_dynamic_settings()

	def initialize_dynamic_settings(self):
		"""Initialize settings that change throughout the game."""
		self.ship_speed_factor = 7
		self.bullet_speed_factor = 12
		self.alien_speed_factor = 5
		self.alien_bullet_speed_factor = 6
		self.alien_bullet_time_gap = 3 #seconds

		# fleet_direction of 1 represents right; -1 represents left.
		self.fleet_direction = 1

		# Scoring
		self.alien_points = 50

		self.reset_alien_range()

	def reset_alien_range(self):
		# Alien range
		self.alien_range_right = self.screen_width
		self.alien_range_left = 0

	def increase_speed(self):
		"""Increase speed settings and alien point values."""
		self.ship_speed_factor *= self.speedup_scale
		self.bullet_speed_factor *= self.speedup_scale
		self.alien_speed_factor *= self.speedup_scale
		self.alien_bullet_speed_factor *= self.speedup_scale
		self.alien_bullet_time_gap /= self.speedup_scale

		self.alien_points = int(self.alien_points * self.score_scale)

