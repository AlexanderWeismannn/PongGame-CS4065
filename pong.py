import pygame, sys, random


def ball_animation():
    global ballSpdX, ballSpdY, p1Score, p2Score, score_time
    ball.x += ballSpdX
    ball.y += ballSpdY

    #collision logic
    if ball.top <= 0 or ball.bottom >= screenHeight:
        #negatively reverse the ball speed (i.e. cause it to bounce)
        ballSpdY *= -1

    #P2 scores a goal
    if ball.left <= 0:
        p2Score += 1
        score_time = pygame.time.get_ticks()
    
    #P1 scores a goal
    if ball.right >= screenWidth:
        p1Score += 1
        score_time = pygame.time.get_ticks()

    #paddle Collison
    if ball.colliderect(player1) or ball.colliderect(player2):
        ballSpdX *= -1


def user_input():
    #Handle user input
    global p1Speed, p2Speed

    player1.y += p1Speed
    player2.y += p2Speed


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        #if the key has been pressed down increase the player speed
        #depending on direction
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                #move down
                p2Speed += 7
            if event.key == pygame.K_UP:
                #move up
                p2Speed -= 7
            if event.key == pygame.K_s:
                #move down
                p1Speed += 7
            if event.key == pygame.K_w:
                #move up
                p1Speed -= 7

        #if the key has been released revert the speed back by the amount
        #it was increased by
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                #move down
                p2Speed -= 7
            if event.key == pygame.K_UP:
                #move up
                p2Speed += 7
            if event.key == pygame.K_s:
                #move down
                p1Speed -= 7
            if event.key == pygame.K_w:
                #move up
                p1Speed += 7                

def player_animation():
    if player1.top <= 0:
        player1.top = 0

    if player1.bottom >= screenHeight:
        player1.bottom = screenHeight    

    if player2.top <= 0:
        player2.top = 0

    if player2.bottom >= screenHeight:
        player2.bottom = screenHeight    


def ball_reset():
    global ballSpdX, ballSpdY, score_time, textFont
    current_time = pygame.time.get_ticks()
    ball.center = (screenWidth/2, screenHeight/2)

    #prints 2
    if(current_time - score_time < 700):
        num3 = textFont.render("3", True, white)
        display.blit(num3,(screenWidth/2 - 10, screenHeight/2 + 30))
        
    if 700 < (current_time - score_time) < 1400:
        num2 = textFont.render("2", True, white)
        display.blit(num2,(screenWidth/2 - 10, screenHeight/2 + 30))
      
    if 1400 < (current_time - score_time) < 2100:
        num1 = textFont.render("1", True, white)
        display.blit(num1,(screenWidth/2 - 10, screenHeight/2 + 30))
         

    #creates a 2.1 second delay where the ball speed = 0 before setting it back to the normal X and Y speeds
    if(current_time - score_time < 2100):
        ballSpdX, ballSpdY = 0,0
    else:
        ballSpdX, ballSpdY = 7 * random.choice((1,-1)),7 * random.choice((1,-1)) 
        score_time = None


   



#set up pygame
pygame.init()
clock = pygame.time.Clock()


#Setup for the main window to be fullscreen
screenWidth = 1600
screenHeight = 900
display = pygame.display.set_mode((screenWidth,screenHeight))
pygame.display.set_caption("Pong")


#Create the ball
#/2 - 15 to get the exact midpoint of our screen
#the ball is created as a rectangle but drawn as an ellipse
ball = pygame.Rect(screenWidth/2 - 15, screenHeight/2 - 15, 30,30)
player1 = pygame.Rect(10, screenHeight/2 - 70,10,140)
player2 = pygame.Rect(screenWidth - 20,screenHeight/2 - 70,10,140)
center = pygame.Rect(screenWidth/2 - 25,screenHeight/2 - 25,50,50)


#colors for the objects
backgroundColor = pygame.Color("grey12")
white = pygame.Color("gray100")
grey = pygame.Color("gray71")

#ball speed 
ballSpdX = 7 * random.choice((1,-1))
ballSpdY = 7 * random.choice((1,-1))

#initial player speed before moving (change movement speed in user_input() if wanted)
p1Speed = 0
p2Speed = 0

#On screen text 
p1Score = 0
p2Score = 0
textFont = pygame.font.Font("freesansbold.ttf", 32)

#Countdown score timer
score_time = None


while True:

    user_input()
    player_animation()
    ball_animation()
    
    #Draw visuals
    display.fill(backgroundColor)


    pygame.draw.aaline(display,white,(screenWidth/2,0),(screenWidth/2, screenHeight))
    pygame.draw.ellipse(display,grey,center)

    pygame.draw.rect(display, white, player1)
    pygame.draw.rect(display, white, player2) 
    pygame.draw.ellipse(display, white, ball)

    #the ball has collided with the left/right side of the screen
    if score_time:
        ball_reset()
  

    player1_text = textFont.render(f"{p1Score}",True,white)
    player2_text = textFont.render(f"{p2Score}",True,white)
    display.blit(player1_text,(735,470))
    display.blit(player2_text,(850,470))


    #updating the window
    pygame.display.flip()
    clock.tick(60)        

