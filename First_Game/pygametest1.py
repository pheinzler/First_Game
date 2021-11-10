import pygame
import os 
pygame.font.init() #initalise font library
pygame.mixer.init() #init Audio

#Video at 1:16:03 https://www.youtube.com/watch?v=jO6qQDNa2UY&list=PLzMcBGfZo4-kNEPqSOaglnUZz3D2R4OzY&index=3

WIDTH, HEIGHT = 900,500
WIN = pygame.display.set_mode((WIDTH,HEIGHT))   #new window with given width and height
pygame.display.set_caption('FirstGame') #Game Title (Anzeige neben Quit und miniaturansicht)

#colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

#other variables
FPS = 60
BORDER = pygame.Rect(WIDTH//2-3, 0 ,6,HEIGHT) #pos of border (middle/0) width of border 10 height = HEIGHT
SPACESHIP_WIDTH , SPACESHIP_HEIGHT = (55,40)
VELOCITY = 3
BULLETS_VELOCITY = 6
MAX_BULLETS = 5

#Fonts
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 60)

#Sounds
BULLET_HIT_SOUND = pygame.mixer.music.load(os.path.join('Assets' , 'Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.music.load(os.path.join('Assets' , 'Gun+Silencer.mp3'))

#events
YELLOW_HIT = pygame.USEREVENT + 1   #creats own user events +x for unique own event number
RED_HIT = pygame.USEREVENT + 2

#pictures
YELLOW_SPACE_SHIP_IMAGE = pygame.image.load(os.path.join('Assets','spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACE_SHIP_IMAGE,(SPACESHIP_WIDTH,SPACESHIP_HEIGHT)), 90) #scale Spaceship ändern
RED_SPACE_SHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACE_SHIP_IMAGE,(SPACESHIP_WIDTH,SPACESHIP_HEIGHT)), 270)
SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets','space.png')), (WIDTH,HEIGHT))

def draw_window(red , yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    #WIN.fill(WHITE) #White Background
    WIN.blit(SPACE, (0,0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1 , RED)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health) , 1 , YELLOW)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    WIN.blit(YELLOW_SPACESHIP,(yellow.x,yellow.y))    #blit() draw surfce on screen
    WIN.blit(RED_SPACESHIP,(red.x , red.y) )

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()

def draw_winner(text):
    
    if text =='YELLOW wins!':
        WIN.fill(YELLOW)
    else: 
        WIN.fill(RED)
        
    draw_winner_text = WINNER_FONT.render(text,1, BLACK)
    WIN.blit(draw_winner_text, (WIDTH//2 - draw_winner_text.get_width()//2 , HEIGHT//2 - draw_winner_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(3000)

def yellow_handlemovement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VELOCITY >= 0: #left
        yellow.x -= VELOCITY
    if keys_pressed[pygame.K_d] and yellow.x + VELOCITY + yellow.width<= BORDER.x: #right
        yellow.x += VELOCITY
    if keys_pressed[pygame.K_w] and yellow.y - VELOCITY>= 0: #up
        yellow.y -= VELOCITY
    if keys_pressed[pygame.K_s] and yellow.y + VELOCITY + yellow.height <= HEIGHT - 15: #down -15 unexplaineble offsett
        yellow.y += VELOCITY

def red_handlemovement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x + VELOCITY >= BORDER.x + BORDER.width: #left
        red.x -= VELOCITY
    if keys_pressed[pygame.K_RIGHT] and red.x + VELOCITY + red.width<= WIDTH: #right
        red.x += VELOCITY
    if keys_pressed[pygame.K_UP]and red.y - VELOCITY>= 0: #up
        red.y -= VELOCITY
    if keys_pressed[pygame.K_DOWN] and red.y + VELOCITY + red.height <= HEIGHT - 15: #down
        red.y += VELOCITY

def handle_bullets(yellow_bullets, yellow, red_bullets, red):
    for bullet in yellow_bullets:
        bullet.x += BULLETS_VELOCITY
        if red.colliderect(bullet): #checks for Bullet and ship collinsion --> Rect collision #yellow bullets hitting red character
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)       
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    #handles red bullets
    for bullet in red_bullets:
        bullet.x -= BULLETS_VELOCITY
        if yellow.colliderect(bullet): #checks for Bullet and ship collinsion --> Rect collision #yellow bullets hitting red character
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)       
        elif bullet.x < 0:
            red_bullets.remove(bullet)
def main(): #handle main game loop
    red = pygame.Rect(700,300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)   #represent spaceships as rectangles (pos_x , pos_y , width, height)
    yellow = pygame.Rect(100,300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    
    red_bullets = []
    yellow_bullets = []

    red_health = 6
    yellow_health = 6

    clock = pygame.time.Clock() 
    run = True

    while run:   #Game loop
        clock.tick(FPS)#control speed of while loop
        for event in pygame.event.get(): #handle possible income events list of all the different events
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect((yellow.x+yellow.width), (yellow.y + yellow.height//2 - 2), 8 , 4)
                    yellow_bullets.append(bullet)
                    #BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_l and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect((red.x), (red.y + red.height//2 - 2), 8 , 4)
                    red_bullets.append(bullet)
                    #BULLET_FIRE_SOUND.play()
            
            if event.type == RED_HIT:
                red_health -= 1
            if event.type == YELLOW_HIT:
                yellow_health -= 1
        winner_text = ''

        if red_health <= 0:
            winner_text = 'YELLOW wins!'
            #BULLET_HIT_SOUND
        if yellow_health <= 0:
            winner_text = 'RED wins!'
            #BULLET_HIT_SOUND.play()
        
        if winner_text != '':
            draw_winner(winner_text)
            break # game over --> pygame.quit()

        keys_pressed = pygame.key.get_pressed() #key pressed methode wenn mehrere controls gleichzeitig
        yellow_handlemovement(keys_pressed, yellow)
        red_handlemovement(keys_pressed,red)
        handle_bullets(yellow_bullets, yellow, red_bullets, red)
        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)
    
    main() #nicht mehr pygame.quit --> restart automatisch -->pygame.quit jetzt bei run = False
    #pygame.quit()   

if __name__ == '__main__':
    main()