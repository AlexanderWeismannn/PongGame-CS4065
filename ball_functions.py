import pygame, sys, random
from pygame.locals import *

def ball_animation(ball, player1, player2, ball_speed_x, ball_speed_y, p1_score, p2_score, score_time, SCREEN_SIZE):

    #collision logic
    if ball.top <= 0 or ball.bottom >= SCREEN_SIZE[1]:
        #negatively reverse the ball speed (i.e. cause it to bounce)
        ball_speed_y *= -1

    #P2 scores a goal
    if ball.left <= 0:
        p2_score += 1
        score_time = pygame.time.get_ticks()

    #P1 scores a goal
    if ball.right >= SCREEN_SIZE[0]:
        p1_score += 1
        score_time = pygame.time.get_ticks()

    #paddle Collison
    #Voodoo magic causes this to work, dont ask me to explain it plz :)#

    if ball.colliderect(player1) and ball_speed_x < 0:
        if abs(ball.left - player1.right) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - player1.top) < 10 and ball_speed_y > 10:
                ball_speed_y *= -1
        elif abs(ball.top - player1.bottom) < 10 and ball_speed_y < 10:
                ball_speed_y *= -1

    if ball.colliderect(player2) and ball_speed_x > 0:
        if abs(ball.right - player2.left) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - player2.top) < 10 and ball_speed_y > 10:
            ball_speed_y *= -1
        elif abs(ball.top - player2.bottom) < 10 and ball_speed_y < 10:
            ball_speed_y *= -1

    return ball_speed_x, ball_speed_y, p1_score, p2_score, score_time

def ball_reset(display, ball, ball_speed_x, ball_speed_y, score_time, TEXT_FONT, SCREEN_SIZE, WHITE):
    current_time = pygame.time.get_ticks()
    ball.center = (SCREEN_SIZE[0]/2, SCREEN_SIZE[1]/2)

    if(current_time - score_time < 700):
        display.blit(TEXT_FONT.render("3", True, WHITE), (SCREEN_SIZE[0]/2 - 10, SCREEN_SIZE[1]/2 + 30))

    if 700 < (current_time - score_time) < 1400:
        display.blit(TEXT_FONT.render("2", True, WHITE), (SCREEN_SIZE[0]/2 - 10, SCREEN_SIZE[1]/2 + 30))

    if 1400 < (current_time - score_time) < 2100:
        display.blit(TEXT_FONT.render("1", True, WHITE), (SCREEN_SIZE[0]/2 - 10, SCREEN_SIZE[1]/2 + 30))

    #creates a 2.1 second delay where the ball speed = 0 before setting it back to the normal X and Y speeds
    if(current_time - score_time < 2100):
        ball_speed_x, ball_speed_y = 0,0
    else:
        ball_speed_x, ball_speed_y = 7 * random.choice((1,-1)),7 * random.choice((1,-1))
        score_time = None

    return ball_speed_x, ball_speed_y, score_time
