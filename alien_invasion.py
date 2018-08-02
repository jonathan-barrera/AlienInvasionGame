import pygame
from settings import Settings
from game_stats import GameStats
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from button import Button
from scoreboard import Scoreboard
import time

def run_game():
	# Initialize pygame, settings, and screen object.
	pygame.init()
	ai_settings = Settings()
	screen = pygame.display.set_mode(
		(ai_settings.screen_width, ai_settings.screen_height))

	pygame.display.set_caption("Alien Invasion")

	# Make the Play button.
	play_button = Button(ai_settings, screen, "Play")

	# Create an instance to store game statistics and create a scoreboard.
	stats = GameStats(ai_settings)
	sb = Scoreboard(ai_settings, screen, stats)

	# Make a ship, a group of bullets, a group of alienbullets, and a group of aliens.
	ship = Ship(ai_settings, screen)
	alien_bullets = Group()
	bullets = Group()
	aliens = Group()

	# Create the fleet of aliens.
	gf.create_fleet(ai_settings, screen, ship, aliens)

	# Initialize the time (used for timing alien bullets)
	t = time.time()

	# Start the main loop for the game.
	while True:
		gf.check_events(ai_settings, screen, stats, sb, play_button, 
			ship, aliens, bullets, alien_bullets)

		if stats.game_active:
			ship.update()
			gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, alien_bullets)
			gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets, alien_bullets)
			gf.update_alien_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, alien_bullets)

			# Check the time to see if alien bullet should be fired
			if time.time() - ai_settings.alien_bullet_time_gap > t:
				gf.fire_alien_bullet(ai_settings, screen, aliens, alien_bullets)
				t = time.time()
		
		gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, alien_bullets, play_button)

run_game()