import asyncio
import pygame
import os

from random import randint

pygame.mixer.init()
pygame.font.init()
pygame.init()

WIDTH = 900
HEIGHT = 600

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("epic game")
pygame.display.set_icon(pygame.image.load(os.path.join('assets', 'muis.jpeg')))

MAX_VEL = 10
MIN_VEL = -10

SCORE_FONT = pygame.font.SysFont('comicsans', 50)

MOUSE = pygame.image.load(os.path.join('assets', 'muis.jpeg'))
MOUSE = pygame.transform.scale(MOUSE, (50, 50))

BANANA = pygame.image.load(os.path.join('assets', 'Banana-Single.jpg'))
BANANA = pygame.transform.scale(BANANA, (50, 50))

BG = pygame.image.load(os.path.join('assets', 'bg.jpg'))
BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))

BIRD = pygame.image.load(os.path.join('assets', 'bird.jpg'))
BIRD = pygame.transform.scale(BIRD, (50, 50))

def draw_screen(mouse, bananas, birds, score):
    WIN.blit(BG, (0, 0))
    WIN.blit(MOUSE, (mouse.x, mouse.y))

    for banana in bananas:
        WIN.blit(BANANA, (banana.x, banana.y))

    for bird in birds:
        WIN.blit(BIRD, (bird.x, bird.y))

    score_text = SCORE_FONT.render(f"Score: {score}", 1, (255, 255, 255))
    WIN.blit(score_text, (WIDTH - score_text.get_width() - 10, 10))

    pygame.display.update()

def handle_input(mouse, vel_x, vel_y):
    keys_pressed = pygame.key.get_pressed()

    if keys_pressed[pygame.K_d] and mouse.x < WIDTH - mouse.width:
        vel_x += 3
    if keys_pressed[pygame.K_a] and mouse.x > 0 + mouse.width:
        vel_x -= 3
    if keys_pressed[pygame.K_s]:
        vel_y += 3
    if keys_pressed[pygame.K_w]:
        vel_y -= 3

    return vel_x, vel_y

def handle_movement(mouse, vel_x, vel_y):

    # Move horizontally based on velocity
    # while not exceeding min or max velocity
    if MAX_VEL > vel_x > MIN_VEL:
        mouse.x += vel_x
    elif vel_x < MIN_VEL:
        mouse.x += MIN_VEL
    else:
        mouse.x += MAX_VEL

    # Move vertically based on velocity
    # while not exceeding min or max velocity
    if MAX_VEL > vel_y > MIN_VEL:
        mouse.y += vel_y
    elif vel_y < MIN_VEL:
        mouse.y += MIN_VEL
    else:
        mouse.y += MAX_VEL

    # Degrade horizontal velocity every iteration
    if vel_x > 0:
        vel_x -= 1
    elif vel_x < 0:
        vel_x += 1

    # Degrade vertical velocity every iteration
    if vel_y > 0:
        vel_y -= 1
    elif vel_y < 0:
        vel_y += 1

    # Prevent mouse from going past edges of screen
    if mouse.x > WIDTH:
        mouse.x = WIDTH - mouse.width
        vel_x = 0

    if mouse.x < 0:
        mouse.x = 0
        vel_x = 0

    if mouse.y > HEIGHT:
        mouse.y = HEIGHT - mouse.height
        vel_y = 0

    if mouse.y < 0:
        mouse.y = 0
        vel_y = 0

    return mouse, vel_x, vel_y

def timed_rect_adding(timer, rect_list, frame_count):
    timer += 1

    if timer == frame_count:
        rect_list.append(pygame.Rect(randint(0, WIDTH - 50), randint(0, HEIGHT - 50), 50, 50))
        timer = 0

    return timer, rect_list

async def game_loop():
    clock = pygame.time.Clock()
    mouse = pygame.Rect(0, 0, 50, 50)
    vel_x = 0
    vel_y = 0

    bananas = []
    banana_make_timer = 0

    birds = []
    bird_make_timer = 0

    score = 0

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return 'QUIT'

        vel_x, vel_y = handle_input(mouse, vel_x, vel_y)

        mouse, vel_x, vel_y = handle_movement(mouse, vel_x, vel_y)

        banana_make_timer, bananas = timed_rect_adding(banana_make_timer, bananas, 180)
        bird_make_timer, birds = timed_rect_adding(bird_make_timer, birds, 180)

        for banana in bananas:
            if mouse.colliderect(banana):
                bananas.remove(banana)
                score += 1

        for bird in birds:
            if mouse.colliderect(bird):
                await asyncio.sleep(3)
                return 'DEATH'

        draw_screen(mouse, bananas, birds, score)

        await asyncio.sleep(0)

async def main():
    while True:
        result = await game_loop()

        if result == 'QUIT':
            break;

asyncio.run(main())