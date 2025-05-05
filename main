import random, sys, time, math, pygame
from pygame.locals import *

"""
POZNAMKOVAL SOM PO SLOVENSKY LEBO SOM TO NARYCHLO ZBUCHAVAL POTOM SA TO MOZE KLUDNE ZMENIT
"""


FPS = 30
WINWIDTH = 4* 240
WINHEIGHT = 3* 240
HALFWINWIDTH = int(WINWIDTH / 2)
HALFWINHEIGHT = int(WINHEIGHT / 2)


# farby este sa budu pridavat
BGCOLOR = (20, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

CAMERASLACK = 90     # kolko sa musi hrac pohnut aby sa pohla kamera
MOVERATE = 9         
BOUNCERATE = 6      
BOUNCEHEIGHT = 30    
STARTLEVEL = 1
STARTHEALTH = 5
WINLEVEL = 300       
NOHITTIME = 2      # sekundy kym je hrac nezranitelny
MAXHEALTH = 10  

NUMSENEMY = 30
ENEMYMINSPEED = 3
ENEMYMAXSPEED = 7
DIRCHANGEFREQ = 2 # direction change frequency - ako casto sa enemy pohybuju nahodne do novej strany
ENEMYHEALTH = 1


def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT))
    pygame.display.set_caption('2DM')
    BASICFONT = pygame.font.Font('freesansbold.ttf', 32)

    #nacitanie obrazkov hraca ,enemyho a dalsich veciciek
    # nieco ako PLAYERIMAGE = pygame.image.load('player.png')


    # tu vytvorit nejake texty game over,win atd. aby sme je mohli potom pouzit a zobrazit na obrazovke



    while True:
        run_game()

def run_game():
    global FPSCLOCK, DISPLAYSURF
    immortalityMode = False
    immortalityStartTime = 0
    gameOverMode = False        
    winMode = False     


    camerax = 0
    cameray = 0


    moveleft = False
    moveright = False   
    moveup = False
    movedown = False

    #spravit nejake pozadie pociatocne na obrazovke


    while True:

        if immortalityMode and time.time() - immortalityStartTime > NOHITTIME:
            immortalityMode = False

        # pohyb vsetkych enemych

        #sledovat vsetky objekty ci ich netreba zmazat ak su mimo obrazovku

        # pridat dalsie objekty do hry ak treba

        # pohnut kamerou ak sa postava pohne mimo nejakej oblasti v strede obrazovky

        # vykreslit pozadie

        # vykreslit vsetky objetkty na obrazovke

        # vykreslit hraca a jeho zivoty


        for event in pygame.event.get(): # event handling cyklus
            if event.type == QUIT:
                terminate()

            #nejaky pohyb
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
                    #otocim hraca do lava
                elif event.key in (K_RIGHT, K_d):
                    moveLeft = False
                    moveRight = True
                    #otocim hraca do prava

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

        # pohyb hraca ak je vsetko ok a nie je game over alebo win

        # sledujem ci nenastala kolizia s enemy alebo inym objektom
        # ak nastala kolizia tak zoberem zivot hracovi a nastavim mu cas kedy je nezranitelny alebo hrac znici enemyho zalezi
        # od ich levelu alebo niecoho ineho

        # sledujem ci som nedosiahol nejake win condition alebo ci som nezomrel

        # ak som zomrel tak nastavim gameOverMode na True a ak som vyhral tak nastavim winMode na True

        pygame.display.update()
        FPSCLOCK.tick(FPS)
    

def terminate():
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()


"""
spravit FUNKCIE/METODY na tieto veci:

vykreslit nejaky health bar
ziskat nejaku nahodnu rychlost enemy
zidskat nahodnu poziciu mimo kameru
tvorba noveho enemy
tvorba nejakeho novehu objektu (nejaky item ktory sa da ziskat koliziuou a ziskam z neho nieco)
zistit ci je nieco mimo obrazovku
nejaky vypocet toho bounnce pohybu hraca/enemy
ziskat nahodnu poziciu na obrazovke


"""
