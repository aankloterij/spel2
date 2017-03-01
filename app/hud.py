import pygame
import constants

class HUD:

	def __init__(self, p):
		self.p = p
		self.heart_image = pygame.image.load('res/heart.png').convert_alpha()
		self.heart_width, self.heart_height = self.heart_image.get_rect().size

		self.font = pygame.font.SysFont(constants.FONT_NAME, 30)

		self.padding = 15
		self.xleft = self.padding
		self.ybottom = constants.SCREEN_HEIGHT - self.heart_height - self.padding

	def draw(self, surface):

		x = y = 0

		for i in range(self.p.lives):
			x = self.xleft + (self.heart_width + self.padding) * i
			y = self.ybottom

			surface.blit(self.heart_image, (x, y))

		text_surface = self.font.render(str(self.p.lives), False, (0, 0, 0))

		surface.blit(text_surface, (x + self.padding + self.heart_width, y - 8))
