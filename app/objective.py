import pygame
from constants import BLOCKSIZE

class Objective(pygame.sprite.Sprite):

	def __init__(self, x, y):
		super().__init__()
		self.image = pygame.image.load("res/code.png").convert_alpha()

		self.rect = pygame.Rect(x, y, BLOCKSIZE, BLOCKSIZE)

class ObjectiveList(pygame.sprite.Group):
	pass
