import pygame
import constants
from constants import BLOCKSIZE, FONT_NAME
from player import Entity

class Objective(Entity):
	
	def __init__(self, x, y):
		super().__init__()
		self.image = pygame.image.load("res/code.png").convert_alpha()

		self.rect = pygame.Rect(x, y, BLOCKSIZE, BLOCKSIZE)

		self.text = pygame.font.SysFont(FONT_NAME, 16).render("<html>", 1, constants.RED)




class ObjectiveList(pygame.sprite.Group):

	def draw(self, surface):

		"""draw all sprites onto the surface
		Group.draw(surface): return None
		Draws all of the member sprites onto the given surface.
		"""

		# Lekker van de source gejat: https://bitbucket.org/pygame/pygame/src/407caa445ee033bfbcf5e9cc5c3961c0aa9db8f4/lib/sprite.py?at=default&fileviewer=file-view-default#sprite.py-464
		sprites = self.sprites()
		surface_blit = surface.blit
		for spr in sprites:
			self.spritedict[spr] = surface_blit(spr.image, spr.rect)

			# render de tekst boven de objectives
			x = spr.rect.centerx - spr.text.get_width() / 2 # in het midden van het objective
			y = spr.rect.y - spr.text.get_height() - 5 # 5 px boven objective
			surface_blit(spr.text, (x, y))

		self.lostsprites = []
