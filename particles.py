import pygame, sys, random
from pygame.locals import *

def particle_animation(display, ball, collision, particles, animate):

    #create random r g and b values
    #previous_time = pygame.time.get_ticks()

    if animate:

        # Left paddle
        if collision == -1:
            for i in range(100):
                particles.append([[ball.x, ball.y+15], [random.randint(0, 400) / 10 - 1, random.randint(-20, 20)], random.randint(4, 6), (255, 255, 255)])
        elif collision == 1: # Right paddle
            for i in range(100):
                particles.append([[ball.x+30, ball.y+15], [random.randint(-400, 0) / 10 - 1, random.randint(-20, 20)], random.randint(4, 6), (255, 255, 255)])
        else: # Ball
            particles.append([[ball.x+15, ball.y+15], [random.randint(0, 25) / 10 - 1, -2], random.randint(4, 6), (random.randint(0,255),random.randint(0,255),random.randint(0,255))])

        for particle in particles:
            particle[0][0] += particle[1][0]
            particle[0][1] += particle[1][1]
            particle[2] -= 0.1
            particle[1][1] += 0.1
            # if particle[3] == False:
            pygame.draw.circle(display, particle[3], [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
          
            if particle[2] <= 0:
                particles.remove(particle)
    else:
        particles.clear()
