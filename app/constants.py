# Global constants

import pygame

pygame.font.init()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

FONT = 'Consolas'

BACKGROUND = (128, 128, 255)

OBJECTIVE = PICKUP = (228, 4, 40)
WATER = (0, 182, 233)
LAVA = (241, 95, 34)

OBJECTIVE_HELPER = (195, 195, 80)

LIVES = 10

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_CENTER = SCREEN_WIDTH / 2
SCREEN_HEIGHT = 600

BLOCKSIZE = SCREEN_HEIGHT / 20 # 20 blocks hoog

# In het verslag hadden we gezegd dat een kogel 3x de breedte van de speler ging
# Dit is pittig weinig.
# Daarom hier BULLET_DISTANCE, zodat we de maximale afstand kunnen veranderen
BULLET_DISTANCE = SCREEN_CENTER # zodat je niet verder kan schieten dan dat je kan zien.
# we kunnen bullet distance ook groter maken, zodat marc lekker gaat ragen lol

# Zorg dat bullet velocity NOOIT groter wordt dan 1 block/frame.
# Dit kan ervoor zorgen dat hij door dingen heen gaat.
# 1 block/frame = BLOCKSIZE * 60 / 60
BULLET_VELOCITY = BLOCKSIZE * 30 / 60 # 30 blocks/sec

# Let op dat je niet te veel ruimte gebruikt.. text is groot.
# Maak desnoods de fontsize kleiner in hud.py
INSTRUCTIONS = [
	'Move: A, D or arrow keys',
	'Jump: W, space or arrow up',
	'Shoot: Ctrl',
	'Pick up all the code in the correct order',
	'and go to the end of the level.',
	'You can kill the bad code by shooting at it',
	'',
	'Press any key to start...',
]
