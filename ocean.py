import pygame
import random

# define some colors (R, G, B)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
LIGHTBLUE= (30, 144, 255)
# game settings
WIDTH = 480
HEIGHT = 600
FPS = 60
TITLE = "SHMUP"
#BGCOLOR = pygame.image.load("/Users/JBone/Documents/ocean.bmp").convert()


# initialize pygame
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("UNDERATTACK!")
clock = pygame.time.Clock()


############  DEFINE SPRITES  ############
class Player(pygame.sprite.Sprite):
    # player sprite - moves left/right, shoots
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load("/Users/JBone/Documents/sssship.bmp").convert_alpha()
        #self.image = pygame.Surface((50, 40))
        #self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.rect.left= WIDTH / 4
        self.rect.right = WIDTH / 4
        self.speedx = 0

    def update(self):
        # only move if arrow key is pressed
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        if keystate[pygame.K_RIGHT]:
            self.speedx = 5

        # move the sprite
        self.rect.x += self.speedx
        # stop at the edges
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        ######
    def power(self):
        newbullet= NewBullet(self.rect.left, self.rect.top)
        all_sprites.add(newbullet)
        newbullets.add(newbullet)
        #####
        newbullet2= NewBullet(self.rect.right, self.rect.top)
        all_sprites.add(newbullet2)
        newbullets.add(newbullet2)

class Mob(pygame.sprite.Sprite):
    # mob sprite - spawns above top and moves downward
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load("/Users/JBone/Documents/pppship.bmp").convert_alpha()
        #self.image = pygame.Surface((30, 40))
        #self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-80, -50)
        self.speedy = random.randrange(1, 4)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10:
            self.rect.y = random.randrange(-80, -50)
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.speedy = random.randrange(1, 8)


class Meteor(Mob):
    def __init__(self):
        Mob.__init__(self)
        #self.image=pygame.Surface((15, 20))
        #self.image.fill(BLUE)
        self.image=pygame.image.load("/Users/JBone/Documents/ssshark.bmp").convert_alpha()
        self.speedy=random.randrange(1, 4)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 20))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # kill if off top of screen
        if self.rect.bottom < 0:
            self.kill()

class NewBullet(Bullet):
    def __init__ (self, x, y):
        Bullet.__init__(self, x, y)
        self.image = pygame.Surface((5, 10))
        self.image.fill(GREEN)
#BACKGROUND
background= pygame.image.load("/Users/JBone/Documents/ocean.bmp").convert()
while True:
    for y in range (0, 480,5):
        for x in range (0, 600, 5):
            screen.blit (background, (x, y))
background_rect= background.get_rect()

# set up new game
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
meteors= pygame.sprite.Group()
newbullets = pygame.sprite.Group()

player = Player()
all_sprites.add(player)


for i in range(8):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

for i in range(8):
    x= Meteor()
    all_sprites.add(x)
    meteors.add(x)

running = True
while running:
    clock.tick(FPS)
    # check for events
    for event in pygame.event.get():
        # this one checks for the window being closed
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
            elif event.key == pygame.K_z:
                player.power()

    ##### Game logic goes here  #########
    all_sprites.update()
    # check if bullets hit mobs
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)
    #check if bullets hit meteor
    hits= pygame.sprite.groupcollide(meteors, newbullets, True, True)
    for hit in hits:
        x = Meteor()
        all_sprites.add(x)
        meteors.add(x)

    # check if mobs hit player
    hits = pygame.sprite.spritecollide(player, mobs, False)
    if hits:
        running = False

    #check if meteor hit player
    hits= pygame.sprite.spritecollide(player, meteors, False)
    if hits:
        running = False

    ##### Draw/update screen #########
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    # after drawing, flip the display
    pygame.display.flip()
