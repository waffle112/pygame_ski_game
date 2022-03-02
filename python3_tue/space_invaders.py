import sys, pygame
import random

# initialize pygame and "boot" it up
pygame.init()

# create game window size
size = width, height = 1000, 800
screen = pygame.display.set_mode(size)

# create variable that handles FPS (frames per sec)
clock = pygame.time.Clock()
