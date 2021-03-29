import pygame, sys, random
from pygame.locals import *
from data.particles import *

def ball_animation(collision, ball, player1, player2, ball_speed_x, ball_speed_y, p1_score, p2_score, score_time, SCREEN_SIZE, speed_mult, player_returns, number_of_vollies, player_round_wins, Advantage_level, game_sounds):

    #collision logic
    if ball.top <= 0 or ball.bottom >= SCREEN_SIZE[1]:
        #negatively reverse the ball speed (i.e. cause it to bounce)
        ball_speed_y *= -1

    #P2 scores a goal
    if ball.left <= -50:
        p2_score += 1
        score_time = pygame.time.get_ticks()

    #P1 scores a goal
    if ball.right >= SCREEN_SIZE[0]+50:
        p1_score += 1
        player_round_wins += 1
        score_time = pygame.time.get_ticks()

    #paddle Collison
    #Voodoo magic causes this to work, dont ask me to explain it plz :)#

    #paddle particles

    previous_collide = 0

    if (previous_collide != -1) and (ball.colliderect(player1) and ball_speed_x < 0):
        player_returns += 1
        number_of_vollies += 1
        game_sounds['paddle_sound'].play()
        collision = -1
        previous_collide = -1
        if (abs((ball.left - player1.right) < 10)) or (abs((ball.right - player1.right) < 10)):
            ball_speed_x -= speed_mult
            ball_speed_x *= -1
        elif abs(ball.bottom - player1.top) < 10 and ball_speed_y > 10:
            ball_speed_y -= speed_mult
            ball_speed_y *= -1
        elif abs(ball.top - player1.bottom) < 10 and ball_speed_y < 10:
            ball_speed_y -= speed_mult
            ball_speed_y *= -1

    if (previous_collide != 1) and (ball.colliderect(player2) and ball_speed_x > 0):

        # WARNING: this must only happen if advantage is set to true
        if (Advantage_level == 1):
            if (player1.height < 144):
                player1.height += 1
        elif (Advantage_level == 2):
            if (player1.height < 168):
                player1.height += 2
        elif (Advantage_level == 3):
            if (player1.height < 192):
                player1.height += 3
            # if (player1.height < 192):
            #     player1.height += 3

        game_sounds['paddle_sound'].play()
        collision = 1
        previous_collide = 1
        number_of_vollies += 1
        if (abs((ball.right - player2.right) < 10)) or (abs((ball.left - player2.right) < 10)):
            ball_speed_x += speed_mult
            ball_speed_x *= -1
        elif abs(ball.bottom - player2.top) < 10 and ball_speed_y > 10:
            ball_speed_y += speed_mult
            ball_speed_y *= -1
        elif abs(ball.top - player2.bottom) < 10 and ball_speed_y < 10:
            ball_speed_y += speed_mult
            ball_speed_y *= -1

    return ball_speed_x, ball_speed_y, p1_score, p2_score, score_time, collision, player_returns, number_of_vollies, player_round_wins, player1

def ball_reset(display, ball, ball_speed_x, ball_speed_y, score_time, TEXT_FONT, SCREEN_SIZE, WHITE, speed_constant, animate, player1, size, p1_score, p2_score, game_sounds, goal_sound):

    goal_font = pygame.font.Font("freesansbold.ttf", 100)

    if (player1.height > size):
        if (player1.height - 10 < size):
            player1.height == size
        else:
            player1.height -= 10

    current_time = pygame.time.get_ticks()
    ball.center = (SCREEN_SIZE[0]/2, SCREEN_SIZE[1]/2)

    if(current_time - score_time < 700):
        #if its the start of the round dont display goal
        if p1_score == 0 and p2_score == 0 :
            display.blit(TEXT_FONT.render("3", True, WHITE), (SCREEN_SIZE[0]/2 - 10, SCREEN_SIZE[1]/2 + 30))
        else:
            display.blit(TEXT_FONT.render("3", True, WHITE), (SCREEN_SIZE[0]/2 - 10, SCREEN_SIZE[1]/2 + 30))
            display.blit(goal_font.render("GOAL!", True, WHITE), (SCREEN_SIZE[0]/2 - 157, SCREEN_SIZE[1]/2 - 150))


    elif 700 < (current_time - score_time) < 1400:
        if p1_score == 0 and p2_score == 0:
            display.blit(TEXT_FONT.render("2", True, WHITE), (SCREEN_SIZE[0]/2 - 10, SCREEN_SIZE[1]/2 + 30))
        else:
            display.blit(TEXT_FONT.render("2", True, WHITE), (SCREEN_SIZE[0]/2 - 10, SCREEN_SIZE[1]/2 + 30))
            display.blit(goal_font.render("GOAL!", True, WHITE), (SCREEN_SIZE[0]/2 - 157, SCREEN_SIZE[1]/2 - 150))

    elif 1400 < (current_time - score_time) < 2100:
        display.blit(TEXT_FONT.render("1", True, WHITE), (SCREEN_SIZE[0]/2 - 10, SCREEN_SIZE[1]/2 + 30))

    #creates a 2.1 second delay where the ball speed = 0 before setting it back to the normal X and Y speeds
    if(current_time - score_time < 2100):
        ball_speed_x, ball_speed_y = 0,0
    else:
        ball_speed_x, ball_speed_y = speed_constant * random.choice((1,-1)), speed_constant * random.choice((1,-1))
        score_time = None
        animate = True
        goal_sound = True

    return ball_speed_x, ball_speed_y, score_time, animate, player1, goal_sound
