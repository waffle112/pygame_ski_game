import sys
import pygame
import random

# initialize pygame and "boot" it up
pygame.init()

# create game window size
size = width, height = 1000, 800
screen = pygame.display.set_mode(size)

# create variable that handles FPS (frames per sec)
clock = pygame.time.Clock()

#create speed and direction
global_direction = 0
global_speed = 0
global_reset = 5

#colors
black = (0, 0, 0)
white = (255, 255, 255)
snow = (220, 220, 220)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)

# sprite groups
all_sprites = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()

class player(pygame.sprite.Sprite):
    # make variables to describe what player can do
    def __init__(self):  # constructor or initialize()
        # call the parent class constrcutor
        pygame.sprite.Sprite.__init__(self)

        self.speed = 5
        self.hp = 3
        self.boosts = 3
        # create the player rectangle
        self.image = pygame.Surface([30, 30])
        self.image.fill(white)
        # self.image = pygame.image.load("basket.png").convert()
        # self.image.set_colorkey((0, 0, 0))
        # get a rectangle hitbox based on the the player image
        self.rect = self.image.get_rect(center=(width / 2, height / 2))

    # update function
    def update(self):
        #self.handleMovement()
        pass

    # make methods to have player do somehting
    # movement
    def handleMovement(self):
        # if a particular keyboard button has been pressed -> do something
        global global_speed
        global global_direction
        # get keystate
        keystate = pygame.key.get_pressed()

        # check if keystate is of a particular button
        # modify what happens to change how the player moves
        if keystate[pygame.K_a]:  # if A was pressed - go downward left x_speed = -speed AND y_speed = speed
            self.image.fill(red)
            # make everything go up left?
            global_direction = 1
        if keystate[pygame.K_d]:  # if D was pressed
            self.image.fill(blue)
            # make everything go up right?
            global_direction = -1
        if keystate[pygame.K_w]:  # if W was pressed
            self.image.fill(black)
            # make everything stop?
            global_speed = 0
            global_direction = 0
        if keystate[pygame.K_s]:  # if S was pressed
            self.image.fill(green)
            # make everything go straight up?
            global_speed = self.speed
            global_direction = 0

        if keystate[pygame.K_SPACE]:
            print("always activating?")
            self.handleBoost()

    # if player clicks on boost button -> go fast
    def handleBoost(self):
        # if a particular keyboard button OR A MOUSE CLICK has been pressed -> do something
        global global_speed
        if self.boosts > 0:
            self.speed = 10
            global_speed = self.speed
            self.boosts -= 1
            #timer event that will return speed back to normal
            pygame.time.set_timer(pygame.USEREVENT+1, 5000, loops=0)
        else:
            print("no more boosts left!")