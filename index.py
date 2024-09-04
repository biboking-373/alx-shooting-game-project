import pygame
from pygame.locals import *
import sys

# Initialize Pygame
pygame.init()

# Define colors and constants
WHITE = (255, 255, 255)
RED = pygame.Color(255, 0, 0)
GREEN = pygame.Color(0, 255, 0)
BLUE = pygame.Color(0, 0, 255)
FPS = 45
fpslimit = pygame.time.Clock()

# Screen dimensions
sclength = 650
scwidth = 1200
screen = pygame.display.set_mode((scwidth, sclength))

# Game running state
isrunning = True

# Define the Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("spaceship.png")
        self.rect = self.image.get_rect()
        self.rect.center = (scwidth // 2, sclength - 50)  # Position the player at the bottom center of the screen

# Instantiate player one
player_one = Player()

# Create a sprite group and add player one to the group
all_sprites = pygame.sprite.Group()
all_sprites.add(player_one)

# Game loop
while isrunning:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Clear the screen
    screen.fill(WHITE)

    # Draw all sprites
    all_sprites.draw(screen)

    # Update the display
    pygame.display.update()

    # Cap the frame rate
    fpslimit.tick(FPS)
