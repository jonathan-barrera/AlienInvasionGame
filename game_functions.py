import sys
import pygame
from bullet import Bullet
from alien_bullet import AlienBullet
from alien import Alien
from time import sleep
from random import randint
import time
import threading

def check_keydown_events(event, ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, alien_bullets):
	"""Respond to keypresses."""
	if event.key == pygame.K_RIGHT:
		ship.moving_right = True
	elif event.key == pygame.K_LEFT:
		ship.moving_left = True
	elif event.key == pygame.K_SPACE:
		fire_bullet(ai_settings, screen, ship, bullets)
	elif event.key == pygame.K_q:
		if stats.score >= stats.high_score:
			stats.store_high_score()
		sys.exit()
	elif event.key == pygame.K_p:
		start_game(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, alien_bullets)

def fire_bullet(ai_settings, screen, ship, bullets):
	"""Fire a bullet if limit no yet reached."""
	#Create a new bullet and add it to the bullets group.
	if len(bullets) < ai_settings.bullets_allowed:
		new_bullet = Bullet(ai_settings, screen, ship)
		bullets.add(new_bullet)

def fire_alien_bullet(ai_settings, screen, aliens, alien_bullets):
	"""Fire an alien bullet from a random alien every 5 seconds"""
	try:
		#Choose a random alien
		alien_sprites_list = aliens.sprites()
		rand_alien_index = randint(0, len(alien_sprites_list))
		chosen_alien = alien_sprites_list[rand_alien_index]

		#Have the chosen alien fire an alien bullet
		new_alien_bullet = AlienBullet(ai_settings, screen, chosen_alien)
		alien_bullets.add(new_alien_bullet)
	except IndexError:
		pass

def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, alien_bullets):
	"""Update the position of bullets and get rid of old bullets."""
	# Update bullet positions.
	bullets.update()

	#Get rid of bullets that have disappeared.
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)

	check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets, alien_bullets)

def update_alien_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, alien_bullets):
	"""Update the position of the alien bullets and get rid of old bullets."""
	# Update bullets positions.
	alien_bullets.update()

	#Get fird of bullets that have disappeared.
	for alien_bullet in alien_bullets.copy():
		if alien_bullet.rect.top >= ai_settings.screen_height:
			alien_bullets.remove(alien_bullet)

	check_alien_bullet_ship_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets, alien_bullets)

def start_new_level(ai_settings, screen, stats, sb, ship, aliens, bullets, alien_bullets):
	# start a new level.
		alien_bullets.empty()
		bullets.empty()
		ai_settings.increase_speed()

		# Increase level.
		stats.level += 1
		sb.prep_level()

		# Reset alien range
		ai_settings.reset_alien_range()

		# Create new fleet
		create_fleet(ai_settings, screen, ship, aliens)

def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets, alien_bullets):
	"""Respond to bullet-alien collisions"""
	# If so, get rid of the bullet and the alien.
	collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
	if collisions:
		for aliens in collisions.values():
			stats.score += ai_settings.alien_points * len(aliens)
			sb.prep_score()
		check_high_scores(stats, sb)

	if len(aliens) == 0:
		start_new_level(ai_settings, screen, stats, sb, ship, aliens, bullets, alien_bullets)

def check_alien_bullet_ship_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets, alien_bullets):
	"""Respond to alien bullet-ship collisions"""
	# If so, get rid of the bullet and the alien.
	collisions = pygame.sprite.spritecollideany(ship, alien_bullets)
	if collisions:
		ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, alien_bullets)

def check_keyup_events(event, ship):
	"""Respond to key releases."""
	if event.key == pygame.K_RIGHT:
		ship.moving_right = False
	elif event.key == pygame.K_LEFT:
		ship.moving_left = False

def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, alien_bullets):
	"""Respond to keypresses and mouse events."""
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			if stats.score >= stats.high_score:
				stats.store_high_score()
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			check_keydown_events(event, ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, alien_bullets)
		elif event.type == pygame.KEYUP:
			check_keyup_events(event, ship)
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x, mouse_y = pygame.mouse.get_pos()
			check_play_button(ai_settings, screen, stats, sb,
				play_button, ship, aliens, bullets, alien_bullets, mouse_x, mouse_y)

def start_game(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, alien_bullets):
	# Hide the mouse cursor.
	pygame.mouse.set_visible(False)

	# Reset the game statistics.
	stats.reset_stats(ai_settings)
	stats.game_active = True

	# Reset the scorebaord images.
	sb.prep_score()
	sb.prep_high_score()
	sb.prep_level()
	sb.prep_ships()

	# Empty the list of aliens and bullets.
	aliens.empty()
	bullets.empty()
	alien_bullets.empty()

	# Create a new fleet and center the ship.
	create_fleet(ai_settings, screen, ship, aliens)
	ship.center_ship()

	# Start firing alien bullets
	fire_alien_bullet(ai_settings, screen, aliens, alien_bullets)

def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, alien_bullets, mouse_x, mouse_y):
	"""Start a new game when the player clicks Play."""
	button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
	if button_clicked and not stats.game_active:
		# Reset the game settings
		

		start_game(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, alien_bullets)

def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, alien_bullets, play_button):
	"""Update images on the screen and flip to the new screen."""
	# Redraw the screen during each pass through the loop
	screen.fill(ai_settings.bg_color)

	#Redraw all bullets behind ship and aliens.
	for bullet in bullets.sprites():
		bullet.draw_bullet()

	#Redraw all alien_bullets behind ship and aliens.
	for alien_bullet in alien_bullets.sprites():
		alien_bullet.draw_bullet()

	ship.blitme()
	aliens.draw(screen)

	# Draw the score information.
	sb.show_score()

	# Draw the play button if the game is inactive.
	if not stats.game_active:
		play_button.draw_button()

	# Make the most recently drawn screen visible.
	pygame.display.flip()

def get_number_rows(ai_settings, ship_height, alien_height):
	"""Determine the number of rows of aliens that fit on the screen."""
	avialable_space_y = (ai_settings.screen_height - 
							(3 * alien_height) - ship_height)
	number_rows = int(avialable_space_y / (2 * alien_height))
	return number_rows

def get_number_aliens_x(ai_settings, alien_width):
	"""Determine the number of aliens that fit in a row."""
	avialable_space_x = ai_settings.screen_width - 2 * alien_width
	number_aliens_x = int(avialable_space_x/(2 * alien_width))
	return number_aliens_x

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
	"""Create and alien and place it in the row."""
	alien = Alien(ai_settings, screen)
	alien_width = alien.rect.width
	alien.x = alien_width + 2 * alien_width * alien_number
	alien.rect.x = alien.x
	alien.y = alien.rect.height + (2 * alien.rect.height * row_number)
	alien.rect.y = alien.y
	aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
	"""Create a full fleet of aliens."""
	# Create an alien and find the nubmer of aliens in a row.
	alien = Alien(ai_settings, screen)
	number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
	number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

	# Create the fleet of aliens.
	for row_number in range(number_rows):
		for alien_number in range(number_aliens_x):
			create_alien(ai_settings, screen, aliens, alien_number, row_number)

def check_fleet_edges(ai_settings, aliens):
	"""Respond appropriately if any aliens have reached an edge."""
	for alien in aliens.sprites():
		if alien.check_right_edge():
			update_range_left(ai_settings, aliens)
			change_fleet_direction(ai_settings, aliens)
			break
		elif alien.check_left_edge():
			update_range_right(ai_settings, aliens)
			change_fleet_direction(ai_settings, aliens)
			break

def update_range_left(ai_settings, aliens):
	x_values = []
	for alien in aliens.sprites():
		x_value = alien.rect.x 
		x_values.append(x_value)
	min_x = min(x_values)
	if min_x - 120 <= 0:
		alien_range_left = 0
	else:
		ai_settings.alien_range_left = randint(0, min_x - 120)

def update_range_right(ai_settings, aliens):
	x_values = []
	for alien in aliens.sprites():
		x_value = alien.rect.x 
		x_values.append(x_value)
	max_x = max(x_values)
	if max_x + 120 >= ai_settings.screen_width:
		alien_range_right = ai_settings.screen_width
	else:
		ai_settings.alien_range_right = randint(max_x + 120, ai_settings.screen_width)

def change_fleet_direction(ai_settings, aliens):
	"""Drop the entire fleet and change the fleet's direciton and update the x range for the alien."""
	for alien in aliens.sprites():
		alien.rect.y += ai_settings.fleet_drop_speed
	ai_settings.fleet_direction *= -1

def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, alien_bullets):
	"""Respond to ship being hit by alien."""
	if stats.ships_left > 0:
		# Decrement ship_left.
		stats.ships_left -= 1

		# Update scoreboard.
		sb.prep_ships()

		# Empty the list of aliens and bullets.
		aliens.empty()
		bullets.empty()
		alien_bullets.empty()

		# Create a new fleet and center the ship.
		create_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()

		# Pause.
		sleep(0.5)

	else:
		if stats.score >= stats.high_score:
			stats.store_high_score()
		stats.game_active = False
		pygame.mouse.set_visible(True)

def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets, alien_bullets):
	"""
	Check if the fleet is at an edge,
		and then update the positions of all aliens in the fleet.
	"""
	check_fleet_edges(ai_settings, aliens)
	aliens.update()

	# Look for alien-ship collision.
	if pygame.sprite.spritecollideany(ship, aliens):
		ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, alien_bullets)

	# Look for aliens hitting the bottom of the screen.
	check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets, alien_bullets)


def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets, alien_bullets):
	"""Check if any aliens have reached the bottom of the screen."""
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			# Treat this the same as if the ship got hit.
			ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, alien_bullets)
			break

def check_high_scores(stats, sb):
	"""Check to see if there's a new high score."""
	if stats.score > stats.high_score:
		stats.high_score = stats.score
		sb.prep_high_score()

