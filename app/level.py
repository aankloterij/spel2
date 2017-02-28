import pygame

import constants

class Platform(pygame.sprite.Sprite):
	""" Platform the user can jump on """

	def __init__(self, width, height, color=constants.GREEN):
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
		screen.fill(constants.BLUE)

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

		BLOCKSIZE = constants.SCREEN_HEIGHT / 20 # 20 blocks hoog

		from PIL import Image

		# Call the parent constructor
		Level.__init__(self, player)

		level = Image.open(source)

		*__, width, height = level.getbbox()

		self.level_limit = -BLOCKSIZE * width

		for py in range(height):

			# The amount of consecutive pixels with the same color (1 when we start)
			consecutive_pixels = 1

			for px in range(width):

				r, g, b, a = level.getpixel((px, py))

				# Skip transparant pixels
				if a == 0:
					continue

				# If there is no "next pixel" or the pixel after this one is different
				if px + 1 >= width or level.getpixel((px + 1, py)) != (r, g, b, a):
					# Make a platform with a width such that it resembles all consecutive pixels
					platform = Platform(BLOCKSIZE * consecutive_pixels, BLOCKSIZE, (r, g, b))
					platform.rect.x = (px - consecutive_pixels + 1) * BLOCKSIZE # x-offset -> (px should be inital pixel) * size of 1 block
					platform.rect.y = py * BLOCKSIZE # y-offset, current y-value * size of 1 block

					# Add platform to the list that contains the other platforms
					container = self.water_list if (r, g, b) == constants.WATER else self.platform_list
					container.add(platform)

					# Clear the amount of consecutive pixels
					consecutive_pixels = 1

				else:
					# In this case there is a next pixel, and it's the same color as the current
					# So we increment the amount of consecutive pixels by 1
					# which causes the resulting "block" or platform thingy to be widened by BLOCKSIZE
					consecutive_pixels += 1
					continue
