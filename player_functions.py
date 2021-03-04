import pygame, sys, random

def player_animation(player1, player2, SCREEN_SIZE):

    player_positions = [-1, -1, -1, -1]

    if player1.top <= 0:
        player_positions[0] = 0

    if player1.bottom >= SCREEN_SIZE[1]:
        player_positions[1] = SCREEN_SIZE[1]

    if player2.top <= 0:
        player_positions[2] = 0

    if player2.bottom >= SCREEN_SIZE[1]:
        player_positions[3] = SCREEN_SIZE[1]

    return player_positions

def user_input(p1_speed):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        #if the key has been pressed down increase the player speed
        #depending on direction
        if event.type == pygame.KEYDOWN:
            # if event.key == pygame.K_DOWN:
            #     #move down
            #     p2_speed += 7
            # if event.key == pygame.K_UP:
            #     #move up
            #     p2_speed -= 7
            if event.key == pygame.K_s:
                #move down
                p1_speed += 10
            if event.key == pygame.K_w:
                #move up
                p1_speed -= 10

        #if the key has been released revert the speed back by the amount
        #it was increased by
        if event.type == pygame.KEYUP:
            # if event.key == pygame.K_DOWN:
            #     #move down
            #     p2_speed -= 7
            # if event.key == pygame.K_UP:
            #     #move up
            #     p2_speed += 7
            if event.key == pygame.K_s:
                #move down
                p1_speed -= 10
            if event.key == pygame.K_w:
                #move up
                p1_speed += 10
    return p1_speed
