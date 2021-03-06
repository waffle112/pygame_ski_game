'''
Goals:
    1) make player - ALMOST DONE
        movement - left/right
        shoot - space

    2) make bullets - almost done
    3) make aliens - half done
        need to make aliens shoot bullets too
    4) make barriers?
        barriers have hp too
        also barriers show damage as well
    5) make health system
        3 pts of hp
        show at top left of screen - 3 cannons to show hp
    6) make score system
        top right of screen

    7) Game repeat
        game keeps going after all aliens are dead
        so restart game but increase speed of aliens

    8) modify code to load in images from sprite sheet
        aliens are 24px by 16px
        alien1 - 3, 225 -- 36, 225
        alien2 - 73, 225 -- 106, 225
        alien3 - 147, 226 -- 179, 226

        bonus alien - 215, 224 (48px by 21px)
        cannon - 277, 228 (26px by 16px))

        (44 by 32px)
        barrier1 - 316, 213
        barrier2 - 373, 211
        barrier3 - 428, 210
        barrier4 - 480, 210
        barrier5 - 480, 265

        explosion - 438, 276

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

#colors
black = (0, 0, 0)
white = (255, 255, 255)

#fonts
arial = pygame.font.match_font('arial')

# create variable that handles FPS (frames per sec)
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
bullet_sprites = pygame.sprite.Group()
alien_b_sprites = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()
barrier_sprites = pygame.sprite.Group()

#sprite sheet
spritesheet = pygame.image.load('space_invaders.png')
scale = 2.3

class Player(pygame.sprite.Sprite):
    def __init__(self):
        # call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        # create an image of the block and fill it with a color
        # this could also be an image loaded from the disk

        # self.image = pygame.Surface([40, 30])
        # self.image.fill(white)

        #cannon - 277, 228 (26px by 16px))
        self.image = pygame.transform.scale(spritesheet.subsurface(277, 228, 26, 16), (26*scale, 16*scale))


        # self.image = pygame.image.load("basket.png").convert()
        self.image.set_colorkey((0, 0, 0))
        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        # self.rect = self.image.get_rect(center = (x,y))
        self.rect = self.image.get_rect(center=(width / 2, height - 30))

        # initalize speed on x and y axis for sprite
        self.x_speed = 0
        self.y_speed = 0

        #initialize hp
        self.hp = 3
        self.score = 0
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

'''
aliens are 24px by 16px
        alien1 - 3, 225 -- 36, 225
        alien2 - 73, 225 -- 106, 225
        alien3 - 147, 226 -- 179, 226
'''
class Enemy(pygame.sprite.Sprite):
    def __init__(self, w, h, x, y, alien):
        # call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        # create an image of the block and fill it with a color
        # this could also be an image loaded from the disk

        # self.image = pygame.Surface([w, h])
        # self.image.fill(white)
        self.alien = alien
        if self.alien == 0:
            self.image = pygame.transform.scale(spritesheet.subsurface(3, 225, 24, 16), (24*scale, 16*scale))
        elif self.alien == 1:
            self.image = pygame.transform.scale(spritesheet.subsurface(73, 225, 24, 16), (24*scale, 16*scale))
        elif self.alien == 2:
            self.image = pygame.transform.scale(spritesheet.subsurface(147, 226, 24, 16), (24*scale, 16*scale))

        # self.image = pygame.image.load("basket.png").convert()
        self.image.set_colorkey((0, 0, 0))
        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        # self.rect = self.image.get_rect(center = (x,y))
        self.rect = self.image.get_rect(center=(x, y))

        # initalize speed on x and y axis for sprite
        self.x_speed = 60
        self.y_speed = 0

        self.internal = False

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

        if self.internal:
            if self.alien == 0:
                self.image = pygame.transform.scale(spritesheet.subsurface(3, 225, 24, 16), (24*scale, 16*scale))
            elif self.alien == 1:
                self.image = pygame.transform.scale(spritesheet.subsurface(73, 225, 24, 16), (24*scale, 16*scale))
            elif self.alien == 2:
                self.image = pygame.transform.scale(spritesheet.subsurface(147, 226, 24, 16), (24*scale, 16*scale))
        else:
            if self.alien == 0:
                self.image = pygame.transform.scale(spritesheet.subsurface(36, 225, 24, 16), (24*scale, 16*scale))
            elif self.alien == 1:
                self.image = pygame.transform.scale(spritesheet.subsurface(106, 225, 24, 16), (24*scale, 16*scale))
            elif self.alien == 2:
                self.image = pygame.transform.scale(spritesheet.subsurface(179, 226, 24, 16), (24*scale, 16*scale))
        self.internal = not self.internal

        if self.rect.bottom >= height * .8:
            game_over()
'''
        barrier1 - 316, 213
        barrier2 - 373, 211
        barrier3 - 428, 210
        barrier4 - 480, 210
        barrier5 - 480, 265
        (44 by 32px)
'''
class Barrier(pygame.sprite.Sprite):
    def __init__(self, x, y):
        # call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        # create an image of the block and fill it with a color
        # this could also be an image loaded from the disk

        # self.image = pygame.Surface([100, 80])
        # self.image.fill(white)

        self.image = pygame.transform.scale(spritesheet.subsurface(316, 213, 44, 32), (44*scale, 32*scale))

        # self.image = pygame.image.load("basket.png").convert()
        self.image.set_colorkey((0, 0, 0))
        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        # self.rect = self.image.get_rect(center = (x,y))
        self.rect = self.image.get_rect(topleft=(x, y))

        # initalize speed on x and y axis for sprite
        self.x_speed = 0
        self.y_speed = 0
        self.hp = 20


    # update method
    def update(self):
        #check if hp is below or at 0 then self.kill

        if self.hp >= 20:
            self.image = pygame.transform.scale(spritesheet.subsurface(316, 213, 44, 32), (44*scale, 32*scale))
        elif self.hp >= 20 * .8:
            self.image = pygame.transform.scale(spritesheet.subsurface(480, 210, 44, 32), (44*scale, 32*scale))
        elif self.hp >= 20 * .6:
            self.image = pygame.transform.scale(spritesheet.subsurface(373, 211, 44, 32), (44*scale, 32*scale))
        elif self.hp >= 20 * .4:
            self.image = pygame.transform.scale(spritesheet.subsurface(428, 210, 44, 32), (44*scale, 32*scale))
        else:
            self.kill()
'''
need 2 bullets 
one for the player 
and one for the enemy 

'''


class bullet1(pygame.sprite.Sprite):

    def __init__(self, x, y, up=1):
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
        self.y_speed = up * 5

    # update method
    def update(self):
        # make bullet go straight up
        self.rect.y += -self.y_speed

        # if the bullet goes out of bounds -> delete bullet
        if self.rect.bottom <= 0:
            self.kill()

class button(pygame.sprite.Sprite):

    def __init__(self, color, x, y, w, h, text=''):
        # call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        #elf.rect = self.image.get_rect()
        #self.rect.center = (x, y)
        self.clicked = False # include new variable
        self.color = color
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.text = text

    def draw(self, outlineColor=None):
        if outlineColor:
            pygame.draw.rect(screen, outlineColor, (self.x - 2, self.y - 2, self.width + 4, self.height + 4))

        # if you have pics instead of buttons -> load an image instead of drawing a rect
        #screen.blit(self.image, (self.rect.x, self.rect.y))
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

        if self.text != '':
            font = pygame.font.Font(arial, 18)
            text_surface = font.render(self.text, True, white)
            screen.blit(text_surface, (self.x + (self.width / 2 - text_surface.get_width() / 2),
                                       self.y + (self.height / 2 - text_surface.get_height() / 2)))
        pressed = False
        pos = pygame.mouse.get_pos()
        if self.x < pos[0] < self.x + self.width and self.y < pos[1] < self.y + self.height:
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                pressed = True
        return pressed

def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(arial, size)
    text_surface = font.render(text, True, white)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

#lives function
def show_lives(hp):
    #draw "lives:" + 3 cannons/rects
    #essnetially, draw/blip rectangles/images onto the game, but because these have no interaction, theres no need to
    #use update
    draw_text(screen, "Lives: ", 40, width/15, height/40)
    image = pygame.Surface([40, 30])
    image.fill(white)
    image_rect = image.get_rect()
    image_rect.x = width/8
    image_rect.y = height/25
    for i in range(hp):
        screen.blit(image, image_rect)
        image_rect.x += 50

    pass

#score function
def show_score(score):
    #draw "score: " + score
    score = "Score: " + str(score)
    draw_text(screen, score, 40, width * 4/5, height/40)
    pass

#check which aliens are the farthest aliens on the left side and right side and return them
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

    #print(left.rect.x, right.rect.x)
    return left, right

def game_over():
    print("Game Over")

    #create two buttons color, x, y, width, height, text=''
    buttonQuit = button(black, width/2-50, height/4 + 60, 100, 50, "Quit Game")
    buttonRestart = button(black, width/2-50, height/4 , 100, 50, "Restart Game")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()


        screen.fill(black)
        if buttonRestart.draw(white):
            #seems like sprites arent deleted yet
            all_sprites.empty()
            enemy_sprites.empty()
            bullet_sprites.empty()
            alien_b_sprites.empty()
            barrier_sprites.empty()
            game()

        if buttonQuit.draw(white):
            sys.exit()

        pygame.display.flip()

def start_game():
    print("Game Start")

    #create two buttons color, x, y, width, height, text=''
    buttonQuit = button(black, width/2-50, height/4+ 60, 100, 50, "Quit Game")
    buttonStart = button(black, width/2-50, height/4, 100, 50, "Start Game")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

        screen.fill(black)
        if buttonStart.draw(white):
            break

        if buttonQuit.draw(white):
            sys.exit()

        pygame.display.flip()

def game(win=None, hp = None, newspeed = None):
    if win is not None:
        player = Player()
        player.score = win
        player.hp = hp
        speed = newspeed
    else:
        start_game()
        player = Player()
        speed = 2000

    all_sprites.add(player)
    alien = 0
    for y in range(1, 6):
        for x in range(1, 11):
            e = Enemy(40, 40, 175 + x * 60, 50 + y * 60, y//2)
            enemy_sprites.add(e)
            #all_sprites.add(e)


    leftmost, rightmost = alienSideCheck()

    for i in range(4):
        b = Barrier(75 + width * (i / 4), height * .8)
        barrier_sprites.add(b)
        all_sprites.add(b)

    # create a timed event that tells the enemies to move
    pygame.time.set_timer(pygame.USEREVENT + 1, 1000)

    #create a timed event that tells a random enemy to fire
    pygame.time.set_timer(pygame.USEREVENT + 3, 800)

    firing_delay = False

    win = 0

    while True:
        clock.tick(60)  # set FPS to 60 FPS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not firing_delay:
                    # shoot a bullet from the player
                    # spawn a bullet whose x and y == player_rect
                    b = bullet1(player.rect.centerx, player.rect.centery)
                    bullet_sprites.add(b)
                    all_sprites.add(b)
                    firing_delay = True
                    pygame.time.set_timer(pygame.USEREVENT + 2, 200)

            if event.type == pygame.USEREVENT + 1:
                # move the enemies
                enemy_sprites.update()
                if rightmost.rect.right >= width:
                    enemy_sprites.update("left")
                if leftmost.rect.left <= 0:
                    enemy_sprites.update("right")
                pygame.time.set_timer(pygame.USEREVENT + 1, speed)

            if event.type == pygame.USEREVENT + 2:
                firing_delay = False

            if event.type == pygame.USEREVENT + 3:
                #enemy shoots something
                alien = random.choice(enemy_sprites.sprites())
                b = bullet1(alien.rect.centerx, alien.rect.centery, -1)
                alien_b_sprites.add(b)
                all_sprites.add(b)
                pygame.time.set_timer(pygame.USEREVENT + 3, 800)
                pass

        all_sprites.update()

        # check if bullet in spritegroup collide with enemy_sprites
        # the true, true is saying delete both bullet and enemy
        #also check if bullets collided with barrier,
        hits = pygame.sprite.groupcollide(barrier_sprites, bullet_sprites, False, True)
        for h in hits:
            h.hp -= 1
        hits = pygame.sprite.groupcollide(barrier_sprites, alien_b_sprites, False, True)
        for h in hits:
            print("barier hit")
            h.hp -= 1

        hits = pygame.sprite.groupcollide(barrier_sprites, bullet_sprites, False, True)
        for h in hits:
            print("barrier hit")
            h.hp -= 1

        hits = pygame.sprite.groupcollide(bullet_sprites, enemy_sprites, True, True)
        if hits:
            leftmost, rightmost = alienSideCheck()
            player.score += 100

        hits = pygame.sprite.spritecollide(player, alien_b_sprites, True)
        for h in hits:
            print("player hit ")
            player.hp -= 1


        # if the alien on the side touches the edge of the game window
        # flip the speed by making it negative
        # if it touches the left side
        # move down
        screen.fill(black)
        all_sprites.draw(screen)
        enemy_sprites.draw(screen)

        show_lives(player.hp)
        show_score(player.score)
        pygame.display.flip()



        #check if game over
        if player.hp <= 0:
            win = None
            break
        if not enemy_sprites:
            #respawn all the enemies and increase hp by 1
            win = player.score
            player.hp += 1
            break

    if win is not None:
        player.kill()
        for b in barrier_sprites:
            b.kill()
        game(win, player.hp, int(speed*.95))
    else:
        game_over()

if __name__ == "__main__":
    game()
