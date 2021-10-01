import pygame
import random
import os

pygame.mixer.init()
pygame.init()

# Colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
Green = (35,45,40)

# Creating window
screen_width = 900
screen_height = 600
gameWindow = pygame.display.set_mode((screen_width, screen_height))

# Game Title
pygame.display.set_caption("Snakes by vishal")
pygame.display.update()

clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial",50)

pygame.mixer.music.load("music/game-start-6104.mp3")
pygame.mixer.music.play()

def text_screen(text , color , x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x,y])


def plot_snake(gameWindow, color, snk_list, snake_size):
    for x,y in snk_list:
        pygame.draw.rect(gameWindow, color, [x,y,snake_size, snake_size])

#Welcome Screen
intro = pygame.image.load("Screen/bg.jpg")
snakeart =pygame.image.load("Screen/snake-art.png")
snakeart= pygame.transform.scale(snakeart, (screen_width, screen_height)).convert_alpha()

def welcome():
    exit_game = False
    while not exit_game:
        gameWindow.blit(intro, (0,0))
        # gameWindow.fill(white)
        gameWindow.blit(snakeart,(0,0))
        text_screen("SNAKES", Green, 570,100)
        text_screen("Press Enter to Start", Green, 500,160)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pygame.mixer.music.load('music/wc.mp3')
                    pygame.mixer.music.play()
                    gameloop()
        pygame.display.update()
        clock.tick(60)


# Game Loop
def gameloop():
    # Game specific variables
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    velocity_x = 0
    velocity_y = 0

    snake_size = 30
    fps = 60
    food_x = random.randint(20,screen_width/2)
    food_y = random.randint(20, screen_height/2)
    score = 0
    init_velocity = 5

    snk_list = []
    snk_length = 1   
    if (not os.path.exists("highscore.txt")):
        with open("highscore.txt","w") as f:
            f.write("0")
    with open("highscore.txt","r") as f:
        highscore = f.read()
    
    while not exit_game:
        if game_over:
            with open("highscore.txt", "w")as f:
                f.write(str(highscore))
            
            #Game over screen
            endimg =pygame.image.load("Screen/snake-art.png")
            gameWindow.fill(white)
            gameWindow.blit(endimg,(100,180))
            text_screen("GAME OVER!  Press Enter to Continue", red, 100,80)
            text_screen("Score: "+ str(score), Green , 160,150)            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        pygame.mixer.music.load("music/game-start-6104.mp3")
                        pygame.mixer.music.play()
                        welcome()
                        # gameloop()
        # To move snake 
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0
    
                    if event.key == pygame.K_LEFT:
                        velocity_x = - init_velocity
                        velocity_y = 0
                           
                    if event.key == pygame.K_UP:
                        velocity_x = 0
                        velocity_y= - init_velocity
                
                    if event.key == pygame.K_DOWN:
                        velocity_x = 0
                        velocity_y = init_velocity
                            
                    if event.key == pygame.K_q:
                        score += 10

            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y

            # food eat
            if abs(snake_x -food_x)< 18 and abs(snake_y - food_y)< 18:
                pygame.mixer.music.load("music/beep-sound-8333.mp3")
                pygame.mixer.music.play()
                pygame.mixer.music.set_volume(.2)
                score += 10
                food_x = random.randint( 20, screen_width/2)
                food_y = random.randint(20, screen_height /2)
                snk_length+=5
                if score>int(highscore):
                    highscore = score
                
            bg =pygame.image.load("Screen/bg2.jpg")
            
            gameWindow.blit(bg,(0,0))    
            text_screen("Score: "+ str(score)+ "  Highscore: "+str(highscore), Green , 5,5)
            pygame.draw.rect(gameWindow, red ,[food_x , food_y, snake_size -8 , snake_size -8 ])

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            # if head hits its own body then gameover
            if len(snk_list)> snk_length:
                del snk_list[0]
            if head in snk_list[:-1]:
                pygame.mixer.music.load("music/snakehis.mp3")
                pygame.mixer.music.play()
                game_over = True

            # if snake hit wall
            if snake_x<0 or snake_x> screen_width or snake_y<0 or snake_y> screen_height:
                game_over = True
                pygame.mixer.music.load("music/hit-someting.mp3")
                pygame.mixer.music.play()
            plot_snake(gameWindow,black,snk_list,snake_size)
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()
# gameloop()
welcome()

