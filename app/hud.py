import pygame
import constants

class HUD:

	def __init__(self, p):
		self.p = p
		self.heart_image = pygame.image.load('res/heart.png').convert_alpha()
		self.heart_image = pygame.transform.scale(self.heart_image, (32, 32))

		self.heart_width, self.heart_height = self.heart_image.get_rect().size

		self.font = pygame.font.Font('res/Pixeled.ttf', 24)

		self.padding = 15
		self.xleft = self.padding
		self.ybottom = constants.SCREEN_HEIGHT - self.heart_height - self.padding

	def draw(self, surface, text=None):

		if text != None:
			text_surface = self.font.render(str(text), False, constants.BLACK)
			surface.blit(text_surface, (self.padding, self.padding))

		for i in range(self.p.lives):
			x = self.xleft + (self.heart_width + self.padding) * i
			y = self.ybottom

			surface.blit(self.heart_image, (x, y))
