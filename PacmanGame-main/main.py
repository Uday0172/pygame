import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) # This sets the width and height of the window
pygame.display.set_caption("Rowdy Game") # This is the name of the game

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)

BORDER = pygame.Rect(0, HEIGHT//2 - 5, WIDTH, 10) # This is what makes the border horizontal instead of vertical


BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('assets', 'hit.mp3' ))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('assets','ult.mp3' ))

HEALTH_FONT = pygame.font.SysFont('dejavusansmono', 40) # this is the different font I used 
WINNER_FONT = pygame.font.SysFont('dejavusansmono', 100)

FPS = 60
BULLET_VEL = 7
MAX_BULLETS = 10 # This is how many bullets the pacman can shoot, its more fair if its only 10 bullets so nobody spams
VEL = 5

YELLOW_HIT = pygame.USEREVENT + 1
BLACK_HIT = pygame.USEREVENT + 2

YELLOW_PACMAN_IMAGE = pygame.image.load(os.path.join('Assets', 'pacman_yellow.png')) #pacman images
YELLOW_PACMAN = pygame.transform.rotate(pygame.transform.scale(YELLOW_PACMAN_IMAGE, (100, 100)), 0) #rotation of images


BLACK_PACMAN_IMAGE = pygame.image.load(os.path.join('Assets', 'pacman_black.png')) # same as above
BLACK_PACMAN = pygame.transform.rotate(pygame.transform.scale(BLACK_PACMAN_IMAGE, (100, 100)), 180)

BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'background.png')), (WIDTH, HEIGHT))

def draw_window(yellow, black, black_bullets, yellow_bullets, black_health, yellow_health):
    WIN.fill(BLUE)
    WIN.blit(BACKGROUND, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER) # this adds the border
    black_health_text = HEALTH_FONT.render("Health: " + str(black_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
    WIN.blit(black_health_text, (WIDTH - black_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, HEIGHT - yellow_health_text.get_height()- 10,)) # this moves the health text on opposite sides


    WIN.blit(YELLOW_PACMAN, (yellow.x, yellow.y))
    WIN.blit(BLACK_PACMAN, (black.x, black.y))

    for bullet in black_bullets:
        pygame.draw.rect(WIN, BLACK, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()

#controls
def black_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:  # LEFT
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + 70 < WIDTH : # RIGHT
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:  # UP
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y - VEL < BORDER.y - 70:  # DOWN
        yellow.y += VEL


def yellow_handle_movement(keys_pressed, black):
    if keys_pressed[pygame.K_LEFT] and black.x - VEL > 0 :   # LEFT
        black.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and black.x + VEL + 70 < WIDTH:  # RIGHT
        black.x += VEL
    if keys_pressed[pygame.K_UP] and black.y + VEL > BORDER.y - 15:  # UP
        black.y -= VEL
    if keys_pressed[pygame.K_DOWN] and black.y + VEL + 95 < HEIGHT:  # DOWN
        black.y += VEL


def handle_bullets(yellow_bullets, black_bullets, yellow, black):
    for bullet in yellow_bullets:
        bullet.y -= BULLET_VEL
        if black.colliderect(bullet):
            pygame.event.post(pygame.event.Event(BLACK_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.y > HEIGHT:
            yellow_bullets.remove(bullet)

    for bullet in black_bullets:
        bullet.y += BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            black_bullets.remove(bullet)
        elif bullet.y < 0:
            black_bullets.remove(bullet)


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    black = pygame.Rect(600, 50, 70, 75)
    yellow = pygame.Rect(600, 550, 135, 80)

    black_bullets = []
    yellow_bullets = []

    black_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            # controls for shooting and code
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width//2, yellow.y + yellow.height - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_LCTRL and len(black_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(black.x + 40, black.y + 30 - 2, 10, 5)
                    black_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == BLACK_HIT:
                black_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""
        if black_health <= 0:
            winner_text = "Blck-Pacman Wins!" #if black pacman wins

        if yellow_health <= 0:
            winner_text = "Ylow-Pacman Wins!" #if yellow pacman wins

        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        black_handle_movement(keys_pressed, black)

        handle_bullets(yellow_bullets, black_bullets, yellow, black)



        draw_window(black, yellow, black_bullets, yellow_bullets,
                    black_health, yellow_health)

    main()
#loop

if __name__ == "__main__":
    main()