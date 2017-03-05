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

import player
from level import Level, LevelFromImage, Level_01, Platform
from hud import HUD
import constants

def main():
	""" Main Program """
	pygame.init()

	pygame.font.init()

	# Set the height and width of the screen
	size = [constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT]
	screen = pygame.display.set_mode(size)

	flags = screen.get_flags()

	pygame.display.set_caption("Marcio")

	pygame.display.set_icon(pygame.image.load("res/player.png"))

	# Create the player
	_player = player.Player()

	# Create all the levels
	level_list = []
	level_list.append(LevelFromImage(_player, "res/level1.png"))

	# Set the current level
	current_level_no = 0
	current_level = level_list[current_level_no]

	active_sprite_list = pygame.sprite.Group()
	_player.level = current_level

	_player.rect.x = 5 * 30
	_player.rect.y = constants.SCREEN_HEIGHT - 5 * 30
	active_sprite_list.add(_player)

	hud = HUD(_player)

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
					done = True

				# Toggle fullscreen with F11
				if event.key == pygame.K_F11:
					if flags & pygame.FULLSCREEN == False:
						flags |= pygame.FULLSCREEN
						pygame.display.set_mode(size, flags)
					else:
						flags ^= pygame.FULLSCREEN
						pygame.display.set_mode(size, flags)

				if event.key in controls_left:
					_player.go_left()
				if event.key in controls_right:
					_player.go_right()
				if event.key in controls_up:
					_player.jump()

			if event.type == pygame.KEYUP:
				if event.key in controls_left and _player.change_x < 0:
					_player.stop()
				if event.key in controls_right and _player.change_x > 0:
					_player.stop()

		# Update the player.
		active_sprite_list.update()

		# Update items in the level
		current_level.update()

		# If the player gets near the right side, shift the world left (-x)
		if _player.rect.right >= 500:
			diff = _player.rect.right - 500
			_player.rect.right = 500
			current_level.shift_world(-diff)

		# If the player gets near the left side, shift the world right (+x)
		if _player.rect.left <= 120:
			diff = 120 - _player.rect.left
			_player.rect.left = 120
			current_level.shift_world(diff)

		# If the player gets to the end of the level, go to the next level
		current_position = _player.rect.x + current_level.world_shift
		if current_position < current_level.level_limit:
			_player.rect.x = 120
			if current_level_no < len(level_list)-1:
				current_level_no += 1
				current_level = level_list[current_level_no]
				_player.level = current_level

		dialog = None

		# TODO detect what block we just hit so we can show the code
		# TODO choose to accept the code by pressing `E`
		if _player.hits_objective():
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

if __name__ == "__main__":
	main()
