import pygame, sys, random
from pygame.locals import *

def particle_animation(display, ball, particles):

    #create random r g and b values
    
    
    #previous_time = pygame.time.get_ticks()

   
       

        
    particles.append([[ball.x+15, ball.y+15], [random.randint(0, 25) / 10 - 1, -2], random.randint(4, 6)])

    for particle in particles:
        particle[0][0] += particle[1][0]
        particle[0][1] += particle[1][1]
        particle[2] -= 0.1
        particle[1][1] += 0.1
        if random.randint(1,5) == 1:
            r,g,b = 255,255,255
            pygame.draw.circle(display, (r,g,b), [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
        else:
            r,g,b = random.randint(0,255),random.randint(0,255),random.randint(0,255)
            pygame.draw.circle(display, (r,g,b), [int(particle[0][0]), int(particle[0][1])], int(particle[2]))    
        
        if particle[2] <= 0:
            particles.remove(particle)
    

