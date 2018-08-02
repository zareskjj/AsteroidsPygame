# Jason Zareski
# PyGame Example

import pygame
from random import *
#Initialize pygame
pygame.init()

# WINDOW CONSTANTS
HEIGHT = 600
WIDTH = 800

# Set window size
window_size = (WIDTH, HEIGHT)

# COLOR CONSTANTS
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)
BLUE     = (   0,   0, 255)

screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("PYGAME WINDOW")
default_font = pygame.font.SysFont("monospace", 14)

# Game over flag
end_game = False
# game ticks
clock = pygame.time.Clock()

# initialize player start pos
x = 390
y = 550

# Sprite speeds
player_speed = 4
proj_speed = 8

# UP, DOWN, LEFT, RIGHT flags
moves = [False, False, False, False]

shots = [] # [ (x, y, lifetime) ]

def show_fps():
    frames = clock.get_fps()
    frames_label = default_font.render("%d FPS" % frames, 1, GREEN)
    screen.blit(frames_label, (30, 30))

def limit_player_movement(x, y):
    if x > WIDTH - 15:
        x = WIDTH - 15
    if x < 5:
        x = 5
    if y > HEIGHT - 15:
        y = HEIGHT - 15
    if y < 5:
        y = 5
    return (x, y)

def move_player(x, y):
    if moves[2]:
        x = x - player_speed
    if moves[3]:
        x = x + player_speed
    if moves[0]:
        y = y - player_speed
    if moves[1]:
        y = y + player_speed
    return (x, y)

def filter_shots(live_shots):
    for a in live_shots:
        a[2] = a[2]-1
        if a[2] <= 0 or a[1] <= 0:
            live_shots.remove(a)
    return live_shots

def player_movement_key_press(e):
    if e.key == pygame.K_a:
        moves[2] = True
    if e.key == pygame.K_d:
        moves[3] = True
    if e.key == pygame.K_w:
        moves[0] = True
    if e.key == pygame.K_s:
        moves[1] = True

def player_movement_key_release(e):
    if e.key == pygame.K_a:
        moves[2] = False
    if e.key == pygame.K_d:
        moves[3] = False
    if e.key == pygame.K_w:
        moves[0] = False
    if e.key == pygame.K_s:
        moves[1] = False

def asteroid_limit(a):
    if a[1] + a[2] > HEIGHT:
        return False
    return True

# [[Asteroid-x, Asteroid-y, Asteroid-type], ...]
asteroids = list()

while not end_game:
    # Fill black screen every frame, redraw after.
    screen.fill(BLACK)

    #Generate asteroids
    while len(asteroids) < 40:
        ax = randrange(WIDTH)
        ay = -1 * randrange(HEIGHT)
        ar = randrange(0, 10)
        asteroids.append([ax, ay, ar])

    # For all events in pygame window at this frame
    for e in pygame.event.get():
        if e.type is not pygame.NOEVENT:
            # Quit event (window quit?)
            if e.type == pygame.QUIT:
                end_game = True
            # Button Pressed event
            if e.type == pygame.KEYDOWN:
                #Exit game on pressing ESC
                if e.key == pygame.K_ESCAPE:
                    end_game = True

                player_movement_key_press(e)
                #Add shooting mechanic
                if e.key == pygame.K_SPACE:
                    shots.insert(0, [x, y, 80])
            if e.type == pygame.KEYUP: #button press
                player_movement_key_release(e)

    x, y = move_player(x, y)
    x, y = limit_player_movement(x, y)

    # Move asteroids down y plane
    for a in asteroids:
        a[1] = a[1] + proj_speed
    asteroids = list(filter(asteroid_limit, asteroids))

    for a in asteroids:
        pygame.draw.circle(screen, WHITE, (a[0], a[1]), a[2], a[2])
    #shots = filter_shots(shots)
    filter_shots(shots)
    for s in shots:
        pygame.draw.circle(screen, RED, (s[0], s[1]), 2, 2)
        s[1] = s[1] - proj_speed

    p1 = pygame.draw.polygon(screen, BLUE, [[x, y], [x - 10, y + 10], [x + 10, y + 10]], 2)

    show_fps()
    pygame.display.flip() #draws new frame over previous frame
    clock.tick(60)

pygame.quit()
