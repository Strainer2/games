import pygame
import random
from pygame.sprite import *
from pygame.locals import *

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
########
class Captain(pygame.sprite.Sprite):
    # captain sprite - moves left/right, shoots
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load("img/sssship.bmp").convert_alpha()
        self.rect = self.image.get_rect()
        self.radius = 25
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
        self.rect.x += self.speedx
        # stop at the edges
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        #shooting bullets to kill Pirates
    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        #shooting spears to kill Sharks and Whales
    def power(self):
        spear= Spear(self.rect.left, self.rect.top)
        all_sprites.add(spear)
        spears.add(spear)
        #getting two spears to shoot at saem time of edges of Captains ship
        spear2= Spear(self.rect.right, self.rect.top)
        all_sprites.add(spear2)
        spears.add(spear2)

class Pirate(pygame.sprite.Sprite):
    #spawns pirates above window and moves downward
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load("img/pppship.bmp").convert_alpha()
        self.rect = self.image.get_rect()
        self.radius= int(self.rect.width /2)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-80, -50)
        self.speedy = random.randrange(1, 8)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10:
            self.rect.y = random.randrange(-80, -50)
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.speedy = random.randrange(1, 8)


class Shark(Pirate):
    #spawns Sharks
    def __init__(self):
        Pirate.__init__(self)
        self.image=pygame.image.load("img/ssshark.bmp").convert_alpha()
        self.rect= self.image.get_rect()
        self.radius= int(self.rect.width /2)
        self.speedy=random.randrange(9, 12)

class Whale(Pirate):
    #spawns Whale
    def __init__(self):
        Pirate.__init__(self)
        self.image=pygame.image.load("img/whale.bmp").convert_alpha()
        self.rect= self.image.get_rect()
        self.radius= int(self.rect.width /2)
        self.speedy= random.randrange(2,5)


class Bullet(pygame.sprite.Sprite):
    #creates Bullet Sprite
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load("img/bullet.bmp").convert_alpha()
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
    #creats Spear Sprite
    def __init__ (self, x, y):
        Bullet.__init__(self, x, y)
        self.image=pygame.image.load("img/sspear.bmp").convert_alpha()
##########################################
class Option:
    #creates beginning screen
    def __init__(self, text, pos):
        self.hovered = False
        self.text = text
        self.pos = pos
        self.set_rect()
        self.draw()

    def draw(self):
        self.set_rend()
        screen.blit(self.rend, self.rect)

    def set_rend(self):
        myfont = pygame.font.Font(None, 60)
        self.rend = myfont.render(self.text, True, self.get_color())

    def get_color(self):
        if self.hovered:
            return (255, 255, 255)
        else:
            return (100, 100, 100)

    def set_rect(self):
        self.set_rend()
        self.rect = self.rend.get_rect()
        self.rect.topleft = self.pos
###############################################
def text_objects(text, font):
    #writes instuctions on beginning page
    paragraphSize = (470, 300)
    fontSize = font.get_height()

    paragraphSurface = pygame.Surface(paragraphSize ) 
    paragraphSurface.fill((0, 255, 0))
    paragraphSurface.set_colorkey((0, 255, 0))

    splitLines = text.split(".")
    offSet = (paragraphSize[1] - len(splitLines) * (fontSize + 1)) // 2 

    for idx, line in enumerate(splitLines):
        currentTextline = font.render(line, False, (255, 0, 0))
        currentPostion = (0, idx * fontSize + offSet)
        paragraphSurface.blit(currentTextline, currentPostion)

    return paragraphSurface

######
num_hits= 0
OPTIONS = 0
BALLS= 1
instructions = "Killing a pirate: 5 points.Killing a shark: 2 points.Killing a whale: 20 points."

# initialize pygame
pygame.mixer.init()
pygame.mixer.pre_init(44100,-16,2, 3072)
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
#####Music Time#######
pygame.mixer.music.load("stan.wav")
pygame.mixer.music.set_volume(0.7)
pygame.mixer.music.play()

clock = pygame.time.Clock()

# set up new game
all_sprites = pygame.sprite.Group()
pirates = pygame.sprite.Group()
bullets = pygame.sprite.Group()
sharks= pygame.sprite.Group()
spears = pygame.sprite.Group()
whales= pygame.sprite.Group()

captain = Captain()
all_sprites.add(captain)

for i in range(9):
    p = Pirate()
    all_sprites.add(p)
    pirates.add(p)

for i in range(6):
    s= Shark()
    all_sprites.add(s)
    sharks.add(s)

for i in range (1):
    w= Whale()
    all_sprites.add(w)
    whales.add(w)
#############################
options = [Option("NEW GAME", (100, 100))]

STATE = OPTIONS
mfont = pygame.font.Font(None, 40)
x= text_objects(instructions, mfont)
running = True
while running:
    pygame.event.pump()
    screen.fill((0, 0, 0))

    if STATE == OPTIONS:
        screen.blit(x, (0, 200))
        for option in options:
            if option.rect.collidepoint(pygame.mouse.get_pos()):
                option.hovered = True
                if pygame.event.get([pygame.MOUSEBUTTONDOWN]) and option.text == "NEW GAME":
                    STATE = BALLS
            else:
                option.hovered = False
            option.draw()
            pygame.display.update()
    elif STATE == BALLS:
        screen.fill(BGCOLOR)

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

    ####RULES FOR GAME#######
    
        all_sprites.update()
    # check if bullets hit mobs
        hits = pygame.sprite.groupcollide(pirates, bullets, True, True)
        for hit in hits:
            p = Pirate()
            all_sprites.add(p)
            pirates.add(p)
            num_hits +=5
    #check if bullets hit meteor
        hits= pygame.sprite.groupcollide(sharks, spears, True, True)
        for hit in hits:
            s= Shark()
            all_sprites.add(s)
            sharks.add(s)
            num_hits += 2
    # cheack if bullets hit whale
        hits= pygame.sprite.groupcollide(whales, spears, True, True)
        for hit in hits:
            w= Whale()
            all_sprites.add(w)
            whales.add(w)
            num_hits += 20
            
    # check if pirates hit captain
        hits = pygame.sprite.spritecollide(captain, pirates, False, pygame.sprite.collide_circle)
        if hits:
            running = False

    #check if sharks hit captain
        hits= pygame.sprite.spritecollide(captain, sharks, False, pygame.sprite.collide_circle)
        if hits:
            running = False
    
    ##### Draw/update screen #########
        myfont = pygame.font.Font(None, 30)
        t=myfont.render("Hit Count: " + str(num_hits), False, (0, 255, 0))
        screen.blit(t, (300, 570))
    
        all_sprites.draw(screen)
    # after drawing, flip the display
        pygame.display.flip()
print ('FINAL SCORE IS ' + str(num_hits))