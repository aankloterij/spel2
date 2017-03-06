"""
From:
http://programarcadegames.com/python_examples/f.php?file=platform_scroller.py

Explanation video: http://youtu.be/QplXBw_NK5Y

Part of a series:
http://programarcadegames.com/python_examples/f.php?file=move_with_walls_example.py
http://programarcadegames.com/python_examples/f.php?file=maze_runner.py
http://programarcadegames.com/python_examples/f.php?file=platform_jumper.py
http://programarcadegames.com/python_examples/f.php?file=platform_scroller.py
http://programarcadegames.com/python_examples/f.php?file=platform_moving.py
http://programarcadegames.com/python_examples/sprite_sheets/
"""

import pygame

from player import Player
from level import Level, HetLevelVanOnsSpel, Level_01, Platform, TestLevel
from hud import HUD, GameMenu
import constants
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_CENTER

def main():
	""" Main Program """
	pygame.init()

	pygame.font.init()

	# Play shitty annoying music
	pygame.mixer.init()
	pygame.mixer.music.load('res/music.mp3')
	pygame.mixer.music.set_volume(0.01)
	pygame.mixer.music.play(-1)

	# Set the height and width of the screen
	size = [SCREEN_WIDTH, SCREEN_HEIGHT]
	screen = pygame.display.set_mode(size)

	flags = screen.get_flags()

	pygame.display.set_caption("Marcio")

	pygame.display.set_icon(pygame.image.load("res/code.png"))

	# Create the player
	player = Player()

	# Create all the levels
	level_list = []

	# TODO remove this in 'prod'
	# level_list.append(TestLevel(player))
	level_list.append(HetLevelVanOnsSpel(player))

	# Set the current level
	current_level_no = 0
	current_level = level_list[current_level_no]

	active_sprite_list = pygame.sprite.Group()
	player.level = current_level

	player.rect.x = 5 * 30
	player.rect.y = SCREEN_HEIGHT - 5 * 30
	active_sprite_list.add(player)

	hud = HUD(player)

	# Loop until the user clicks the close button.
	done = False

	# Used to manage how fast the screen updates
	clock = pygame.time.Clock()

	# Controls (misschien met een GUI?)
	# Volgens marc kan dat wel als we tijd over hebben, voor nu eerst de spellen afmaken.
	controls_left = [pygame.K_LEFT, pygame.K_a]
	controls_right = [pygame.K_RIGHT, pygame.K_d]
	controls_up = [pygame.K_UP, pygame.K_w, pygame.K_SPACE]

	menu = GameMenu(screen, ('PLAY', 'EXIT', 'RESTART'))
	menu.run()

	# -------- Main Program Loop ----------- #
	while not done:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					menu = GameMenu(screen, ('RESUME', 'EXIT', 'RESTART'))
					menu.run()

				# Toggle fullscreen with F11
				if event.key == pygame.K_F11:
					if flags & pygame.FULLSCREEN == False:
						flags |= pygame.FULLSCREEN
						pygame.display.set_mode(size, flags)
					else:
						flags ^= pygame.FULLSCREEN
						pygame.display.set_mode(size, flags)

				if event.key in controls_left:
					player.go_left()
				if event.key in controls_right:
					player.go_right()
				if event.key in controls_up:
					player.jump()

			if event.type == pygame.KEYUP:
				if event.key in controls_left and player.change_x < 0:
					player.stop()
				if event.key in controls_right and player.change_x > 0:
					player.stop()

		# Update the player.
		active_sprite_list.update()

		# Update items in the level
		current_level.update()

		# Keep the player in the center of the level
		if player.rect.centerx != SCREEN_CENTER:
			diff = SCREEN_CENTER - player.rect.centerx

			if current_level.world_shift < 0:
				player.rect.centerx = SCREEN_CENTER

			if current_level.world_shift + diff > 0:
				diff = -current_level.world_shift

			# De rechterkant van de map werkt dus niet lekker, maak de map maar
			# langer zodat je daar nooit kan komen, ez fix.

			if diff != 0:
				current_level.shift_world(diff)

		usenicefont = False

		if len(player.level.objective_list) == 0:
			usenicefont = True
			dialog = 'Picked up all objectives'
		else:
			if player.next_objective > 0:
				dialog = player.level.objective_list.snippets[player.next_objective - 1]
			else:
				dialog = None


		if player.hits_end():

			if len(player.level.objective_list) != 0:
				usenicefont = True
				dialog = 'Not done yet!'
			else:
				# Increment the current level
				current_level_no += 1

				if current_level_no + 1 > len(level_list):
					print('You sat through the entire game! Good job!')
					exit(0)

				current_level = level_list[current_level_no]

				player.level = current_level

				player.lives = constants.LIVES


		# If the player hits lava,
		# he will lose one heart and get teleported to the start of the level
		if player.in_lava():

			current_level.shift_world(-current_level.world_shift)

			# Teleport the player back to the starting position
			# TODO Teleporting like this doesn't really work
			player.rect.x = 5 * 30
			player.rect.y = constants.SCREEN_HEIGHT - 5 * 30

			# Reduce the amount of lives by one
			player.lives -= 1

			# If the player has 0 hearts left,
			# exit with a message in the console
			# TODO Make this a nice dialog for people who don't run the game from the console
			if player.lives == 0:
				print("Game over, RIP")
				return

		# TODO detect what block we just hit so we can show the code
		# TODO choose to accept the code by pressing `E`
		touching_objectives = player.get_touching_objectives()
		if len(touching_objectives) > 0:
			objective = touching_objectives[0]

			if player.next_objective != objective.index:
				# Verkeerd objective
				current_level.shift_world(-current_level.world_shift)

				# Teleport the player back to the starting position
				player.rect.x = 5 * 30
				player.rect.y = constants.SCREEN_HEIGHT - 5 * 30

				# Reduce the amount of lives by one
				player.lives -= 1

				# If the player has 0 hearts left,
				# exit with a message in the console
				# TODO Make this a nice dialog for people who don't run the game from the console
				if player.lives == 0:
					print("Game over, RIP")
					return
			else:
				# Goed objective
				objective.kill()
				player.next_objective += 1

		# ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
		current_level.draw(screen)
		active_sprite_list.draw(screen)
		hud.draw(screen, dialog, usenicefont)


		# ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT

		# Limit to 60 frames per second
		clock.tick(60)

		# Go ahead and update the screen with what we've drawn.
		pygame.display.flip()

	# Be IDLE friendly. If you forget this line, the program will 'hang'
	# on exit.
	pygame.quit()

def restart_program():
	"""Restarts the current program, with file objects and descriptors
	   cleanup
	"""
	import os
	import sys

	os.execl(sys.executable, sys.executable, *sys.argv)

if __name__ == "__main__":
	main()
