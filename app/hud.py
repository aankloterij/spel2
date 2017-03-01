import pygame
import constants

class HUD:

	def __init__(self, player):
		self.player = player
		self.heart_image = pygame.image.load('res/heart.png').convert_alpha()
		self.heart_width, self.heart_height = self.heart_image.get_rect().size

		self.padding = 15
		self.xleft = self.padding
		self.ybottom = constants.SCREEN_HEIGHT - self.heart_height - self.padding

	def draw(self, surface):
		# draw

		for i in range(self.player.lives):
			x = self.xleft + (self.heart_width + self.padding) * i
			y = self.ybottom

			surface.blit(self.heart_image, (x, y))

