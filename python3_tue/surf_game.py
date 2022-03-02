import sys, pygame
import random

# initialize pygame and "boot" it up
pygame.init()

# create game window size
size = width, height = 1000, 800
screen = pygame.display.set_mode(size)

# create variable that handles FPS (frames per sec)
clock = pygame.time.Clock()

# create some base rgb colors
black = (0, 0, 0)
white = (255, 255, 255)
snow = (220, 220, 220)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)

# sprite groups
all_sprites = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()
slow_sprites = pygame.sprite.Group()
power_sprites = pygame.sprite.Group()
misc_sprites = pygame.sprite.Group()

global_direction = 0
global_speed = 0

player_images = pygame.image.load('player.png')
objects_images = pygame.image.load('objects.png')

class player(pygame.sprite.Sprite):
    # make variables to describe what player can do
    def __init__(self):  # constructor or initialize()
        # call the parent class constrcutor
        pygame.sprite.Sprite.__init__(self)

        self.speed = 5
        self.hp = 3
        self.boosts = 3
        # create the player rectangle
        self.image = player_images.subsurface(pygame.Rect(212, 320, 23, 49))
        #self.image = pygame.Surface([23, 49])
        #self.image.fill(white)
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
            self.image = player_images.subsurface(pygame.Rect(146, 322, 179-146, 369-322))
            self.rect = self.image.get_rect(center=(width / 2, height / 2))
            # make everything go up left?
            global_direction = 1
        if keystate[pygame.K_d]:  # if D was pressed
            self.image = player_images.subsurface(pygame.Rect(329, 322, 367-329, 369-322))
            self.rect = self.image.get_rect(center=(width / 2, height / 2))
            # make everything go up right?
            global_direction = -1
        if keystate[pygame.K_w]:  # if W was pressed
            self.image = player_images.subsurface(pygame.Rect(5, 323, 48-5, 379-323))
            self.rect = self.image.get_rect(center=(width / 2, height / 2))
            # make everything stop?
            global_speed = 0
            global_direction = 0
        if keystate[pygame.K_s]:  # if S was pressed
            self.image = player_images.subsurface(pygame.Rect(212, 320, 23, 49))
            self.rect = self.image.get_rect(center=(width / 2, height / 2))
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


class obstacle(pygame.sprite.Sprite):
    # make variables to describe what player can do
    def __init__(self, color):  # constructor or initialize()
        # call the parent class constrcutor
        pygame.sprite.Sprite.__init__(self)

        self.x_speed = 0
        self.y_speed = 0
        self.image = pygame.Surface([random.randint(20,100), random.randint(20,100)])
        self.image.fill(color)
        # self.image = pygame.image.load("egg.png").convert()
        # self.image = pygame.transform.scale(self.image, (42, 48))
        # self.image.set_colorkey((0, 0, 0))
        # self.image = pygame.image.load("basket2.png").convert()
        # get a rectangle hitbox based on the the player image
        self.rect = self.image.get_rect()
        self.rect.y = random.randint(height + 100, height * 2 )
        self.rect.x = random.randint(width * -2, width* 2)
        self.speed = 5
        self.color = color
    def update(self):
        self.handle_movement()


    def handle_movement(self):
        self.rect.y -= global_speed
        self.rect.x += global_direction * global_speed
        # if object goes offscreen we either delete it or reuse it
        if self.rect.bottom <= 0:
            self.rect.y = random.randint(height + 100, height * 2 )
            self.rect.x = random.randint(width * -2, width* 2)

            self.image.fill(self.color)



class powerup(pygame.sprite.Sprite):
    # make variables to describe what player can do
    def __init__(self, color):  # constructor or initialize()
        # call the parent class constrcutor
        pygame.sprite.Sprite.__init__(self)

        self.x_speed = 0
        self.y_speed = 0
        self.image = pygame.Surface([20, 20])
        self.image.fill(color)
        # self.image = pygame.image.load("egg.png").convert()
        # self.image = pygame.transform.scale(self.image, (42, 48))
        # self.image.set_colorkey((0, 0, 0))
        # self.image = pygame.image.load("basket2.png").convert()
        # get a rectangle hitbox based on the the player image
        self.rect = self.image.get_rect()
        self.rect.y = random.randint(height + 100, height * 2 )
        self.rect.x = random.randint(width * -2, width* 2)
        self.speed = 5
        self.color = color

    def update(self):
        self.handle_movement()


    def handle_movement(self):
        self.rect.y -= global_speed
        self.rect.x += global_direction * global_speed
        # if object goes offscreen we either delete it or reuse it
        if self.rect.bottom <= 0:
            self.rect.y = random.randint(height + 100, height * 2 )
            self.rect.x = random.randint(width * -2, width* 2)

            self.image.fill(self.color)

font_name = pygame.font.match_font('arial')


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, black)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def game_over():
    print("Game Over")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

# create the Main Game Loop
def game():
    global global_speed
    mp = player()  # created main player
    all_sprites.add(mp)  # add mp to sprite group
    for i in range(40):
        e = obstacle(red)
        all_sprites.add(e)
        enemy_sprites.add(e)
    for i in range(30):
        e = obstacle(blue)
        all_sprites.add(e)
        slow_sprites.add(e)

    for i in range(10):
        e = obstacle((240,248,255))
        all_sprites.add(e)
        misc_sprites.add(e)

    for i in range(4):
        e = powerup(green)
        all_sprites.add(e)
        power_sprites.add(e)
    hurt = False
    turn = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                mp.handleMovement()
            if event.type == pygame.USEREVENT+1:
                #timer event that will return speed back to normal
                global_speed = 5
                mp.speed = 5
                pass
            if event.type == pygame.USEREVENT+2:
                #timer event that will return speed back to normal
                hurt = False
                turn = False
                pass
        clock.tick(60)  # set FPS to 60 FPS

        hits = pygame.sprite.spritecollide(mp, enemy_sprites, False)

        if hits and not hurt:
            hurt = True
            mp.hp -= 1
            if mp.hp <= 0:
                game_over()
            else:
                global_speed = 0
                mp.speed = 0
                #timer event that will return speed back to normal
                pygame.time.set_timer(pygame.USEREVENT+1, 2000, loops=0)
                pygame.time.set_timer(pygame.USEREVENT+2, 3000, loops=0)

        hits = pygame.sprite.spritecollide(mp, slow_sprites, False)
        if hits:
            global_speed = 2
            mp.speed = 2
            #timer event that will return speed back to normal
            pygame.time.set_timer(pygame.USEREVENT+1, 1000, loops=0)
        hits = pygame.sprite.spritecollide(mp, power_sprites, True)
        if hits:
            mp.boosts += 1

        hits = pygame.sprite.spritecollide(mp, misc_sprites, False)
        if hits and not turn:
            global global_direction
            turn = True
            if global_direction == 1:
                global_direction = -1
            elif global_direction == -1:
                global_direction = 1
            else:
                global_direction = random.randint(-1, 1)
            pygame.time.set_timer(pygame.USEREVENT+2, 2000, loops=0)

        # screen.blit(bg, bg_rect)
        screen.fill(snow)
        all_sprites.update()
        all_sprites.draw(screen)
        pygame.display.update()  # Actually draws the game


if __name__ == "__main__":
    game()
