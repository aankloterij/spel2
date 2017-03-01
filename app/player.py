import pygame

import constants

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

		# Amount of lives
		self.lives = 3

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
		if self.rect.y >= constants.SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
			self.change_y = 0
			self.rect.y = constants.SCREEN_HEIGHT - self.rect.height

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
		if len(platform_hit_list) > 0 or self.rect.bottom >= constants.SCREEN_HEIGHT or self.is_in_water:
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
