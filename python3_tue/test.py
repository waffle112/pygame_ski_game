import pygame
import random

pygame.init()

screen_width = 500
screen_height = 500

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Boundaries")

white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)

# create variable that handles FPS (frames per sec)
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        # call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        # create an image of the block and fill it with a color
        # this could also be an image loaded from the disk
        # self.image = pygame.Surface([30, 40])
        # self.image.fill(white)
        self.image = pygame.image.load("basket.png").convert()
        self.image.set_colorkey((0, 0, 0))
        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        # self.rect = self.image.get_rect(center = (x,y))
        self.rect = self.image.get_rect(center=(screen_width / 2, screen_height - 30))

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
        if keystate[pygame.K_UP]:
            self.y_speed -= 7
        elif keystate[pygame.K_DOWN]:
            self.y_speed += 7
        elif keystate[pygame.K_LEFT]:
            self.x_speed -= 7
        elif keystate[pygame.K_RIGHT]:
            self.x_speed += 7

        self.rect.x += self.x_speed
        self.rect.y += self.y_speed

        # Keep player inside screen bounds
        if self.rect.right >= screen_width:
            self.rect.right = screen_width
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height


class Enemy(pygame.sprite.Sprite):
    '''
    we want enemies to spawn above the screen so they do not seem
    like they are just appearing randomly and we want to make sure
    that they are falling in between the sides of the screen. We will
    set a random speed for the enemy to move down the screen towards the
    bottom.
    '''

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # self.image = pygame.Surface([30, 40])
        # self.image.fill(red)
        self.image = pygame.image.load("egg.png").convert()
        self.image = pygame.transform.scale(self.image, (42, 48))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(screen_width - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.y_speed = random.randrange(1, 3)

        '''
     The enemy will move on its own as it spawns in. Once the enemy reaches
     the bottom of the screen and is out of the player's sight we want to 
     respawn the enemy above the screen again. For this we will set rect.x, rect.y
     and y_speed to its initial values that we gave it in the init function.
     '''

    def update(self):
        self.rect.y += self.y_speed
        if self.rect.top > screen_height + 10:
            self.rect.x = random.randrange(screen_width - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.y_speed = random.randrange(1, 3)


font_name = pygame.font.match_font('arial')


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, black)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def game():
    all_sprites = pygame.sprite.Group()
    player = Player()
    all_sprites.add(player)

    enemies = pygame.sprite.Group()
    # start with spawning five enemies at the start of the game
    for i in range(5):

        e = Enemy()
        all_sprites.add(e)
        enemies.add(e)

    bg = pygame.image.load("Full-Background.png").convert()
    bg_rect = bg.get_rect(center=(screen_width / 2, -100))
    total = 0
    # game loop
    while True:
        clock.tick(60)  # set FPS to 60 FPS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        all_sprites.update()

        hits = pygame.sprite.spritecollide(player, enemies, True)

        for hit in hits:
            total += 10
            e = Enemy()
            all_sprites.add(e)
            enemies.add(e)

        # Draw/render
        screen.blit(bg, bg_rect)
        all_sprites.draw(screen)  # draw each sprite in the sprite group
        draw_text(screen, str(total), 18, screen_width/2, 10)

        # Mandatory otherwise sprite won't show
        # *after* drawing everything flip the display

        pygame.display.flip()

if __name__ == "__main__":
    game()