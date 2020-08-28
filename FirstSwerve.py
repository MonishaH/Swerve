import pygame
import random
import os 


WIDTH = 750
HEIGHT = 600
FPS = 60

#define colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)


#Initialise pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Swerve")
clock = pygame.time.Clock()


        # --- Making the Player + Movements ---
        
class Player(pygame.sprite.Sprite): #Hero
    #sprite for the Player
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #mandtatory built in function
        self.image = pygame.Surface((35,35))
        self.image.fill(BLUE) 
        #every sprite has to have this self.rect. Rect that encloses the sprite moving it
        #around and determines where it is in the screen.
        self.rect = self.image.get_rect()
        #lets put the player at the center of the screen
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 8
        self.speedx = 0

    def update(self):
        self.speedx = 0 #speed of player is always zero, should never be moving
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        self.rect.x += self.speedx
        #player will not move outside the window box when moving left/right
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

        self.speedy = 0
        if keystate[pygame.K_UP]:
            self.speedy = -6
        if keystate[pygame.K_DOWN]:
            self.speedy = 6
        self.rect.y += self.speedy
        #player will not move outside the window box when moving up/down
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        
            
        # --- Making the Attackers + Movements ---

class Attacker(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30,35))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100,-60)
        self.speedy = random.randrange(1,6) #randomize their speed. slow + fast
        #move from side to side
        self.speedx = random.randrange(-1,3)

        
    def update(self):
        self.rect.x += self.speedx #udated for moving side to side 
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 15:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100,-60)
            self.speedy = random.randrange(-1,3)



all_sprites = pygame.sprite.Group()
#group to hold the attackers
attackers = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

for i in range(20): #number of attackers
    a = Attacker()
    all_sprites.add(a)
    attackers.add(a)
    

#Game Loop
running = True
while running:
    #Keep loop running at the right speed
    clock.tick(FPS)
    #process input (events)
    for event in pygame.event.get():
        #check for closing window
        if event.type ==pygame.QUIT:
            running = False

    #Update
    all_sprites.update()
    
    #Draw / render
    screen.fill(BLACK)
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
