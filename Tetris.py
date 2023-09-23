
import pygame
import sys, time
import random

# Constantes hors jeu

WHITE = (200, 200, 200) # Couleurs
BLACK = (0, 0, 0)
BLOCKSIZE = 20 # Taille carrés grille

# Initialsiation jeu

pygame.init()
print()
print("Démarrage du jeu...")

# Initialisation fenêtre 

SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 500, 700 # Size
GAME_SIZE = GAME_WIDTH, GAME_HEIGHT = 400, 700 # Game size
MARGIN = 60 # Ecart bordure fenêtre - Bordure du jeu

screen = pygame.display.set_mode(SIZE) # Screen creation with size
pygame.display.set_caption("Tetris") # Screen title

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

# Fonctions pratiques

def drawGrid():
    """Draw the game grid"""

    for x in range(MARGIN, GAME_WIDTH, BLOCKSIZE):
        for y in range(MARGIN, GAME_HEIGHT, BLOCKSIZE):
            rect = pygame.Rect(x, y, BLOCKSIZE, BLOCKSIZE)
            pygame.draw.rect(screen, WHITE, rect, 1) # écran, couleur, object rect, 0 = fill et 1 = non

def score_display(score):
    value = score_font.render("Score: " + str(score), True, (255, 255, 0)) # True = Smooth edge
    screen.blit(value, [0, 0]) # Render an image, size

def clear(x, y, MARGIN):
    x = random.randrange(y, GAME_WIDTH-MARGIN, BLOCKSIZE)
    rect = pygame.Rect(x, y, BLOCKSIZE, BLOCKSIZE*4)
    pygame.draw.rect(screen, (0, 0, 255), rect, 0)       
    x = random.randrange(y, GAME_WIDTH-MARGIN, BLOCKSIZE)
    rect = pygame.Rect(x, y, BLOCKSIZE, BLOCKSIZE*4)
    pygame.draw.rect(screen, (0, 0, 255), rect, 0) 

# Tetriminos

def drawLigne(sens, y=MARGIN, x=0):
    """1 = droit, 2 = côté droit, 3 = côté gauche, 4 = bas"""

    # MARGIN <= x <= GAME_WIDTH

    # Draw

    if sens == 1 or sens == 4:
        x = random.randrange(y, GAME_WIDTH, BLOCKSIZE)
        rect = pygame.Rect(x, y, BLOCKSIZE, BLOCKSIZE*4)
        pygame.draw.rect(screen, (0, 0, 255), rect, 0)
   
    elif sens == 2:
        x = random.randrange(y, GAME_WIDTH-MARGIN, BLOCKSIZE)
        rect = pygame.Rect(x, y, BLOCKSIZE*4, BLOCKSIZE)
        pygame.draw.rect(screen, (0, 0, 255), rect, 0)   
    elif sens == 3:
        x = random.randrange(y, GAME_WIDTH-MARGIN, BLOCKSIZE)
        rect = pygame.Rect(x, y, BLOCKSIZE*4, BLOCKSIZE)
        pygame.draw.rect(screen, (0, 0, 255), rect, 0)

    # Clear 
    elif sens == -1 or sens == -4: 
        clear(x, y, 0)


    return (x, y) # Return starting position

def drawZigDroit(sens):
    return

# Boucle du jeu

running = True
nbr_ligne = 0
clock = pygame.time.Clock() # Horloge pour ne pas se déplacer trop rapidement
FPS = 10

tetriminos_en_jeu = False
x, y = 0, MARGIN

while running:

    clock.tick(FPS)
    drawGrid() # Affichage grille du jeu
    score_display(nbr_ligne) # score = nbr_ligne faite

    if not tetriminos_en_jeu: # S'il n'y a pas de tetriminos
        tetriminos_en_jeu = True
        figure, sens = random.randint(0, 0), random.randint(0, 4)
        #if figure == 0:
        x, y = drawLigne(sens)
    else:
        print(x, y)
        if pygame.Surface.get_at(screen, (x, y+BLOCKSIZE//2)) == (0, 0, 0, 255) or y > GAME_HEIGHT: # Case en dessous est noir ou sort du cadre
            tetriminos_en_jeu = False
       # else: # Sinon on fait descendre le tetrimino selon son sens
            # On efface à l'ancienne position

            # On redessinne à la nouvelle
            

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            print("Fermeture...")
            sys.exit()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_DOWN]:
        drawLigne(3)
        print("Key DOWN has been pressed")
                
    elif keys[pygame.K_UP]:
        
        print("Key UP has been pressed")

    pygame.display.update()
