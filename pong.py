import pygame, sys, random
from pygame.locals import *
from ball_functions import ball_animation, ball_reset
from player_functions import player_animation, user_input
from particles import *


"""
Potential idea:
Advantage scales from Level 1 advantage to level 3
Level 1: Paddle can get 20% larger
Level 2: Paddle can get 40% larger
Level 3: Paddle can get 60% larger

This way we're measuring both the effect of the advantage, as well as how far
the advantage can be pushed before the player notices.
"""

# Initialize pygame
pygame.init()
STARTING = True

# UI settings
SCREEN_SIZE = [1600, 900]
SCREEN_CAPTION = "Pong"
CENTER_RADIUS = 25

# Geometry settings
BALL_RADIUS = 15
PADDLE_SIZE = [25, 120]

# Colors
BG_COLOR = pygame.Color("gray12")
WHITE = pygame.Color("gray100")
GREY = pygame.Color("gray71")
BLACK = pygame.Color("black")

# Data Collection
current_set = 1 # Implemented
player_set_wins = 0 # Implemented
player_round_wins = 0 # Implemented

# TODO: Currently this is vollies / returns per set, not round. Must change to round
number_of_vollies = 0 # Implemented
player_returns = 0 # Implemented

# Game settings
Advantage_level = 0
GAME_SPEED = 80
score_per_round = 1
score_time = True
speed_constant = 8
speed_mult = 1.000001
ball_speed_x = speed_constant * random.choice((1,-1))
ball_speed_y = speed_constant * random.choice((1,-1))
p1_speed, p2_speed, p1_score, p2_score = 0, 0, 0, 0
TEXT_FONT = pygame.font.Font("freesansbold.ttf", 32)
player1_text = TEXT_FONT.render(f"{p1_score}", True, WHITE)
player2_text = TEXT_FONT.render(f"{p2_score}", True, WHITE)

#Particles
particles = []
paddle_particles = []

#Pygame config
clock = pygame.time.Clock()
display = pygame.display.set_mode((SCREEN_SIZE[0], SCREEN_SIZE[1]))
pygame.display.set_caption(SCREEN_CAPTION)


def opponent_ai():
    if player2.center[1] < ball.center[1]:
        center = list(player2.center)
        center[1] += p2_speed
        player2.center = center
    elif player2.center[1] > ball.center[1]:
        center = list(player2.center)
        center[1] -= p2_speed
        player2.center = center
    if player2.top <= 0:
        player2.top = 0
    if player2.bottom >= SCREEN_SIZE[1]:
        player2.bottom = SCREEN_SIZE[1]


def start_screen():
    print("IN START SCREEN")
    intro_img = pygame.image.load("introduction.png")
    while True:

        #Draw visuals
        display.fill(BLACK)
        intro_text = TEXT_FONT.render("WELCOME TO OUR EXPERIMENT!", True, WHITE)
        intro_text_2 = TEXT_FONT.render("please read the instructions below carefully", True, WHITE)
        display.blit(intro_text,[SCREEN_SIZE[0] * 0.35, SCREEN_SIZE[1] * 0.15])
        display.blit(intro_text_2,[SCREEN_SIZE[0]/2 * 0.60, SCREEN_SIZE[1] * 0.25 ])
        display.blit(intro_img, [SCREEN_SIZE[0] * 0.26, SCREEN_SIZE[1] * 0.35] )

        #updating the window
        pygame.display.flip()
        clock.tick(GAME_SPEED)



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                #makes sure that the player can only hit enter and doesnt allow for other keys to be pressed at the same time
                #originally the value goes outside of the screen space and breaks player control if held before movement is allowed.
                if event.key == pygame.K_RETURN and (pygame.key.get_pressed()[K_w] == False) and (pygame.key.get_pressed()[K_s] == False):
                    game_loop(ball,player1,player2,center)


def pause_screen():
    global player_returns, p1_speed, number_of_vollies, current_set, player_round_wins, player_set_wins, player1

  

    # Reset player
    player1.height = PADDLE_SIZE[1]

    print("IN PAUSE SCREEN")
    print(f"Advantage Level: {Advantage_level}")
    print(f"Finished set: {current_set}")
    print(f"Player return count for previous round: {player_returns}")
    print(f"Volley count: {number_of_vollies}")
    print(f"Rounds won by player: {player_round_wins}")
    print(f"Did player win the set? {player_round_wins >= score_per_round}")

    if player_round_wins >= score_per_round:
        player_set_wins += 1

    print(f"Total sets won by player: {player_set_wins}")

    p1_speed = 0
    current_set += 1
    player_returns = 0
    number_of_vollies = 0
    player_round_wins = 0

    display.fill(BLACK)
    pause_text = TEXT_FONT.render("BREAK SCREEN", True, WHITE)
    pause_text_2 = TEXT_FONT.render("press [ENTER] to continue when ready", True, WHITE)
    display.blit(pause_text,[SCREEN_SIZE[0] * 0.42, SCREEN_SIZE[1] * 0.15])
    display.blit(pause_text_2,[SCREEN_SIZE[0] * 0.31, SCREEN_SIZE[1] * 0.25 ])

    while True:

        #updating the window
        pygame.display.flip()
        clock.tick(GAME_SPEED)

        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and (pygame.key.get_pressed()[K_w] == False) and (pygame.key.get_pressed()[K_s] == False):
                        pygame.event.clear(None)
                        return

def end_screen():
    global player_returns, p1_speed, number_of_vollies, current_set, player_round_wins, player_set_wins, player1

    # Reset player
    player1.height = PADDLE_SIZE[1]

    print("IN END SCREEN")
    print(f"Finished set: {current_set}")
    print(f"Player return count for previous round: {player_returns}")
    print(f"Volley count: {number_of_vollies}")
    print(f"Rounds won by player: {player_round_wins}")
    print(f"Did player win the set? {player_round_wins >= score_per_round}")

    if player_round_wins >= score_per_round:
        player_set_wins += 1

    print(f"Total sets won by player: {player_set_wins}")

    p1_speed = 0
    current_set += 1
    player_returns = 0
    number_of_vollies = 0
    player_round_wins = 0

    display.fill(BLACK)
    pause_text = TEXT_FONT.render("THE END", True, WHITE)
    pause_text_2 = TEXT_FONT.render("Press [ENTER] to exit", True, WHITE)
    display.blit(pause_text,[SCREEN_SIZE[0] * 0.45, SCREEN_SIZE[1] * 0.15])
    display.blit(pause_text_2,[SCREEN_SIZE[0] * 0.39, SCREEN_SIZE[1] * 0.25 ])

    while True:
        #updating the window
        pygame.display.flip()
        clock.tick(GAME_SPEED)

        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and (pygame.key.get_pressed()[K_w] == False) and (pygame.key.get_pressed()[K_s] == False):
                        pygame.quit()
                        sys.exit()
                        



def game_loop(ball, player1, player2, center):
    global p1_speed, p2_speed, p1_score, p2_score, ball_speed_x, ball_speed_y, score_time, WHITE, speed_mult, STARTING, player_returns, player_round_wins, number_of_vollies, Advantage_level, PADDLE_SIZE
    animate = False
    collision = 0
    if STARTING:
        score_time = pygame.time.get_ticks()
        STARTING = False
    while True:

        p1_speed = user_input(p1_speed)
        player1.y += p1_speed

        #ai speed(WARNING: DO NOT GO PAST 8! ITS THE NUMBER OF THE BEAST. I SERIOUSLY CAN'T BEAT IT ONCE AT 8. AT 8 IT CAN PERFECTLY COVER THE ENTIRE GOAL)
        p2_speed = 7.999
        #ai position method
        opponent_ai()

        player_positions = player_animation(player1, player2, SCREEN_SIZE)
        if player_positions[0] != -1:
            player1.top = player_positions[0]
        if player_positions[1] != -1:
            player1.bottom = player_positions[1]

        ball_speed_x, ball_speed_y, p1_score, p2_score, score_time, collision, player_returns, number_of_vollies, player_round_wins, player1 = ball_animation(collision, ball, player1, player2, ball_speed_x, ball_speed_y, p1_score, p2_score, score_time, SCREEN_SIZE, speed_mult, player_returns, number_of_vollies, player_round_wins, Advantage_level)
        ball.x += ball_speed_x
        ball.y += ball_speed_y

        #Draw visuals
        display.fill(BG_COLOR)

        pygame.draw.aaline(display, WHITE, (SCREEN_SIZE[0]/2, 0),
                            (SCREEN_SIZE[0]/2, SCREEN_SIZE[1]))

        pygame.draw.ellipse(display, GREY, center)
        pygame.draw.rect(display, WHITE, player1)
        pygame.draw.rect(display, WHITE, player2)
        pygame.draw.ellipse(display, WHITE, ball)

        # Particles
        particle_animation(display, ball, collision, particles, animate)
        collision = 0

        # the ball has collided with the left/right side of the screen
        if score_time:
            animate = False
            ball_speed_x, ball_speed_y, score_time, animate, player1 = ball_reset(display, ball, ball_speed_x, ball_speed_y, score_time, TEXT_FONT, SCREEN_SIZE, WHITE, speed_constant, animate, player1, PADDLE_SIZE[1])

        player1_text = TEXT_FONT.render(f"{p1_score}", True, WHITE)
        player2_text = TEXT_FONT.render(f"{p2_score}", True, WHITE)
        display.blit(player1_text,(735,470))
        display.blit(player2_text,(850,470))

        #TEST FOR THE BREAK SCREEN
        if p1_score >= score_per_round or p2_score >= score_per_round:
            p1_score,p2_score = 0,0
            Advantage_level += 1

            if Advantage_level <= 3:
                pause_screen()
            else:
                end_screen()
           
            
            score_time = pygame.time.get_ticks()

        #updating the window
        pygame.display.update()
        clock.tick(GAME_SPEED)


if __name__ == "__main__":

    pygame.mixer.init()
    pygame.mixer.music.load("paddle.mp3")

    # Create the ball and center it
    ball = pygame.Rect(SCREEN_SIZE[0]/2 - BALL_RADIUS,
                       SCREEN_SIZE[1]/2 - BALL_RADIUS,
                       BALL_RADIUS*2, BALL_RADIUS*2)

    # Create the player paddles
    player1 = pygame.Rect(PADDLE_SIZE[0],
                          SCREEN_SIZE[1]/2 - PADDLE_SIZE[1]/2,
                          PADDLE_SIZE[0], PADDLE_SIZE[1])

    player2 = pygame.Rect(SCREEN_SIZE[0] - PADDLE_SIZE[0]*2,
                          SCREEN_SIZE[1]/2 - PADDLE_SIZE[1]/2,
                          PADDLE_SIZE[0], PADDLE_SIZE[1])

    # Create the starting point for the ball
    center = pygame.Rect(SCREEN_SIZE[0]/2 - CENTER_RADIUS,
                         SCREEN_SIZE[1]/2 - CENTER_RADIUS,
                         CENTER_RADIUS*2, CENTER_RADIUS*2)
    #call the start screen first
    start_screen()
