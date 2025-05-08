import random, sys, time, math, pygame
from pygame.locals import *


from hero import Hero
from enemy import Enemy
from tree import Tree

"""
POZNAMKOVAL SOM PO SLOVENSKY LEBO SOM TO NARYCHLO ZBUCHAVAL POTOM SA TO MOZE KLUDNE ZMENIT
"""


FPS = 30
WINWIDTH = 4* 240
WINHEIGHT = 3* 240
HALFWINWIDTH = int(WINWIDTH / 2)
HALFWINHEIGHT = int(WINHEIGHT / 2)


# Colors
BGCOLOR = (20, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

CAMERASLACK = 180     # how much hero needs to move to move the camera
MOVERATE = 25     # speed of the player   
BOUNCERATE = 6      
BOUNCEHEIGHT = 30    
STARTLEVEL = 1
STARTHEALTH = 5
WINLEVEL = 300   
NOHITTIME = 2      # invicible time
MAXHEALTH = 100  

NUMSENEMY = 30
ENEMYMINSPEED = 3
ENEMYMAXSPEED = 7
DIRCHANGEFREQ = 2 # direction change frequency - ako casto sa enemy pohybuju nahodne do novej strany ??div110: netusim co to je
ENEMYHEALTH = 1

NUMSOFTREES = 10 
MAXOFFSCREENPOS = 1000 # max distance (in pixels??) of a object

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT
    global main_character, RHEROIMG, LHEROIMG, LENEMYIMG, RENEMYIMG, TREEIMG

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT))
    pygame.display.set_caption('2DM')
    BASICFONT = pygame.font.Font('freesansbold.ttf', 32)

    #loading pictures
    RHEROIMG = pygame.image.load('graphics/boxer2.png')
    LHEROIMG = pygame.transform.flip(RHEROIMG, True, False)
    LENEMYIMG = pygame.image.load('graphics/policeman.png')
    RENEMYIMG = pygame.transform.flip(LENEMYIMG,True, False)
    TREEIMG = pygame.image.load('graphics/tree_v1.png')

    # game texts, incomplete!!
    game_over_surf, game_over_rect = make_text("GAME OVER", WHITE, BLACK, 0,0)
    game_win_surf, game_win_rect = make_text("YOU HAVE ACHIEVED MAX LEVEL", WHITE, BLACK, 0,0)


    while True:
        run_game()

def run_game():
    # tu sa nastavuju pociatocne hodnoty aby sa vynulovali pri resete hry
    global FPSCLOCK, DISPLAYSURF, main_character
    global moveDown, moveLeft, moveRight, moveUp, camera_x, camera_y
    global gameOverMode, winMode, immortalityMode, immortalityStartTime
    immortalityMode = False
    immortalityStartTime = 0
    gameOverMode = False        
    winMode = False     


    camera_x = 0
    camera_y = 0

    # creating a Player Character
    main_character = Hero(RHEROIMG, HALFWINWIDTH, HALFWINHEIGHT, STARTLEVEL, MAXHEALTH)
    
    enemy1 = Enemy(LENEMYIMG,100,100,5,100)

    moveLeft = False
    moveRight = False   
    moveUp = False
    moveDown = False

    #spravit nejake pozadie pociatocne na obrazovke 

    # tu vytvorim nejake objekty(pozadie nie enemy) ktore sa budu nachadzat po obrazovke a budu sa generovat nahodne 
    trees_objs = []
    for i in range(0, NUMSOFTREES):
            tree = Tree(TREEIMG, 0, 0)
            tree.get_random_position(MAXOFFSCREENPOS, WINWIDTH, WINHEIGHT)
            trees_objs.append((tree))


    #game loop 
    while True:
        # aktualitizujem pociatocne hodnoty hraca a jeho pohyb
        if moveLeft:
            main_character.position_x -= MOVERATE
        if moveRight:
            main_character.position_x += MOVERATE
        if moveUp:
            main_character.position_y -= MOVERATE
        if moveDown:
            main_character.position_y += MOVERATE
        # zistujem ci ma hrac este pociatocnu nesmrtelnost
        if immortalityMode and time.time() - immortalityStartTime > NOHITTIME:
            immortalityMode = False

        # pohyb vsetkych enemych

        #sledovat vsetky objekty ci ich netreba zmazat ak su mimo obrazovku
        for (tree) in trees_objs:
            if tree.is_off_screen( camera_x, camera_y, MAXOFFSCREENPOS, WINWIDTH, WINHEIGHT):
                trees_objs.remove(tree)
                tree = Tree(TREEIMG, 0, 0)
                tree.get_random_position_off_screen(moveUp, moveDown, moveLeft, moveRight, MAXOFFSCREENPOS, WINWIDTH, WINHEIGHT)
                trees_objs.append(tree)
        # pridat dalsie objekty do hry ak treba

        # pohnut kamerou ak sa postava pohne mimo nejakej oblasti v strede obrazovky

        # draw background -- could use a texture?
        DISPLAYSURF.fill(GREEN)
         # vykreslit strom na pozadi

        for tree in trees_objs:
            treeRect = tree.image.get_rect()
            treeRect.center = (tree.position_x - camera_x, tree.position_y - camera_y)
            DISPLAYSURF.blit(tree.image, treeRect)

        # draw all objects

        # draw player and other entities
        draw_entity(main_character,camera_x,camera_y)
        main_character.draw_health_bar(DISPLAYSURF)
        
        draw_entity(enemy1, camera_x, camera_y)
        enemy1.move(main_character.position_x,main_character.position_y)

        for event in pygame.event.get(): # event handling cycle
            if event.type == QUIT:
                terminate()

            #handling player movement
            elif event.type == KEYDOWN:
                if event.key in (K_UP, K_w):
                    moveDown = False
                    moveUp = True
                elif event.key in (K_DOWN, K_s):
                    moveUp = False
                    moveDown = True
                elif event.key in (K_LEFT, K_a):
                    moveRight = False
                    moveLeft = True
                    #flipping the player left
                    if main_character.image == RHEROIMG:
                        main_character.image = LHEROIMG

                elif event.key in (K_RIGHT, K_d):
                    moveLeft = False
                    moveRight = True
                    #flipping the player right
                    if main_character.image == LHEROIMG:
                        main_character.image = RHEROIMG

            #zastavim pohyb hraca ak sa uvolni klavesa
            elif event.type == KEYUP:
                if event.key in (K_LEFT, K_a):
                    moveLeft = False
                elif event.key in (K_RIGHT, K_d):
                    moveRight = False
                elif event.key in (K_UP, K_w):
                    moveUp = False
                elif event.key in (K_DOWN, K_s):
                    moveDown = False

                elif event.key == K_ESCAPE:
                    terminate()


        # pohyb hraca
        moving_hero(main_character, moveLeft, moveRight, moveUp, moveDown) 
        # pohyb kamery ak sa hrac pohnul mimo obrazovky
        moving_camera(main_character)

        # test v konzole vypisuje poziciu hraca a kamery
        print(f"hero pos x {main_character.position_x}, hero pos y {main_character.position_y},camera x {camera_x}, camera y{camera_y}")


        # pohyb hraca ak je vsetko ok a nie je game over alebo win

        # sledujem ci nenastala kolizia s enemy alebo inym objektom
        # ak nastala kolizia tak zoberem zivot hracovi a nastavim mu cas kedy je nezranitelny alebo hrac znici enemyho zalezi
        # od ich levelu alebo niecoho ineho

        # sledujem ci som nedosiahol nejake win condition alebo ci som nezomrel

        # ak som zomrel tak nastavim gameOverMode na True a ak som vyhral tak nastavim winMode na True

        pygame.display.update()
        FPSCLOCK.tick(FPS)
    

def terminate(): # ukonci program
    pygame.quit()
    sys.exit()

def make_text(text, color, bg_color, top, left): # vytvori text na obrazovke
    text_surf = BASICFONT.render(text, True, color, bg_color)
    text_rect = text_surf.get_rect()
    text_rect.topleft = (top, left)
    return text_surf, text_rect

def draw_entity(hero, camera_x, camera_y): # vykresli hraca na obrazovku
    heroRect = hero.image.get_rect()
    heroRect.center = (hero.position_x - camera_x, hero.position_y - camera_y)
    DISPLAYSURF.blit(hero.image, heroRect)

def moving_hero(hero, moveLeft, moveRight, moveUp, moveDown): # posuva hraca ak sa pohne
    global camera_x, camera_y
    if moveLeft and hero.position_x > CAMERASLACK:
        hero.position_x -= MOVERATE
    if hero.position_x < camera_x + CAMERASLACK:
        camera_x -= MOVERATE
    if moveRight and hero.position_x < WINWIDTH - CAMERASLACK:
        hero.position_x += MOVERATE
    if hero.position_x > camera_x + WINWIDTH - CAMERASLACK:
        camera_x += MOVERATE
    if moveUp and hero.position_y > CAMERASLACK:
        hero.position_y -= MOVERATE
    if hero.position_y < camera_y + CAMERASLACK:
        camera_y -= MOVERATE
    if moveDown and hero.position_y < WINHEIGHT - CAMERASLACK:
        hero.position_y += MOVERATE
    if hero.position_y > camera_y + WINHEIGHT - CAMERASLACK:
        camera_y += MOVERATE

def moving_camera(hero): # posuvam kameru ak sa hrac pohnul mimo obrazovky
    global camera_x, camera_y
    if hero.position_x < camera_x + CAMERASLACK:
        camera_x -= MOVERATE
    if hero.position_x > camera_x + WINWIDTH - CAMERASLACK:
        camera_x += MOVERATE
    if hero.position_y < camera_y + CAMERASLACK:
        camera_y -= MOVERATE
    if hero.position_y > camera_y + WINHEIGHT - CAMERASLACK:
        camera_y += MOVERATE


if __name__ == '__main__':
    main()


"""
spravit FUNKCIE/METODY na tieto veci:

vykreslit nejaky health bar - DONE -> hero.draw_health_bar()
ziskat nejaku nahodnu rychlost enemy
tvorba noveho enemy
tvorba nejakeho novehu objektu (nejaky item ktory sa da ziskat koliziuou a ziskam z neho nieco)
nejaky vypocet toho bounnce pohybu hraca/enemy - NE->pohyby vyresime na Discordu


Pridal jsem textury - graphics, jsou jen prozatim
"""
