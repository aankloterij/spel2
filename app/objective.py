import pygame
import constants
import random
from constants import BLOCKSIZE
from player import Entity

class Objective(Entity):

	def __init__(self, x, y):
		super().__init__()
		self.image = pygame.image.load("res/code.png").convert_alpha()
		self.rect = pygame.Rect(x, y, BLOCKSIZE, BLOCKSIZE)
		self.font = pygame.font.SysFont('Consolas', 16)
		self.text = None # Dit wordt later ingesteld

	def set_snippet(self, order, text):
		self.order = order
		self.text = self.font.render(text, 1, constants.OBJECTIVE_HELPER)

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

	def populate_objectives(self, snippets):
		objectives = self.sprites()

		if len(objectives) != len(snippets):
			exit("Error: te veel/weinig objectives voor het level")

		for objective in objectives:
			index, snippet = random.choice(list(snippets.items()))

			objective.set_snippet(index, snippet)
