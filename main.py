import pygame
import random
import math
from pygame import mixer
pygame.init()
s=pygame.display.set_mode((800,600))
r=True
pygame.display.set_caption("Black Panther")
icon=pygame.image.load('cat.png')
pygame.display.set_icon(icon)
# Player details
player=pygame.image.load("ufo.png")
playerX,playerY=370,480
changeX,changeY=0,0

#Enemy Details
#no.of enemies
num=5
enemy=[]
    #=pygame.image.load("enemy.png")
enemyX=[]
    #=random.randint(0,736)
enemyY=[]
    #=random.randint(50,150)
enemy_changeX=[]
    #=0.15

for i in range(num):
    enemy.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0,736))
    enemyY.append(random.randint(50,150))
    enemy_changeX.append(2)

#Bullet details
bullet=pygame.image.load("bullet.png")
bulletX=playerX
bulletY=playerY
bullet_changeY=5
bullet_state="ready"

#Score Details
score=0
font=pygame.font.Font('freesansbold.ttf',20)
textX=15
textY=12

#Game_Over Details
over_font=pygame.font.Font("freesansbold.ttf",65)
X=200
Y=280

#Background
background=pygame.image.load("background.jpg")
mixer.music.load("background_sound.wav")
mixer.music.play(-1)
def Player(x,y):
    s.blit(player,(x,y))
def Enemy(i,x,y):
    s.blit(enemy[i],(x,y))
def Bullet(x,y):
    s.blit(bullet,(x+16,y+10))
def Collision(x1,y1,x2,y2):
    distance=math.sqrt(pow(x1-x2,2)+pow(y1-y2,2))
    if distance<27:
        return True
    else:
        return False
def show_score(x,y):
    f = "SCORE" + " - " + str(score)
    text = font.render(f, True, (255, 255, 255))
    s.blit(text,(textX,textY))

def Game_Over():
    t1=over_font.render("GAME OVER",True,(255,255,255))
    s.blit(t1,(X,Y))

while r:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            r=False
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_UP:
                changeY=-3
            if event.key==pygame.K_DOWN:
                changeY=3
            if event.key==pygame.K_RIGHT:
                changeX=3
            if event.key==pygame.K_LEFT:
                changeX=-3
            if event.key==pygame.K_SPACE:
                if bullet_state=="ready":
                    bullet_state="fire"
                    bulletX=playerX
                    bulletY=playerY
                    bullet_sound=mixer.Sound("laser.wav")
                    bullet_sound.play()
                    Bullet(bulletX,bulletY)

        if event.type==pygame.KEYUP:
            changeX,changeY=0,0
    s.blit(background,(0,0))
    if bulletY<=0:
        bullet_state="ready"
        bulletY=playerY
        bulletX=playerX
    if bullet_state=="fire":
        bulletY-=bullet_changeY
        Bullet(bulletX,bulletY)

    if playerX+changeX<730 and playerX+changeX>0:
        playerX+=changeX
    if playerY+changeY<530 and playerY+changeY>0:
        playerY+=changeY
    Player(playerX,playerY)
    for i in range(num):
        if ((enemyX[i]>playerX and enemyX[i]-playerX<60) or (enemyX[i]<playerX and playerX-enemyX[i]<60)) and playerY-enemyY[i]<40:
            for i in range(num):
                enemyY[i]=2000
            Game_Over()
            break
        enemyX[i]+=enemy_changeX[i]
        if enemyX[i]<=0:
            enemyY[i]+=15
            enemyX[i]=0
            enemy_changeX[i]=2
        elif enemyX[i]>=730:
            enemyY[i]+=15
            enemyX[i]=730
            enemy_changeX[i]=-2
        collison=False
        if bullet_state=="fire":
            collison=Collision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collison:
            bullet_state="ready"
            explosion_sound=mixer.Sound("explosion.wav")
            explosion_sound.play()
            score+=10
            if enemyX[i]>368:
                enemyX[i]=random.randint(0,300)
            else:
                enemyX[i]=random.randint(400,736)
            if enemyY[i]>100:
                enemyY[i]=random.randint(50,80)
            else:
                enemyY[i]=random.randint(120,150)
        Enemy(i,enemyX[i], enemyY[i])
    show_score(textX,textY)
    pygame.display.update()