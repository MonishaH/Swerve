import pygame
import random
import sys 
from os import path


img_dir = path.join(path.dirname(__file__), 'img')


WIDTH = 750
HEIGHT = 600
FPS = 60
move_side = 20
move_event = pygame.USEREVENT + 1

#define colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
PURPLE = (255,0,255)

#Initialise pygame and create window
pygame.init()
pygame.mixer.init() #for the sound 
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Swerve")
clock = pygame.time.Clock()

#Game Sounds
#hitsound = pygame.mixer.Sound('C:/Users/18622/Desktop/soundfolder/ses.wav')
hitsound = pygame.mixer.Sound('C:/Users/18622/Downloads/Cat Yelling In Fear-SoundBible.com-455973055.wav')
goversound = pygame.mixer.Sound('C:/Users/18622/Downloads/GameOver.wav')

music = pygame.mixer.music.load('C:/Users/18622/Desktop/bgsong.mp3')
pygame.mixer.music.play(loops=-1)

score = 0
gameLives = 3
gameNo = 2

#pygame.mixer.music.play(loops=-1)

font_name = pygame.font.match_font('arial')

def draw_text(surf, text, size, x, y): #xy for location, size for how big
     

    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE) #True/False whether you
                                            #want the font anti-alias or not
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surf.blit(text_surface, text_rect)



        # --- Making the Player + Movements ---
        
class Player(pygame.sprite.Sprite): #Hero
    
    #sprite for the Player
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (65,65))
        self.image.set_colorkey(BLACK)
        
        #every sprite has to have this self.rect. Rect that encloses the sprite moving it
        #around and determines where it is in the screen.
        self.rect = self.image.get_rect()
        self.radius = 21
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
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

    def reset(self):
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 8
        
            
        # --- Making the Attackers + Movements ---

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
            self.speedy = random.randrange(1,8)

    def reset(self):
        #self.rect.y = 0
        #self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100,-40)
        self.speedy = random.randrange(1,3)

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
        print(self.frame)
        if current_time - self.last_update > self.frame_rate:
            self.last_update = current_time
            self.frame += 1
            if self.frame == len(self.explosion_anim[self.ex_type]):
                self.kill()
                return True
            else:
                center = self.rect.center
                self.image = self.explosion_anim[self.ex_type][self.frame]
                self.rect.center = center
        

        
#Load all game graphics
background = pygame.image.load('img/bg.png').convert()
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir, "cat3.png")).convert()
attacker_img = pygame.image.load(path.join(img_dir, "fire1.png")).convert_alpha()


explosion_anim = {}
explosion_anim['large'] = []
explosion_anim['small'] = []
for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert_alpha()
    image_lg = pygame.transform.scale(img, (45,45))
    explosion_anim['large'].append(image_lg)
    image_sm = pygame.transform.scale(img, (20,20))
    explosion_anim['small'].append(image_sm)

    print(filename)

img = pygame.image.load(path.join(img_dir, filename)).convert_alpha()

#our group
all_sprites = pygame.sprite.Group()
#group to hold the attackers
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
#variable = 1
hope = False

#Game Loop

running = True
while running:
    
    score += 1
     
    #Keep loop running at the right speed
    clock.tick(FPS)
    #process input (events)
   
    for event in pygame.event.get():
        if event.type == move_event:
           
            attackers.update()
            #player.update()
            
        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                 running = False
                 pygame.quit()
                 #print('escape')
                 sys.exit()
                 if event.type == pygame.QUIT:
                     running = False

                     
   
    #Update
    player.update()
   # explosion.update()
    ##rebirth = explosion.update()
    

    #check to see if an attacker hits the player
    
    collisions = pygame.sprite.spritecollide(player, attackers, False, pygame.sprite.collide_circle)
    #if collisions:
    #for hit in collisions:
        ##expl = Explosion(hit.rect.center, 'large', explosion_anim)
        ##explosion.add(expl)
        ##all_sprites.add(expl)

    
   # print(len(explosion))
    ##if collisions:
        ##hope = True
        ##pygame.event.clear()
    if len(explosion) == 0 and hope == True:
        ##hope = False 
        #print('hello')
        #pygame.event.pump()
        #pygame.time.wait(3000)
        
         #screen.blit(background, background_rect)
        
        #gameLives -= 1

       # if gameLives >= 1:
            
          #  pygame.draw.rect(screen, BLUE, (210, 280, 320, 80))
          #  draw_text(screen, 'You died! You have' + ' ' + str(gameLives) + ' ' + 'lives remaining', 20, 375, 300)
          #  draw_text(screen, 'The game will restart in' + ' ' + str(3) + ' ' + 'seconds', 20, 380, 320)
           # hitsound.play()
                            
            #for attacker in attackers:
           #     attacker.reset()
               # player.reset()           
                
        #if gameLives < 1: #moves toright, #lower num then goes up, #lower number, gets thinner and longer
                   # pygame.draw.rect(screen, GREEN, (194, 185, 396, 280))
                   # draw_text(screen, 'Game over!', 48, 390, 240)
                    #draw_text(screen, 'Your final score is:', 28, 390, 310)
                    #draw_text(screen, str(score - 1) + ' ', 32, 392, 360)
                    #hitsound.play()
                    #pygame.time.wait(1000)
                   # goversound.play()
                   # pygame.mixer.music.pause()
                   # pygame.display.update()
                    #pygame.time.wait(100000)
                   # pygame.quit()
 
 
        #if score > topScore:
        ##    topScore = score

        #pygame.display.update()
       # pygame.time.wait(3000)
        #pygame.event.clear()
    
    #Draw / render
    #screen.fill(GREEN)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, 'Score:' + ' ' + str(score), 18, WIDTH / 2, 5)
    draw_text(screen, 'Top Score:' + ' ' +str(topScore), 18, WIDTH / 2, 28)
    draw_text(screen, 'Lives:' + ' ' +str(gameLives), 18, WIDTH / 2, 50)

            

    pygame.display.flip()

pygame.quit()
