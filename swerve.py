import pygame
import random
import sys
from os import path
from pygame.locals import QUIT
import time 


img_dir = path.join(path.dirname(__file__), 'img')


WIDTH = 750
HEIGHT = 600
FPS = 60
move_side = 20
move_event = pygame.USEREVENT + 1

#Define Colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
PURPLE = (255,0,255)

#Initialise pygame and create window
pygame.init()
pygame.mixer.init()#for the sound
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Swerve")
clock = pygame.time.Clock()

#Game Sounds
hitsound = pygame.mixer.Sound('Cat Yelling In Fear-SoundBible.com-455973055.wav')
goversound = pygame.mixer.Sound('GameOver.wav')

music = pygame.mixer.music.load('bgsong.mp3')
pygame.mixer.music.play(loops=-1)


score = 0
gameLives = 3
gameNo = 2

font_name = pygame.font.match_font('arial')

def draw_text(surf, text, size, x, y): #xy for location, size for how big
     

    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE) #True/False whether you
                                            #want the font anti-alias or not
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surf.blit(text_surface, text_rect)
     

                # x --- Making the Player + Movements --- x
        
class Player(pygame.sprite.Sprite): 
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (65,65))
        self.image.set_colorkey(BLACK)
        #every sprite has to have this self.rect. Rect that encloses the sprite moving it
        #around and determines where it is in the screen.
        self.rect = self.image.get_rect()
        self.radius = 21
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        #Putting the player at the center of the screen
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

    def reset(self):
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 8 
              
                # x --- Making the Attackers + Movements --- x

class Attacker(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = attacker_img
        self.image = pygame.transform.scale(attacker_img, (30,40))
        self.image.set_colorkey(WHITE)
        
        self.rect = self.image.get_rect()
        self.radius = 18
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100,-40) #where? up above the screen
        self.speedy = random.randrange(1,3) #randomize their speed. slow + fast
        #move from side to side
        self.speedx = random.randrange(-2,2)
        
    def update(self):
        self.rect.x += self.speedx #updated for moving side to side
        
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 20 or self.rect.left < -25 or self.rect.right > WIDTH + 35:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100,-40)
            self.speedy = random.randrange(2,3)

    def reset(self):
        self.rect.y = random.randrange(-100,-40)
        self.speedy = random.randrange(1,3)
        

                        # x ----- EXPLOSION ----- x 

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, ex_type, explosion_anim):
        super().__init__()
        self.ex_type = ex_type
        self.explosion_anim = explosion_anim
        self.image = explosion_anim[self.ex_type][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        current_time = pygame.time.get_ticks()
        #print(self.frame)
        if current_time - self.last_update > self.frame_rate:
            self.last_update = current_time
            self.frame += 1
            if self.frame == len(self.explosion_anim[self.ex_type]):
                self.kill()
                #return True
            else:
                center = self.rect.center
                self.image = self.explosion_anim[self.ex_type][self.frame]
                self.rect.center = center        


                        # x ---- START SCREEN MENU ---- x

def menu():

    menumusic = pygame.mixer.music.load('Fun Background.mp3')
    pygame.mixer.music.play(loops=-1)

    #Background
    background = pygame.image.load('img/bbg.png').convert()
    background_rect = background.get_rect()

    #Extra Images for Screen
    
    fire_show = pygame.image.load(path.join(img_dir, 'fire1.png')).convert_alpha()
    fire_show = pygame.transform.scale(fire_show, (24,28))
    
    fire_showw = pygame.image.load(path.join(img_dir, 'fire1.png')).convert_alpha()
    fire_showw = pygame.transform.scale(fire_showw, (24,28))

    fire_show = pygame.image.load(path.join(img_dir, 'fire1.png')).convert_alpha()
    fire_show = pygame.transform.scale(fire_show, (24,28))

    cat_alt = pygame.image.load(path.join(img_dir, 'cat3.png')).convert_alpha()
    cat_alt = pygame.transform.scale(cat_alt, (45,45))

    arrow_keys = pygame.image.load(path.join(img_dir, 'arrows.jpg')).convert_alpha()
    arrow_keys = pygame.transform.scale(arrow_keys, (76,60))
       
    screen.blit(background, background_rect)
    screen.blit(fire_show, (340,203))
    screen.blit(fire_showw, (380, 204))
    screen.blit(fire_showw, (420, 201.4))
    screen.blit(cat_alt, (370, 232))
    screen.blit(arrow_keys, (120, 300))

    #Text for Screen 
    
    image = pygame.image.load("Welcome-to-Swerve-.png").convert_alpha()
    screen.blit(image, (70,40)) #right.left, up/down

    draw_text(screen, "This single player game is meant to be quick and easy.", 20, WIDTH/2, HEIGHT/5)
    draw_text(screen, "Simply avoid the attackers, the red fires, falling from space", 20, WIDTH/2, HEIGHT/4.2)
    draw_text(screen, "by moving your player, the blue Manx cat.", 20, WIDTH/2, HEIGHT/3.6)    
    draw_text(screen, "Use the arrow keys to move your player.", 18, WIDTH/2, HEIGHT/1.9)   
    draw_text(screen, "You have 3 lives to reachest the highest score possible.", 18, WIDTH/2, HEIGHT/1.8)
    draw_text(screen, "There is no pause button.", 18, WIDTH/2, HEIGHT/1.7)
    draw_text(screen, "Press [ENTER] to play", 32, WIDTH/2, HEIGHT/1.4)
    draw_text(screen, "Press [Q] to quit", 32, WIDTH/2, HEIGHT/1.3)
    draw_text(screen, "Special thanks to Karen for guiding me through this entire project, supporting me, and making the process enjoyable.", 14, WIDTH/2, HEIGHT/1.10)
    draw_text(screen, "Thank you to my mentor Alma for the constant support and advising me to learn and improve from every opportunity.", 14, WIDTH/2, HEIGHT/1.07)
    draw_text(screen, "Thank you to America Needs You for providing me with this and many other countless opportunities while positively impacting our life.", 14, WIDTH/2, HEIGHT/1.04)

    
    pygame.display.update()
    
    while True:
        event = pygame.event.poll()
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_RETURN:
                break
            elif event.key == pygame.K_q:
                pygame.quit()
                sys.exit()
        elif event.type == QUIT:
            pygame.quit()
            sys.exit()

    
#Load all game graphics
background = pygame.image.load('img/bg.png').convert()
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir, "cat3.png")).convert()
attacker_img = pygame.image.load(path.join(img_dir, "fire1.png")).convert_alpha()

### EXPLOSION SPRITE
explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
for i in range(3):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (75,75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32,32))
    explosion_anim['sm'].append(img_sm)


# Our Sprite Groups
all_sprites = pygame.sprite.Group()
attackers = pygame.sprite.Group()
player = Player()
explosion = pygame.sprite.Group()
all_sprites.add(player)

for i in range(20):
    
    #number of attackers
    a = Attacker()
    all_sprites.add(a)
    attackers.add(a)

pygame.time.set_timer(move_event, move_side)

score = 0
topScore = 0
hope = False

#Game Loop

running = True
show_menu = True

while running:
    score += 1
    #Keep loop running at the right speed
    clock.tick(FPS)
    #process input (events)
    if show_menu:
        menu()
        pygame.time.delay(0)
        pygame.mixer.music.fadeout(1000)
        pygame.mixer.music.load('bgsong.mp3')
        pygame.mixer.music.play(-1)
        show_menu = False        

    for event in pygame.event.get():
        if event.type == move_event:
            attackers.update()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                    pygame.quit()
                    sys.exit()
                    if event.type == pygame.QUIT:
                        running = False

   
    #Updating Sprites
    player.update()
    attackers.update()
    explosion.update()
    

    #Check to see if an attacker hits the player
    collisions = pygame.sprite.spritecollide(player, attackers, True, pygame.sprite.collide_circle)
    for hit in collisions:
        expl = Explosion(player.rect.center, 'lg', explosion_anim)
        explosion.add(expl)
        all_sprites.add(expl)

        new_attacker = Attacker()
        attackers.add(new_attacker)
        all_sprites.add(new_attacker)

    if collisions:
            hope = True
            pygame.time.set_timer(move_event, 0)
            pygame.event.clear()

    if len(explosion) == 0 and hope == True:
        hope = False
        pygame.time.set_timer(move_event, move_side)

        gameLives -= 1

        if gameLives >= 1:
            
            
            pygame.draw.rect(screen, BLUE, (210, 280, 320, 80))
            draw_text(screen, 'You died! You have' + ' ' + str(gameLives) + ' ' + 'lives remaining', 20, 375, 300)
            draw_text(screen, 'The game will restart in' + ' ' + str(3) + ' ' + 'seconds', 20, 380, 320)
            hitsound.play()

                             
            for attacker in attackers:
                attacker.reset()
                player.reset()

            
        if gameLives < 1:
                pygame.draw.rect(screen, GREEN, (194, 185, 396, 280))
                draw_text(screen, 'Game over!', 48, 390, 240)
                draw_text(screen, 'Your final score is:', 28, 390, 310)
                draw_text(screen, str(score - 1) + ' ', 32, 392, 360)
                pygame.mixer.music.pause()
                goversound.play()
                pygame.display.update()
                pygame.time.wait(4000)
                show_menu = True 
                                          
        if score > topScore:
            topScore = score
      
        
        pygame.display.update()
        pygame.event.pump() #not behind by a frame 
        pygame.time.wait(3000)
        
        pygame.event.clear()
    
    #Draw / render
    #screen.fill(GREEN)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, 'Score:' + ' ' + str(score), 18, WIDTH / 2, 5)
    draw_text(screen, 'Top Score:' + ' ' +str(topScore), 18, WIDTH / 2, 28)
    draw_text(screen, 'Lives:' + ' ' +str(gameLives), 18, WIDTH / 2, 50)
    
    

    pygame.display.flip()

pygame.quit()

