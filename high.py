import pygame
import random
from pygame.sprite import *
from pygame.locals import *
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
TITLE = "PIRATES ARE COMING!!!!"
BGCOLOR = LIGHTBLUE

############  DEFINE SPRITES  ############
class Captain(pygame.sprite.Sprite):
    # captain sprite - moves left/right, shoots
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load("/Users/JBone/Documents/sssship.bmp").convert_alpha()
        #self.image = pygame.Surface((50, 40))
        #self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.radius = 25
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
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
        spear= Spear(self.rect.left, self.rect.top)
        all_sprites.add(spear)
        spears.add(spear)
        #####
        spear2= Spear(self.rect.right, self.rect.top)
        all_sprites.add(spear2)
        spears.add(spear2)

class Pirate(pygame.sprite.Sprite):
    # mob sprite - spawns above top and moves downward
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load("/Users/JBone/Documents/pppship.bmp").convert_alpha()
        #self.image = pygame.Surface((30, 40))
        #self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.radius= int(self.rect.width /2)
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-80, -50)
        self.speedy = random.randrange(1, 4)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10:
            self.rect.y = random.randrange(-80, -50)
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.speedy = random.randrange(1, 8)


class Shark(Pirate):
    def __init__(self):
        Pirate.__init__(self)
        #self.image=pygame.Surface((15, 20))
        #self.image.fill(BLUE)
        self.image=pygame.image.load("/Users/JBone/Documents/ssshark.bmp").convert_alpha()
        self.rect= self.image.get_rect()
        self.radius= int(self.rect.width /2)
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.speedy=random.randrange(1, 4)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        #self.image = pygame.Surface((10, 20))
        #self.image.fill(YELLOW)
        self.image=pygame.image.load("/Users/JBone/Documents/bullet.bmp").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # kill if off top of screen
        if self.rect.bottom < 0:
            self.kill()

class Spear(Bullet):
    def __init__ (self, x, y):
        Bullet.__init__(self, x, y)
        #self.image = pygame.Surface((5, 10))
        #self.image.fill(GREEN)
        self.image=pygame.image.load("/Users/JBone/Documents/sspear.bmp").convert_alpha()

####
num_hits= 0
# initialize pygame
pygame.mixer.init()
pygame.mixer.pre_init(44100,-16,2, 3072)
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
#####Music Time#######
pygame.mixer.music.load("Fack.wav")
pygame.mixer.music.set_volume(0.7)
pygame.mixer.music.play()

###MOVE ABOVE###
clock = pygame.time.Clock()

# set up new game
all_sprites = pygame.sprite.Group()
pirates = pygame.sprite.Group()
bullets = pygame.sprite.Group()
sharks= pygame.sprite.Group()
spears = pygame.sprite.Group()

captain = Captain()
all_sprites.add(captain)


for i in range(8):
    p = Pirate()
    all_sprites.add(p)
    pirates.add(p)

for i in range(8):
    s= Shark()
    all_sprites.add(s)
    sharks.add(s)

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
                captain.shoot()
            elif event.key == pygame.K_z:
                captain.power()

    ##### Game logic goes here  #########
    
    all_sprites.update()
    # check if bullets hit mobs
    hits = pygame.sprite.groupcollide(pirates, bullets, True, True)
    for hit in hits:
        p = Pirate()
        all_sprites.add(p)
        pirates.add(p)
        num_hits +=1
    #check if bullets hit meteor
    hits= pygame.sprite.groupcollide(sharks, spears, True, True)
    for hit in hits:
        s= Shark()
        all_sprites.add(s)
        sharks.add(s)
        num_hits += (1/2)
    
    # check if mobs hit captain
    hits = pygame.sprite.spritecollide(captain, pirates, False, pygame.sprite.collide_circle)
    if hits:
        running = False

    #check if meteor hit captain
    hits= pygame.sprite.spritecollide(captain, sharks, False, pygame.sprite.collide_circle)
    if hits:
        running = False
    
    ##### Draw/update screen #########
    screen.fill(BGCOLOR)

    myfont = pygame.font.Font(None, 30)
    t=myfont.render("Hit Count: " + str(num_hits), False, (0, 255, 0))
    screen.blit(t, (300, 570))
    
    all_sprites.draw(screen)
    # after drawing, flip the display
    pygame.display.flip()
print ('Final score is ' + str(num_hits))