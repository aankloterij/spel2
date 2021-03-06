import pygame
import constants

class HUD:

	def __init__(self, p):
		self.p = p
		self.heart_image = pygame.image.load('res/heart.png').convert_alpha()
		self.heart_image = pygame.transform.scale(self.heart_image, (32, 32))

		self.heart_width, self.heart_height = self.heart_image.get_rect().size

		self.font = pygame.font.SysFont(constants.FONT, 32)
		self.nicefont = pygame.font.Font('res/Pixeled.ttf', 16)

		self.padding = 15
		self.xleft = self.padding
		self.ybottom = constants.SCREEN_HEIGHT - self.heart_height - self.padding
		self.show_controls = True

		self.instruction_lines = []

		# Dialog aan het begin van het spel, met control uitleg
		for line in constants.INSTRUCTIONS:
			self.instruction_lines.append(self.nicefont.render(line, False, constants.RED))


	def draw(self, surface, text=None, font=False):

		if font:
			_font = pygame.font.Font('res/Pixeled.ttf', 16)
		else:
			_font = pygame.font.SysFont('Courier New', 32)

		if text != None:
			text = _font.render(str(text), False, constants.WHITE)
			surface.blit(text, (self.padding, self.padding))

		for i in range(self.p.lives):
			x = self.xleft + (self.heart_width + self.padding) * i
			y = self.ybottom

			surface.blit(self.heart_image, (x, y))

		if self.show_controls:
			y = 100 # 100 px van bovenkant scherm

			for line in self.instruction_lines:
				x = constants.SCREEN_WIDTH / 2 - line.get_width() / 2
				surface.blit(line, (x, y))
				y += line.get_height() + self.padding


# Danku https://nebelprog.wordpress.com/2013/08/14/create-a-simple-game-menu-with-pygame-pt-1-writing-the-menu-options-to-the-screen/

class GameMenu():
	def __init__(self, screen, items, bg_color=(0,0,0), font_size=30, font_color=(255, 255, 255)):
		self.screen = screen
		self.scr_width = self.screen.get_rect().width
		self.scr_height = self.screen.get_rect().height

		self.bg_color = bg_color
		self.clock = pygame.time.Clock()

		self.items = items
		self.font = pygame.font.Font('res/Pixeled.ttf', font_size)
		self.font_color = font_color

		self.items = []
		for index, item in enumerate(items):
			label = self.font.render(item, 1, font_color)

			width = label.get_rect().width
			height = label.get_rect().height

			posx = (self.scr_width / 2) - (width / 2)

			# t_h: total height of text block
			t_h = len(items) * height
			posy = (self.scr_height / 2) - (t_h / 2) + (index * height)

			self.items.append([item, label, (width, height), (posx, posy)])

	def run(self):
		mainloop = True

		self.sprites = []

		while mainloop:
			# Limit frame speed to 50 FPS
			# No fuck that, 60fps
			self.clock.tick(60)

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					mainloop = False

				# Exit the menu when escape is pressed
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						mainloop = False

				if event.type == pygame.MOUSEBUTTONDOWN:
					pos = pygame.mouse.get_pos()

					clicked_sprites = [s for s in self.sprites if s.collidepoint(pos)]

					# If the user clicked any sprites at all
					if len(clicked_sprites) > 0:
						# ('RESUME', 'EXIT', 'RESTART')

						# The user clicked resume, go back to the game
						if self.sprites.index(clicked_sprites[0]) == 0:
							mainloop = False

						# The user clicked exit, so exit the program
						elif self.sprites.index(clicked_sprites[0]) == 1:
							exit(0)

						elif self.sprites.index(clicked_sprites[0]) == 2:
							# TODO psutil not found
								import os, sys

								os.execl(sys.executable, sys.executable, *sys.argv)

			self.sprites = []

			# Redraw the background
			self.screen.fill(self.bg_color)

			for name, label, (width, height), (posx, posy) in self.items:
				self.sprites.append(self.screen.blit(label, (posx, posy)))

			pygame.display.flip()

class Dialog:
	def __init__(self):
		self.screen = pygame.display.get_surface()
		self.width = self.screen.get_rect().width
		self.height = self.screen.get_rect().height

		self.margin = 100 # ruimte tussen de rand van het scherm en dialog
		self.clock = pygame.time.Clock()

		self.dialogloop = False
		self.texts = []

		self.background_color = constants.RED

		self.image = pygame.Surface([constants.SCREEN_WIDTH - 2 * self.margin, constants.SCREEN_HEIGHT - 2 * self.margin])
		# self.image = pygame.image.load("res/jan.gif").convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.x = self.rect.y = self.margin
		self.image.fill(self.background_color)

	def show(self):

		self.dialogloop = True

		while self.dialogloop:
			self.clock.tick(60)

			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					self.onkeydown(self, event)

			self.render()
			pygame.display.flip()

	@staticmethod
	def onkeydown(dialog, event):
		if event.key == pygame.K_ESCAPE:
			dialog.close()


	def close(self):
		self.dialogloop = False

	def render(self):
		self.image.fill(constants.BLACK)
		self.screen.blit(self.image, self.rect)

		x = y = self.margin + 15

		for text in self.texts:
			self.screen.blit(text, (x, y))
			y += text.get_height() + 15

	def set_text(self, lines):

		font = pygame.font.Font('res/Pixeled.ttf', 16)

		for line in lines:
			self.texts.append(font.render(line, False, constants.RED))
