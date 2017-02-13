"""
Sample Python/Pygame Programs
Simpson College Computer Science
http://programarcadegames.com/
http://simpson.edu/computer-science/

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

# Global constants

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

WATER = (0, 182, 233)

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Entity(pygame.sprite.Sprite):
	"""
	This class represents a movable object in the game.
	"""
	def __init__(self):
		super().__init__()


class Player(Entity):
	"""
	This class represents the player that can be controlled.
	"""

	# -- Methods
	def __init__(self):
		""" Constructor function """

		# Call the parent's constructor
		super().__init__()

		# Create an image of the block, and fill it with a color.
		# This could also be an image loaded from the disk.
		width = 200
		height = 320
		# self.image = pygame.Surface([width, height])
		# self.image.fill(RED)

		self.image = pygame.image.load('res/player.png').convert_alpha()

		# Set a referance to the image rect.
		self.rect = self.image.get_rect()

		# Set speed vector of player
		self.change_x = 0
		self.change_y = 0

		# List of sprites we can bump against
		self.level = None

	def update(self):
		""" Move the player. """

		self.is_in_water = self.in_water()

		# Gravity
		self.calc_grav()

		# Move left/right
		self.rect.x += self.change_x

		# See if we hit anything
		block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
		for block in block_hit_list:
			# If we are moving right,
			# set our right side to the left side of the item we hit
			if self.change_x > 0:
				self.rect.right = block.rect.left
			elif self.change_x < 0:
				# Otherwise if we are moving left, do the opposite.
				self.rect.left = block.rect.right

		# Move up/down
		self.rect.y += self.change_y

		# Check and see if we hit anything
		block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
		for block in block_hit_list:

			# Reset our position based on the top/bottom of the object.
			if self.change_y > 0:
				self.rect.bottom = block.rect.top
			elif self.change_y < 0:
				self.rect.top = block.rect.bottom

			# Stop our vertical movement
			self.change_y = 0

	def calc_grav(self):
		""" Calculate effect of gravity. """

		if self.change_y == 0:
			self.change_y = 1 if not self.is_in_water else 0.5
		else:
			# Downward velocity in water is at most 5. This makes sure that the
			# player loses y-velocity when he falls into the water with a
			# high velocity downwards.
			self.change_y = self.change_y + .35 if not self.is_in_water else min(self.change_y + .35, 5)

		# See if we are on the ground.
		if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
			self.change_y = 0
			self.rect.y = SCREEN_HEIGHT - self.rect.height

	def in_water(self):
		return len(pygame.sprite.spritecollide(self, self.level.water_list, False)) > 0

	def jump(self):
		""" Called when user hits 'jump' button. """

		# move down a bit and see if there is a platform below us.
		# Move down 2 pixels because it doesn't work well if we only move down 1
		# when working with a platform moving down.
		self.rect.y += 2
		platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
		self.rect.y -= 2

		# If it is ok to jump, set our speed upwards
		if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT or self.is_in_water:
			self.change_y = -10 if not self.is_in_water else -7

	# Player-controlled movement:
	def go_left(self):
		""" Called when the user hits the left arrow. """
		self.change_x = -6

	def go_right(self):
		""" Called when the user hits the right arrow. """
		self.change_x = 6

	def stop(self):
		""" Called when the user lets off the keyboard. """
		self.change_x = 0


class Platform(pygame.sprite.Sprite):
	""" Platform the user can jump on """

	def __init__(self, width, height, color=GREEN):
		""" Platform constructor. Assumes constructed with user passing in
			an array of 5 numbers like what's defined at the top of this code.
			"""
		super().__init__()

		self.image = pygame.Surface([width, height])
		self.image.fill(color)

		self.rect = self.image.get_rect()


class Level():
	""" This is a generic super-class used to define a level.
		Create a child class for each level with level-specific
		info. """

	def __init__(self, player):
		""" Constructor. Pass in a handle to player. Needed for when moving
			platforms collide with the player. """
		self.platform_list = pygame.sprite.Group()
		self.water_list = pygame.sprite.Group()
		self.enemy_list = pygame.sprite.Group()
		self.player = player

		# How far this world has been scrolled left/right
		self.world_shift = 0

	# Update everythign on this level
	def update(self):
		""" Update everything in this level."""
		self.platform_list.update()
		self.enemy_list.update()
		self.water_list.update()

	def draw(self, screen):
		""" Draw everything on this level. """

		# Draw the background
		screen.fill(BLUE)

		# Draw all the sprite lists that we have
		self.platform_list.draw(screen)
		self.water_list.draw(screen)
		self.enemy_list.draw(screen)

	def shift_world(self, shift_x):
		""" When the user moves left/right and we need to scroll
		everything: """

		# Keep track of the shift amount
		self.world_shift += shift_x

		# Go through all the sprite lists and shift
		for platform in self.platform_list:
			platform.rect.x += shift_x

		for enemy in self.enemy_list:
			enemy.rect.x += shift_x

		for water in self.water_list:
			water.rect.x += shift_x


# Create platforms for the level
class Level_01(Level):
	""" Definition for level 1. """

	def __init__(self, player):
		""" Create level 1. """

		# Call the parent constructor
		Level.__init__(self, player)

		self.level_limit = -1000

		# Array with width, height, x, and y of platform
		level = [[210, 70, 500, 500],
				 [210, 70, 800, 400],
				 [210, 70, 1000, 500],
				 [210, 70, 1120, 280],
			]

		# Go through the array above and add platforms
		for platform in level:
			block = Platform(platform[0], platform[1])
			block.rect.x = platform[2]
			block.rect.y = platform[3]
			block.player = self.player
			self.platform_list.add(block)

class LevelFromImage(Level):
	""" Try to generate a level from an image.
	Note that each pixel in the image represents a block () """

	def __init__(self, player, source):
		""" Create a level from an image. """

		BLOCKSIZE = SCREEN_HEIGHT / 20 # 20 blocks hoog

		from PIL import Image
		
		# Call the parent constructor
		Level.__init__(self, player)

		level = Image.open(source)
		
		*topleft, width, height = level.getbbox()

		self.level_limit = -BLOCKSIZE * width

		for py in range(height):

			# The amount of consecutive pixels with the same color (1 when we start)
			consecutive_pixels = 1

			for px in range(width):

				r, g, b, a = level.getpixel((px, py))

				# Skip transparant pixels
				if a == 0:
					consecutive_pixels = 1
					continue

				# If there is no "next pixel" or the pixel after this one is different
				if px + 1 >= width or level.getpixel((px + 1, py)) != (r, g, b, a):
					# Make a platform with a width such that it resembles all consecutive pixels
					platform = Platform(BLOCKSIZE * consecutive_pixels, BLOCKSIZE, (r, g, b))
					platform.rect.x = (px - consecutive_pixels + 1) * BLOCKSIZE # x-offset -> (px should be inital pixel) * size of 1 block
					platform.rect.y = py * BLOCKSIZE # y-offset, current y-value * size of 1 block

					# Add platform to the list that contains the other platforms
					container = self.water_list if (r, g, b) == WATER else self.platform_list
					container.add(platform)

					# Clear the amount of consecutive pixels
					consecutive_pixels = 1

				else:
					# In this case there is a next pixel, and it's the same color as the current
					# So we increment the amount of consecutive pixels by 1
					# which causes the resulting "block" or platform thingy to be widened by BLOCKSIZE
					consecutive_pixels += 1
					continue


def main():
	""" Main Program """
	pygame.init()

	# Set the height and width of the screen
	size = [SCREEN_WIDTH, SCREEN_HEIGHT]
	screen = pygame.display.set_mode(size)

	pygame.display.set_caption("Marcio")

	# Create the player
	player = Player()

	# Create all the levels
	level_list = []
	level_list.append(LevelFromImage(player, "res/level1.png"))

	# Set the current level
	current_level_no = 0
	current_level = level_list[current_level_no]

	active_sprite_list = pygame.sprite.Group()
	player.level = current_level

	player.rect.x = 5 * 30
	player.rect.y = SCREEN_HEIGHT - 5 * 30
	active_sprite_list.add(player)

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

		# If the player gets near the right side, shift the world left (-x)
		if player.rect.right >= 500:
			diff = player.rect.right - 500
			player.rect.right = 500
			current_level.shift_world(-diff)

		# If the player gets near the left side, shift the world right (+x)
		if player.rect.left <= 120:
			diff = 120 - player.rect.left
			player.rect.left = 120
			current_level.shift_world(diff)

		# If the player gets to the end of the level, go to the next level
		current_position = player.rect.x + current_level.world_shift
		if current_position < current_level.level_limit:
			player.rect.x = 120
			if current_level_no < len(level_list)-1:
				current_level_no += 1
				current_level = level_list[current_level_no]
				player.level = current_level

		# ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
		current_level.draw(screen)
		active_sprite_list.draw(screen)

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
