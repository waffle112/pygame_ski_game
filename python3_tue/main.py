import sys, pygame
import random

# initialize pygame and "boot" it up
pygame.init()

# create game window size
size = width, height = 500, 500
screen = pygame.display.set_mode(size)

# create variable that handles FPS (frames per sec)
clock = pygame.time.Clock()

# create some base rgb colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

# sprite groups
all_sprites = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()


class player(pygame.sprite.Sprite):
    # make variables to describe what player can do
    def __init__(self):  # constructor or initialize()
        # call the parent class constrcutor
        pygame.sprite.Sprite.__init__(self)

        self.x_speed = 0
        self.y_speed = 0
        self.speed = 5
        self.hp = 3
        self.boosts = 0
        # create the player rectangle
        # self.image = pygame.Surface([30, 40])
        # self.image.fill(white)
        self.image = pygame.image.load("basket.png").convert()
        self.image.set_colorkey((0, 0, 0))
        # get a rectangle hitbox based on the the player image
        self.rect = self.image.get_rect()
        self.rect.y = height - 100
        self.rect.x = width / 2

    # update function
    def update(self):
        self.handleMovement()
        self.handleBoost()

    # make methods to have player do somehting
    # movement
    def handleMovement(self):
        # if a particular keyboard button has been pressed -> do something

        # get keystate
        keystate = pygame.key.get_pressed()

        # check if keystate is of a particular button
        # modify what happens to change how the player moves
        if keystate[pygame.K_a]:  # if A was pressed - go downward left x_speed = -speed AND y_speed = speed
            self.x_speed = -self.speed
        if keystate[pygame.K_d]:  # if D was pressed
            self.x_speed = self.speed
        if keystate[pygame.K_w]:  # if W was pressed
            self.y_speed = -self.speed
        if keystate[pygame.K_s]:  # if S was pressed
            self.y_speed = self.speed

        # actually move the player
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed

        # reset
        self.y_speed = 0
        self.x_speed = 0

        # boundaries
        if self.rect.right >= width:
            self.rect.right = width
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= height:
            self.rect.bottom = height

    # if player clicks on boost button -> go fast
    def handleBoost(self):
        # if a particular keyboard button OR A MOUSE CLICK has been pressed -> do something
        pass


class enemy(pygame.sprite.Sprite):
    # make variables to describe what player can do
    def __init__(self):  # constructor or initialize()
        # call the parent class constrcutor
        pygame.sprite.Sprite.__init__(self)

        self.x_speed = 0
        self.y_speed = 0
        self.speed = random.randint(1, 5)
        self.hp = 3
        self.boosts = 0
        # create the player rectangle
        # self.image = pygame.Surface([30, 40])
        # self.image.fill(red)
        self.image = pygame.image.load("egg.png").convert()
        self.image = pygame.transform.scale(self.image, (42, 48))
        self.image.set_colorkey((0, 0, 0))
        # self.image = pygame.image.load("basket2.png").convert()
        # get a rectangle hitbox based on the the player image
        self.rect = self.image.get_rect()
        self.rect.y = random.randint(-200, -40)
        self.rect.x = random.randint(0, width - 30)

    def update(self):
        self.handle_movement()
        pass

    def handle_movement(self):
        self.rect.y += self.speed

        # if object goes offscreen we either delete it or reuse it
        if self.rect.top >= height:
            self.rect.y = random.randint(-200, -40)
            self.rect.x = random.randint(0, width - 30)
            self.speed = random.randint(1, 5)


font_name = pygame.font.match_font('arial')


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, black)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


# create the Main Game Loop
def game():
    mp = player()  # created main player
    all_sprites.add(mp)  # add mp to sprite group
    total = 0
    for i in range(10):
        e = enemy()
        all_sprites.add(e)
        enemy_sprites.add(e)

    bg = pygame.image.load("Full-Background.png").convert()
    bg_rect = bg.get_rect(center=(width / 2, -100))

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

        clock.tick(60)  # set FPS to 60 FPS

        all_sprites.update()

        hits = pygame.sprite.spritecollide(mp, enemy_sprites, True)
        for h in hits:
            total += 10
            print(total)
            e = enemy()
            all_sprites.add(e)
            enemy_sprites.add(e)
        # draw game
        # screen.fill(black)  # draw the background
        screen.blit(bg, bg_rect)
        all_sprites.draw(screen)  # draw each sprite in the sprite group
        draw_text(screen, str(total), 18, width/2, 10)

        pygame.display.update()  # Actually draws the game


if __name__ == "__main__":
    game()
