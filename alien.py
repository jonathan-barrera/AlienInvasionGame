import pygame
from pygame.sprite import Sprite
from random import randint

class Alien(Sprite):
	""" A class to represent a single alien in the fleet."""

	def __init__(self, ai_settings, screen):
		""" Initialize the alien and set its starting position."""
		super(Alien, self).__init__()
		self.screen = screen
		self.ai_settings = ai_settings

		# Load the alien image and set its rect attribute.
		self.image = pygame.image.load('images/alien.bmp')
		self.rect = self.image.get_rect()

		# Start each new alien near the top left of the screen.
		self.rect.x = self.rect.width
		self.rect.y = self.rect.height

		# Store the alien's exact postion.
		self.x = float(self.rect.x)

	def blitme(self):
		"""Draw the alien at its current location."""
		self.screen.blit(self.image, self.rect)

	def update(self):
		"""Move the alien right or left."""
		self.x += (self.ai_settings.alien_speed_factor *
						self.ai_settings.fleet_direction)
		self.rect.x = self.x

	def check_right_edge(self):
		"""Return True if alien is at edge of right range."""
		alien_range_right = self.ai_settings.alien_range_right
		if self.rect.right >= alien_range_right:
			return True

	def check_left_edge(self):
		"""Return True if alien is at edge of left range."""
		alien_range_left = self.ai_settings.alien_range_left
		if self.rect.left <= alien_range_left:
			return True


