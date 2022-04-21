import os
import sys

import pygame
import pygame.display
pygame.font.init()
pygame.mixer.init()


'''
X to shoot for left player, m to shoot for right player
WASD to move left, arrows for right

'''

WIDTH, HEIGHT = 900,500 #sets size of window as a constant
WIN= pygame.display.set_mode((WIDTH,HEIGHT)) #displays window
pygame.display.set_caption("StarWars DogFight!")

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)
GREEN = (0,255,0)
DIVIDER = pygame.Rect(WIDTH//2 - 5 , 0, 10, HEIGHT)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
BULLET_HIT_SOUND.set_volume(0.1)
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Blaster effect.mp3'))
BULLET_FIRE_SOUND.set_volume(0.1)

HEALTH_FONT = pygame.font.SysFont('comicsans', 25)
WINNER_FONT = pygame.font.SysFont('comicsans', 25)

FPS = 60
VEL = 5
BULLETS_VEL = 7
MAX_BULLETS = 3


SHIP_WIDTH, SHIP_HEIGHT = 100,75
TIE_WIDTH, TIE_HEIGHT = 50, 50

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets','cool.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SHIP_HEIGHT, SHIP_WIDTH)), 270)


RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets','tie_fighter.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (TIE_HEIGHT, TIE_WIDTH)), 0)

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets','starwars.png')), (WIDTH,  HEIGHT))


def draw_window(red, yellow, red_bullets , yellow_bullets, red_health, yellow_health):

    WIN.blit(SPACE,(0,0))
    pygame.draw.rect(WIN, BLACK, DIVIDER)

    red_health_text = HEALTH_FONT.render("Health: "  + str(red_health), 1,WHITE)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10,10))


    WIN.blit(YELLOW_SPACESHIP,(yellow.x, yellow.y)) #blit draws surface on screen
    WIN.blit(RED_SPACESHIP, (red.x, red.y))



    for bullets in red_bullets:
        pygame.draw.rect(WIN, RED, bullets)

    for bullets in yellow_bullets:
        pygame.draw.rect(WIN, GREEN, bullets)

    pygame.display.update()  # updates display once colour changes

def yellow_movement(keys_pressed, yellow):
    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:  # left
        yellow.x -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT:
        yellow.y += VEL
    if keys_pressed[pygame.K_d]  and yellow.x + VEL + yellow.width < DIVIDER.x:
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:
        yellow.y -= VEL

def red_movement(keys_pressed, red):
    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > DIVIDER.x + DIVIDER.width:  # left
        red.x -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL+ red.height < HEIGHT:
        red.y += VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:  #right
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL>0:
        red.y -= VEL


def handle_bullets(yellow_bullets,red_bullets, yellow , red): #ALL BULLET INTERACTIONS
    for bullet in yellow_bullets:
        bullet.x += BULLETS_VEL
        if red.colliderect(bullet):#if rect representing yellow, colides with bullet
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLETS_VEL
        if yellow.colliderect(bullet):#if rect representing red, colides with bullet
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)


def draw_winner(text):
    draw_text = WINNER_FONT.render(text,1,WHITE)
    WIN.blit(draw_text,(WIDTH//2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(3000) #the time the game stays open wh




def MainMenu():
    title = pygame.font.SysFont("comicsans", 20)
    rule_title = pygame.font.SysFont('comicsans',18)

    run = True
    click = False
    while run:
        title_label = title.render("Welcome, to the Starwars Dogfight game, press the mouse to continue!",1,(255,255,255))
        WIN.blit(title_label,(WIDTH/2 - title_label.get_width()/2,250))
        rule_title_label = rule_title.render("WASD for the player on the left with X to shoot, arrow keys for player on the right with M to shoot!",1,(255,255,255))
        WIN.blit(rule_title_label,(WIDTH/1.98 - rule_title_label.get_width()/2,350))

        pygame.display.update()
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

def game():
    running = True
    while running:

        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()


def main():
    global winner_text
    red = pygame.Rect(700, 300, SHIP_WIDTH, SHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SHIP_WIDTH, SHIP_HEIGHT)

    yellow_bullets = []
    red_bullets = []

    red_health = 10
    yellow_health = 10


    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #when x in top right is pressed window is closed
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height //2 -2,10,5) #height/2 to put it in the middle of the ship, width of bullet = 10, height = 5
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_m and len(red_bullets)< MAX_BULLETS:
                    bullet = pygame.Rect(red.x , red.y + red.height // 2 - 2, 10,5)  # height/2 to put it in the middle of the ship, width of bullet = 10, height = 5
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -=1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -=1
                BULLET_HIT_SOUND.play()


        winner_text = ""
        if red_health <=0:
            winner_text = "Yellow wins!"

        if yellow_health <=0:
            winner_text = "Red Wins!"

        if winner_text != "": #if it doesnt equal an empty string, someone has won
            draw_winner(winner_text)
            break



        keys_pressed = pygame.key.get_pressed()
        yellow_movement(keys_pressed, yellow)
        red_movement(keys_pressed, red)

        handle_bullets(yellow_bullets,red_bullets, yellow , red)







        draw_window(red,yellow, red_bullets, yellow_bullets, red_health, yellow_health)

    pygame.quit()




if __name__ == "__main__": #only runs main function if you run the file directly
    MainMenu()