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

LIVES = 5

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_CENTER = SCREEN_WIDTH / 2
SCREEN_HEIGHT = 600

BLOCKSIZE = SCREEN_HEIGHT / 20 # 20 blocks hoog

# In het verslag hadden we gezegd dat een kogel 3x de breedte van de speler ging
# Dit is pittig weinig.
# Daarom hier BULLET_DISTANCE, zodat we de maximale afstand kunnen veranderen
BULLET_DISTANCE = BLOCKSIZE * 20

# Zorg dat bullet velocity NOOIT groter wordt dan 1 block/frame.
# Dit kan ervoor zorgen dat hij door dingen heen gaat.
# 1 block/frame = BLOCKSIZE * 60 / 60
BULLET_VELOCITY = BLOCKSIZE * 30 / 60 # 30 blocks/sec
