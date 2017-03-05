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

# Danku https://nebelprog.wordpress.com/2013/08/14/create-a-simple-game-menu-with-pygame-pt-1-writing-the-menu-options-to-the-screen/

class GameMenu():
	def __init__(self, screen, items, bg_color=(0,0,0), font_size=30,
					font_color=(255, 255, 255)):
		self.screen = screen
		self.scr_width = self.screen.get_rect().width
		self.scr_height = self.screen.get_rect().height
 
		self.bg_color = bg_color
		self.clock = pygame.time.Clock()
 
		self.items = items
		self.font = pygame.font.SysFont(constants.FONT_NAME, font_size)
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
		while mainloop:
			# Limit frame speed to 50 FPS
			self.clock.tick(50)
 
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					mainloop = False
 
			# Redraw the background
			self.screen.fill(self.bg_color)
 
			for name, label, (width, height), (posx, posy) in self.items:
				self.screen.blit(label, (posx, posy))
 
			pygame.display.flip()
