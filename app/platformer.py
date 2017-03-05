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
from level import Level, HetLevelVanOnsSpel, Level_01, Platform
from hud import HUD, GameMenu
import constants
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_CENTER

def main():
	""" Main Program """
	pygame.init()

	pygame.font.init()

	# Set the height and width of the screen
	size = [SCREEN_WIDTH, SCREEN_HEIGHT]
	screen = pygame.display.set_mode(size)

	pygame.display.set_caption("Marcio")

	pygame.display.set_icon(pygame.image.load("res/player.png"))

	# Create the player
	player = Player()

	# Create all the levels
	level_list = []
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

	# -------- Main Program Loop -----------
	while not done:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					menu = GameMenu(screen, ('Start', 'Lol'))
					menu.run()

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
		print(current_level.world_shift)

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

		dialog = None

		# TODO detect what block we just hit so we can show the code
		# TODO choose to accept the code by pressing `E`
		if player.hits_objective():
			dialog = "You just hit something :D"

		# ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
		current_level.draw(screen)
		active_sprite_list.draw(screen)
		hud.draw(screen, dialog)

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
	import psutil

	p = psutil.Process(os.getpid())
	for handler in p.get_open_files() + p.connections():
		os.close(handler.fd)

	python = sys.executable
	os.execl(python, python, *sys.argv)

if __name__ == "__main__":
	main()
