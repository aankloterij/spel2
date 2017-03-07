import pygame

import constants

class Entity(pygame.sprite.Sprite):
	"""
	This class represents a movable object in the game.
	"""
	def __init__(self):
		super().__init__()


class Bullet(Entity):

	def __init__(self, velocity, coords):
		# Call the parent's constructor
		super().__init__()

		width = height = constants.BLOCKSIZE
		self.image = pygame.image.load('res/bullet.png').convert_alpha()
		# self.image = pygame.Surface([width, height])
		# self.image.fill(constants.BLACK)

		self.rect = self.image.get_rect() # get rekt lol
		self.rect.x, self.rect.y = coords

		self.velocity = velocity
		self.distance_traveled = 0

		if self.velocity < 0:
			self.image = pygame.transform.flip(self.image, True, False)

	def update(self, level):
		""" Move the bullet """
		self.distance_traveled += abs(self.velocity)
		self.rect.x += self.velocity

		if len(pygame.sprite.spritecollide(self, level.platform_list, False)) > 0:
			self.kill()
			return

		objectives_hit = pygame.sprite.spritecollide(self, level.objective_list, False)

		if len(objectives_hit) > 0:
			if isinstance(objectives_hit[0].index, int):

				from hud import Dialog

				gg = Dialog()
				gg.set_text(['Game over!!', '', 'Press any key to quit'])
				gg.onkeydown = lambda dialog, event: exit(1)

				level.player.die() or gg.show()
				self.kill()
				return

			else:
				# Een niet bs-code geraakt.
				# Laten we bs-code een niet-integer index geven.
				objectives_hit[0].kill()

				# Marc wil een extra leven erbij als je code wegschiet
				level.player.lives += 1

				self.kill()
				return

		if self.distance_traveled > constants.BULLET_DISTANCE:
			self.kill()
			return




class Player(Entity):
	"""
	This class represents the player that can be controlled.
	"""

	# -- Methods
	def __init__(self):
		""" Constructor function """

		# Call the parent's constructor
		super().__init__()

		self.image = pygame.image.load('res/player.png').convert_alpha()

		# Force schale the image to 1x2 blocks
		self.image = pygame.transform.scale(self.image, (30, 34))

		# Set a referance to the image rect.
		self.rect = self.image.get_rect()

		# Set speed vector of player
		self.change_x = 0
		self.change_y = 0

		# Used to determine the direction the player should be facing
		self.last_change_x = 0

		# List of sprites we can bump against
		self.level = None

		# Amount of lives
		self.lives = constants.LIVES

		# Next objective
		self.next_objective = 0

		# Lava warning
		self.has_seen_lava_warning = False

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

		# See if we move out of the map
		if self.rect.left < 0:
			self.rect.left = 0

		if self.rect.right > self.level.level_limit:
			self.rect.right = self.level.level_limit

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

		if not self.has_seen_lava_warning: self.check_lava_warning()

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

	def get_touching_objectives(self):
		return pygame.sprite.spritecollide(self, self.level.objective_list, False)

	def in_lava(self):
		return len(pygame.sprite.spritecollide(self, self.level.lava_list, False)) > 0

	def in_water(self):
		return len(pygame.sprite.spritecollide(self, self.level.water_list, False)) > 0

	def hits_end(self):
		return len(pygame.sprite.spritecollide(self, self.level.end_list, False)) > 0

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
		self.change_x = self.last_change_x = -6

	def go_right(self):
		""" Called when the user hits the right arrow. """
		self.change_x = self.last_change_x = 6

	def stop(self):
		""" Called when the user lets off the keyboard. """
		self.change_x = 0

	def die(self):
		self.level.shift_world(-self.level.world_shift)

		# Haal alle kogels weg
		self.level.bullet_list.empty()

		# Teleport the player back to the starting position
		# TODO Teleporting like this doesn't really work
		self.rect.x = 5 * 30
		self.rect.y = constants.SCREEN_HEIGHT - 5 * 30

		# Reduce the amount of lives by one
		self.lives -= 1

		# If the player has 0 hearts left,
		# exit with a message in the console
		if self.lives == 0:
			print("Game over, RIP")
			return False

		return True

	def shoot(self):

		from constants import BULLET_VELOCITY as bv

		# Spawn a bullet at the player
		bullet = Bullet(-bv if self.last_change_x < 0 else bv, (self.rect.x, self.rect.y))

		# Let the bullet appear in the level
		self.level.bullet_list.add(bullet)

	def can_finish_level(self):
		return self.next_objective > self.level.objective_list.highest


	def check_lava_warning(self):

		if self.level.lava_x == None:
			print('level heeft geen lava')
			self.has_seen_lava_warning = True
			return

		if self.rect.x >= self.level.lava_x - constants.LAVA_WARNING_DISTANCE:

			print('show info')

			from hud import Dialog
			dialog = Dialog()
			dialog.set_text(constants.LAVA_WARNING)
			dialog.onkeydown = lambda dialog, event: event.key != pygame.K_RETURN or dialog.close()
			dialog.show()

			self.has_seen_lava_warning = True
