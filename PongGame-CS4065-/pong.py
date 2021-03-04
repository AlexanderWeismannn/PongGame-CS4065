import pygame, sys, random
from pygame.locals import *
from ball_functions import ball_animation, ball_reset
from player_functions import player_animation, user_input
from particles import particle_animation


# Initialize pygame
pygame.init()

# UI settings
SCREEN_SIZE = [1600, 900]
SCREEN_CAPTION = "Pong"
CENTER_RADIUS = 25

# Geometry settings
BALL_RADIUS = 15
PADDLE_SIZE = [10, 120]

# Colors
BG_COLOR = pygame.Color("gray12")
WHITE = pygame.Color("gray100")
GREY = pygame.Color("gray71")

# Game settings
GAME_SPEED = 80
score_time = True
speed_constant = 8
speed_mult = 0.5
ball_speed_x = speed_constant * random.choice((1,-1))
ball_speed_y = speed_constant * random.choice((1,-1))
p1_speed, p2_speed, p1_score, p2_score = 0, 0, 0, 0
TEXT_FONT = pygame.font.Font("freesansbold.ttf", 32)
player1_text = TEXT_FONT.render(f"{p1_score}", True, WHITE)
player2_text = TEXT_FONT.render(f"{p2_score}", True, WHITE)

#Particles
particles = []


# Pygame config
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


def game_loop(ball, player1, player2, center):
    global p1_speed, p2_speed, p1_score, p2_score, ball_speed_x, ball_speed_y, score_time, WHITE, speed_mult
    while True:

        p1_speed = user_input(p1_speed)
        player1.y += p1_speed

        #ai speed(WARNING: DO NOT GO PAST 8! ITS THE NUMBER OF THE BEAST. I SERIOUSLY CAN'T BEAT IT ONCE AT 8. AT 8 IT CAN PERFECTLY COVER THE ENTIRE GOAL)
        p2_speed = 7.99
        #ai position method
        opponent_ai()
        
       

        player_positions = player_animation(player1, player2, SCREEN_SIZE)
        if player_positions[0] != -1:
            player1.top = player_positions[0]
        if player_positions[1] != -1:
            player1.bottom = player_positions[1]

        ball_speed_x, ball_speed_y, p1_score, p2_score, score_time = ball_animation(ball, player1, player2, ball_speed_x, ball_speed_y, p1_score, p2_score, score_time, SCREEN_SIZE, speed_mult)
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
        particle_animation(display,ball,particles)
        
    
        # the ball has collided with the left/right side of the screen
        if score_time:
            ball_speed_x, ball_speed_y, score_time = ball_reset(display, ball, ball_speed_x, ball_speed_y, score_time, TEXT_FONT, SCREEN_SIZE, WHITE, speed_constant)

        player1_text = TEXT_FONT.render(f"{p1_score}", True, WHITE)
        player2_text = TEXT_FONT.render(f"{p2_score}", True, WHITE)
        display.blit(player1_text,(735,470))
        display.blit(player2_text,(850,470))

        #updating the window
        pygame.display.update()
        clock.tick(GAME_SPEED)

if __name__ == "__main__":

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

    game_loop(ball, player1, player2, center)
  
