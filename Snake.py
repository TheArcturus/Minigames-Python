
import pygame
import sys, time
import random

# Constantes hors jeu

WHITE = (200, 200, 200) # Couleurs
BLACK = (0, 0, 0)
BLOCKSIZE = 30 # Taille carrés grille

# Initialsiation jeu

pygame.init()
print()
print("Démarrage du jeu...")

# Initialisation fenêtre 

SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 720, 480 # Size
GAME_SIZE = GAME_WIDTH, GAME_HEIGHT = 600, 400 # Game size
MARGIN = 60 # Ecart bordure fenêtre - Bordure du jeu

screen = pygame.display.set_mode(SIZE) # Screen creation with size
pygame.display.set_caption("Snake") # Screen title

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

# Fonctions pratiques

def drawGrid():
    """Draw the game grid"""

    for x in range(MARGIN, GAME_WIDTH, BLOCKSIZE):
        for y in range(MARGIN, GAME_HEIGHT, BLOCKSIZE):
            rect = pygame.Rect(x, y, BLOCKSIZE, BLOCKSIZE)
            pygame.draw.rect(screen, WHITE, rect, 1) # écran, couleur, object rect, 0 = fill et 1 = non

def drawApple(snake):
    """Draw an apple in a random position"""

    # X = 0 <=> MARGIN, X = max <=> WIDTH-MARGIN

    x, y = random.randrange(MARGIN, GAME_WIDTH, BLOCKSIZE)+8, random.randrange(MARGIN, GAME_HEIGHT, BLOCKSIZE)+8 # Center the apple

    for _, _, _, xsnake, ysnake in snake:
        if x == xsnake or y == ysnake:
            x, y = random.randrange(MARGIN, GAME_WIDTH, BLOCKSIZE)+8, random.randrange(MARGIN, GAME_HEIGHT, BLOCKSIZE)+8

    apple = pygame.Rect(x, y, 15, 15)
    pygame.draw.rect(screen, (255, 0, 0), apple, 0) # Red

    print("New apple created at : x=" + str(x) + " and y=" + str(y))
    return (x, y)

def score_display(score):
    value = score_font.render("Score: " + str(score), True, (255, 255, 0)) # True = Smooth edge
    screen.blit(value, [0, 0]) # Render an image, size

def draw_snake(snake):
    """Draw the snake with the different colors"""

    for r, g, b, x, y in snake:
        cube = pygame.Rect(x, y, BLOCKSIZE, BLOCKSIZE)
        pygame.draw.rect(screen, (r, g, b), cube, 0)

def mov_snake(snake, pos, mov): # Pos = x or y = 3 or 4
    """Move the snake and clear former cube"""

    # Stock former positions
    tmp = [tpl for tpl in snake]

    # Move head to next position 
    head = list(snake[0])
    head[pos] += mov # New y position
    snake[0] = tuple(head)

    # Then move all other cube to cube before them
    for i in range(1, len(snake)):
        tpl = tmp[i]
        former_tpl = list(tmp[i-1])
        r, g, b = tpl[0], tpl[1], tpl[2]
        tpl = former_tpl
        tpl[0], tpl[1], tpl[2] = r, g, b
        snake[i] = tuple(tpl)

    # Fill last position of the snake with black since the case is empty
    if pos == 3:
        rect = pygame.Rect(tmp[len(tmp)-1][3], tmp[len(tmp)-1][4], BLOCKSIZE, BLOCKSIZE)
        pygame.draw.rect(screen, BLACK, rect, 1)
        rect = pygame.Rect(tmp[len(tmp)-1][3], tmp[len(tmp)-1][4], BLOCKSIZE, BLOCKSIZE)
        pygame.draw.rect(screen, BLACK, rect, 0)       
    else:
        rect = pygame.Rect(tmp[len(tmp)-1][3], tmp[len(tmp)-1][4], BLOCKSIZE, BLOCKSIZE)
        pygame.draw.rect(screen, BLACK, rect, 1)
        rect = pygame.Rect(tmp[len(tmp)-1][3], tmp[len(tmp)-1][4], BLOCKSIZE, BLOCKSIZE)
        pygame.draw.rect(screen, BLACK, rect, 0)

# Boucle du jeu

running = True
new_apple = True # True s'il faut une nouvelle pomme (aucune n'est sur la grille)
snake = [(0, 255, 0, MARGIN, MARGIN)] # Snake =  [(r, g, b, x, y)], head = green by default, first_position coordinate = (x=0, y=0) = (x=MARGIN, y=MARGIN)

clock = pygame.time.Clock() # Horloge pour ne pas se déplacer trop rapidement
FPS = 8
direction = (3, BLOCKSIZE) # Le serpent commence par aller vers la droite (direction par défaut)

while running:

    clock.tick(FPS)
    drawGrid() # Affichage grille du jeu
    score_display(len(snake)-1) # score = longueur serpent - 1 (taille de base)
    
    if new_apple: # Update pomme
        x_apple, y_apple = drawApple(snake)
        new_apple = False

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            print("Fermeture...")
            sys.exit()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_DOWN]:
        direction = (4, BLOCKSIZE)
        mov_snake(snake, 4, BLOCKSIZE)
        print("Key DOWN has been pressed")
                
    elif keys[pygame.K_UP]:
        direction = (4, -BLOCKSIZE)
        mov_snake(snake, 4, -BLOCKSIZE)
        print("Key UP has been pressed")

    elif keys[pygame.K_RIGHT]:
        direction = (3, BLOCKSIZE)
        mov_snake(snake, 3, BLOCKSIZE)
        print("Key RIGHT has been pressed")

    elif keys[pygame.K_LEFT]:
        direction = (3, -BLOCKSIZE)
        mov_snake(snake, 3, -BLOCKSIZE)
        print("Key LEFT has been pressed")
        
    elif keys[pygame.K_a]:
        new_apple = True
        print("Cheat key APPLE (a) has been pressed")
    
    else:
        print("Direction du serpent : (x=3 | y=4)=" + str(direction[0]))
        mov_snake(snake, direction[0], direction[1])

    draw_snake(snake) # Drawing with current state of the snake 

    if snake[0][3] == x_apple-8 and snake[0][4] == y_apple-8: # Head is on the apple

        # Update score
        screen.fill((0, 0, 0))

        # Prepare future apple
        new_apple = True 
        print("Apple eaten !")

        # Add a cube to the snake with random color
        snake.append((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), snake[len(snake)-1][3]-BLOCKSIZE, snake[len(snake)-1][4]))
        print("Actual snake is : " + str(snake))

    if (snake[0][3] > GAME_WIDTH or snake[0][3] < MARGIN or snake[0][4] < MARGIN or snake[0][4] > GAME_HEIGHT): # Head leave screen
        screen.fill((0, 0, 0))
        value = font_style.render("Game Over ! Your score was : " + str(len(snake)-1), True, (255, 0, 0))
        screen.blit(value, [WINDOW_WIDTH//4, WINDOW_HEIGHT//2])
        pygame.display.update()
        time.sleep(1.5)
        pygame.quit()
        print("Fermeture...")
        sys.exit() #Game over, closure

    pygame.display.update()

    

    