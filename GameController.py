# Jason Zareski
# PyGame Example

import pygame
from random import *

#Initialize pygame
pygame.init()

HEIGHT = 600
WIDTH = 800

SHOT_WIDTH = 2
PLAYER_OBJ_WIDTH = 10

screen = pygame.display.set_mode((WIDTH, HEIGHT))
default_font = pygame.font.SysFont("monospace", 14)

# COLOR CONSTANTS
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)
BLUE     = (   0,   0, 255)

# Sprite speeds
player_speed = 3
proj_speed = 6

def show_fps(clock):
    frames = clock.get_fps()
    frames_label = default_font.render("%d FPS" % frames, 1, GREEN)
    screen.blit(frames_label, (30, 30))

def show_lives(lives):
    lives_label = default_font.render("%d LIVES" % lives, 1, RED)
    screen.blit(lives_label, (30, 50))

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

def move_player(moves, x, y):
    if moves[2]:
        x = x - player_speed
    if moves[3]:
        x = x + player_speed
    if moves[0]:
        y = y - player_speed
    if moves[1]:
        y = y + player_speed
    return (moves, x, y)

def filter_shots(live_shots):
    for a in live_shots:
        a[2] = a[2]-1
        if a[2] <= 0 or a[1] <= 0:
            live_shots.remove(a)
    return live_shots

def player_movement_key_press(e, moves):
    if e.key == pygame.K_a:
        moves[2] = True
    if e.key == pygame.K_d:
        moves[3] = True
    if e.key == pygame.K_w:
        moves[0] = True
    if e.key == pygame.K_s:
        moves[1] = True

    return moves

def player_movement_key_release(e, moves):
    if e.key == pygame.K_a:
        moves[2] = False
    if e.key == pygame.K_d:
        moves[3] = False
    if e.key == pygame.K_w:
        moves[0] = False
    if e.key == pygame.K_s:
        moves[1] = False
    
    return moves

def asteroid_limit(a):
    if a[1] + a[2] > HEIGHT:
        return False
    return True

# astrs: from asteroids list
# live_shots: from shots list
def detect_collisions(px, py, astrs, live_shots, lives):
    asteroids_p1 = list()
    asteroids_p2 = list()

    #Shot collisions with asteroids
    for a in astrs:
        destroyed = False
        for shot in live_shots:
            dist = ((shot[0] - a[0])**2 + (shot[1] - a[1])**2)**(1/2)
            if dist <= SHOT_WIDTH + a[2]:
                destroyed = True
        if not destroyed:
            asteroids_p1.append(a)


    #Player collisions with asteroids (shots take priority in frame by frame)
    for a in asteroids_p1:
        #a: [ax, ay, ar]
        dist = ((px - a[0])**2 + (py - a[1])**2)**(1/2)
        if dist <= PLAYER_OBJ_WIDTH + a[2]:
            lives = lives - 1
        else:
            #add to new array of asteroids
            asteroids_p2.append(a)	
    
    return asteroids_p2, lives, live_shots

def run_game():
    # Game lives for player
    lives = 3

    # Set window size
    pygame.display.set_caption("PYGAME WINDOW")
    
    # game ticks
    clock = pygame.time.Clock()
    time = pygame.time
    # initialize player start pos
    x = 390
    y = 550

    start_time = time.get_ticks()
    end_game = False
    # UP, DOWN, LEFT, RIGHT flags
    moves = [False, False, False, False]

    # [[Asteroid-x, Asteroid-y, Asteroid-radius], ...]
    asteroids = list()

    # [ (x, y, lifetime) ]
    shots = []
    while not end_game:
        # Fill black screen every frame, redraw after.
        screen.fill(BLACK)

        #Generate asteroids
        while len(asteroids) < 40:
            ax = randrange(WIDTH)
            ay = -1 * randrange(HEIGHT)
            ar = randrange(5, 15)
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

                    moves =	player_movement_key_press(e, moves)
                    #Add shooting mechanic
                    if e.key == pygame.K_SPACE:
                        shots.insert(0, [x, y, 80])
                if e.type == pygame.KEYUP: #button press
                    moves = player_movement_key_release(e, moves)

        moves, x, y = move_player(moves, x, y)
        x, y = limit_player_movement(x, y)

        # Move asteroids down y plane
        for a in asteroids:
            a[1] = a[1] + proj_speed
        asteroids = list(filter(asteroid_limit, asteroids))
        asteroids, lives, shots = detect_collisions(x, y, asteroids, shots, lives)

        for a in asteroids:
            pygame.draw.circle(screen, WHITE, (a[0], a[1]), a[2], a[2])
        filter_shots(shots)
        for s in shots:
            pygame.draw.circle(screen, RED, (s[0], s[1]), SHOT_WIDTH, SHOT_WIDTH)
            s[1] = s[1] - proj_speed

        pygame.draw.polygon(screen, BLUE, [[x, y], [x - PLAYER_OBJ_WIDTH, y + PLAYER_OBJ_WIDTH], [x + PLAYER_OBJ_WIDTH, y + PLAYER_OBJ_WIDTH]], 2)

        show_fps(clock)
        show_lives(lives)

        if lives <= 0:
            end_game = True
        pygame.display.flip() #draws new frame over previous frame
        clock.tick(60)

        if end_game:
            # Calculate survival time using ticks, make score.
            end_time = time.get_ticks()
            score = (end_time - start_time) // 100
            score_label = default_font.render("GAME OVER.    Final Score: %d    Press P to play again." % score, 1, RED)
            screen.blit(score_label, (WIDTH * .3, HEIGHT * .4))
            print("Scored: ", score)
            pygame.display.flip()
            # Prompt for restart or quit
            response = False
            while not response:
                for e in pygame.event.get():
                    if e.type == pygame.KEYUP:
                        if e.key == pygame.K_ESCAPE:
                            response = True
                            print("Thanks for playing!")
                            pygame.quit()
                        elif e.key == pygame.K_p:
                            response = True
                            print("Playing again.")
                            run_game()

run_game()
