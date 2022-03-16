'''
Goals:
    1) make player
        movement - left/right
        shoot - space

    2) make bullets
    3) make aliens
    4) make barriers?

probably make a player class
then a bullet class
then code it so that the player can shoot bullet

'''

import sys, pygame
import random

# initialize pygame and "boot" it up
pygame.init()

# create game window size
size = width, height = 1000, 800
screen = pygame.display.set_mode(size)

black = (0, 0, 0)
white = (255, 255, 255)

# create variable that handles FPS (frames per sec)
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
bullet_sprites = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()
barrier_sprites = pygame.sprite.Group()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        # call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        # create an image of the block and fill it with a color
        # this could also be an image loaded from the disk
        self.image = pygame.Surface([40, 30])
        self.image.fill(white)
        # self.image = pygame.image.load("basket.png").convert()
        self.image.set_colorkey((0, 0, 0))
        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        # self.rect = self.image.get_rect(center = (x,y))
        self.rect = self.image.get_rect(center=(width / 2, height - 30))

        # initalize speed on x and y axis for sprite
        self.x_speed = 0
        self.y_speed = 0

    # update method
    def update(self):
        # have to set these values to 0 otherwise sprite
        # will fly off the screen
        self.x_speed = 0
        self.y_speed = 0
        # Option 1
        """ if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.y_speed -= 7
                elif event.key == pygame.K_DOWN:
                    self.y_speed += 7
                elif event.key == pygame.K_LEFT:
                    self.x_speed -= 7
                elif event.key == pygame.K_RIGHT:
                    self.x_speed += 7 """
        # Option 2
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_a]:
            self.x_speed -= 7
        elif keystate[pygame.K_d]:
            self.x_speed += 7

        self.rect.x += self.x_speed

        # Keep player inside screen bounds
        if self.rect.right >= width:
            self.rect.right = width
        if self.rect.left <= 0:
            self.rect.left = 0


class Enemy(pygame.sprite.Sprite):
    def __init__(self, w, h, x, y):
        # call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        # create an image of the block and fill it with a color
        # this could also be an image loaded from the disk
        self.image = pygame.Surface([w, h])
        self.image.fill(white)
        # self.image = pygame.image.load("basket.png").convert()
        self.image.set_colorkey((0, 0, 0))
        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        # self.rect = self.image.get_rect(center = (x,y))
        self.rect = self.image.get_rect(center=(x, y))

        # initalize speed on x and y axis for sprite
        self.x_speed = 60
        self.y_speed = 0

    def handle_movement(self):
        self.rect.x += self.x_speed

    def left(self):
        self.x_speed = -self.x_speed
        self.rect.x -= 60

    def right(self):
        self.x_speed = -self.x_speed
        self.rect.x += 60
        self.rect.y += 60

    # update method
    def update(self, swap = None):
        # have to set these values to 0 otherwise sprite
        # will fly off the screen
        if swap == "left":
            self.left()
        elif swap == "right":
            self.right()
        else:
            self.handle_movement()

class Barrier(pygame.sprite.Sprite):
    def __init__(self, x, y):
        # call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        # create an image of the block and fill it with a color
        # this could also be an image loaded from the disk
        self.image = pygame.Surface([100, 80])
        self.image.fill(white)
        # self.image = pygame.image.load("basket.png").convert()
        self.image.set_colorkey((0, 0, 0))
        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        # self.rect = self.image.get_rect(center = (x,y))
        self.rect = self.image.get_rect(topleft=(x, y))

        # initalize speed on x and y axis for sprite
        self.x_speed = 0
        self.y_speed = 0

    # update method
    def update(self):
        # have to set these values to 0 otherwise sprite
        # will fly off the screen
        self.x_speed = 0
        self.y_speed = 0


'''
need 2 bullets
one for the player 
and one for the enemy 

'''


class bullet1(pygame.sprite.Sprite):

    def __init__(self, x, y):
        # call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        # create an image of the block and fill it with a color
        # this could also be an image loaded from the disk
        self.image = pygame.Surface([5, 10])
        self.image.fill(white)

        # self.image = pygame.image.load("basket.png").convert()
        self.image.set_colorkey((0, 0, 0))

        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        # self.rect = self.image.get_rect(center = (x,y))
        self.rect = self.image.get_rect(center=(x, y))

        # initalize speed on x and y axis for sprite
        self.y_speed = 5

    # update method
    def update(self):
        # make bullet go straight up
        self.rect.y += -self.y_speed

        # if the bullet goes out of bounds -> delete bullet
        if self.rect.bottom <= 0:
            self.kill()


def alienSideCheck():
    left = None
    right = None
    for e in enemy_sprites:
        if left is None and right is None:
            left = e
            right = e
        if e.rect.x < left.rect.x:
            left = e
        if e.rect.x > right.rect.x:
            right = e

    print(left.rect.x, right.rect.x)
    return left, right


def game():
    player = Player()
    all_sprites.add(player)
    for y in range(1, 6):
        for x in range(1, 11):
            e = Enemy(40, 40, 175 + x * 60, 50 + y * 60)
            enemy_sprites.add(e)
            #all_sprites.add(e)

    leftmost, rightmost = alienSideCheck()

    for i in range(4):
        b = Barrier(75 + width * (i / 4), height * .8)
        barrier_sprites.add(b)
        all_sprites.add(b)

    # create a timed event that tells the enemies to move
    pygame.time.set_timer(pygame.USEREVENT + 1, 1000)

    while True:
        clock.tick(60)  # set FPS to 60 FPS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # shoot a bullet from the player
                    # spawn a bullet whose x and y == player_rect
                    b = bullet1(player.rect.centerx, player.rect.centery)
                    bullet_sprites.add(b)
                    all_sprites.add(b)

            if event.type == pygame.USEREVENT + 1:
                # move the enemies
                enemy_sprites.update()
                if rightmost.rect.right >= width:
                    enemy_sprites.update("left")
                if leftmost.rect.left <= 0:
                    enemy_sprites.update("right")
                pygame.time.set_timer(pygame.USEREVENT + 1, 2000)

        all_sprites.update()

        # check if bullet in spritegroup collide with enemy_sprites
        # the true, true is saying delete both bullet and enemy
        hits = pygame.sprite.groupcollide(bullet_sprites, enemy_sprites, True, True)
        if hits:
            leftmost, rightmost = alienSideCheck()



        # if the alien on the side touches the edge of the game window
        # flip the speed by making it negative
        # if it touches the left side
        # move down
        screen.fill(black)
        all_sprites.draw(screen)
        enemy_sprites.draw(screen)
        pygame.display.flip()


if __name__ == "__main__":
    game()
