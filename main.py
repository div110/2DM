import random, sys, time, math, pygame
from pygame.locals import *


from hero import Hero
from enemy import Enemy
from tree import Tree



FPS = 30
WINWIDTH = 4* 240
WINHEIGHT = 3* 240
HALFWINWIDTH = int(WINWIDTH / 2)
HALFWINHEIGHT = int(WINHEIGHT / 2)


# Colors
BGCOLOR = (25, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 150, 0)

CAMERASLACK = 180     # how much hero needs to move to move the camera
MOVERATE = 10     # speed of the player   
BOUNCERATE = 6      
BOUNCEHEIGHT = 30    
STARTLEVEL = 1
STARTHEALTH = 5
WINLEVEL = 300   
NOHITTIME = 2      # invicible time
MAXHEALTH = 20  

NUMSENEMY = 30
ENEMYMINSPEED = 3
ENEMYMAXSPEED = 7
DIRCHANGEFREQ = 2 # direction change frequency - ako casto sa enemy pohybuju nahodne do novej strany ??div110: netusim co to je
ENEMYHEALTH = 1

NUMSOFTREES = 20 
MAXOFFSCREENPOS = 200 # max distance (in pixels??) of a object

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, NUMSOFTREES
    global main_character, RHEROIMG, LHEROIMG, LENEMYIMG, RENEMYIMG, TREEIMG, treeimgheight, treeimgwidth,grass_tile_size, GRASSIMG, HEARTIMG, RBLACKHEARTIMG, LBLACKHEARTIMG
    global RSWORDPARTICLES, LSWORDPARTICLES, R2HEROIMG,L2HEROIMG, R3HEROIMG, L3HEROIMG
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT))
    pygame.display.set_caption('2DM')
    BASICFONT = pygame.font.Font('freesansbold.ttf', 32)

    #loading pictures
    RHEROIMG = pygame.image.load('graphics/hero_v3.png')
    RHEROIMG = pygame.transform.scale(RHEROIMG,(100, 100))
    LHEROIMG = pygame.transform.flip(RHEROIMG, True, False)

    R2HEROIMG = pygame.image.load('graphics/sword_up_hero.png')
    R2HEROIMG = pygame.transform.scale(R2HEROIMG,(100, 100))
    L2HEROIMG = pygame.transform.flip(R2HEROIMG, True, False)

    R3HEROIMG = pygame.image.load('graphics/sword_down_hero.png')
    R3HEROIMG = pygame.transform.scale(R3HEROIMG,(100, 100))
    L3HEROIMG = pygame.transform.flip(R3HEROIMG, True, False)

    LENEMYIMG = pygame.image.load('graphics/skull_enemy.png')
    LENEMYIMG = pygame.transform.scale(LENEMYIMG,(130, 100))
    RENEMYIMG = pygame.transform.flip(LENEMYIMG,True, False)
    TREEIMG = pygame.image.load('graphics/tree_v2.png')
    TREEIMG = pygame.transform.scale(TREEIMG, (150,150))

    GRASSIMG = pygame.image.load('graphics/grass_v3.png')
    GRASSIMG = pygame.transform.scale(GRASSIMG,(WINWIDTH,WINWIDTH))
    HEARTIMG = pygame.image.load('graphics/heart.png')
    HEARTIMG = pygame.transform.scale(HEARTIMG, (20,20))
    RBLACKHEARTIMG = pygame.image.load('graphics/black_heart_r.png')
    RBLACKHEARTIMG = pygame.transform.scale(RBLACKHEARTIMG, (20,20))
    LBLACKHEARTIMG = pygame.transform.flip(RBLACKHEARTIMG, True, False)
    RSWORDPARTICLES = pygame.image.load('graphics/sword_particles.png')
    RSWORDPARTICLES = pygame.transform.scale(RSWORDPARTICLES, (120,180) )
    LSWORDPARTICLES = pygame.transform.flip(RSWORDPARTICLES, True, False)
    treeimgwidth = TREEIMG.get_width()
    treeimgheight = TREEIMG.get_height()
    grass_tile_size = GRASSIMG.get_width()
    # game texts, incomplete!!
    game_over_surf, game_over_rect = make_text("GAME OVER", WHITE, BLACK, 0,0)
    game_win_surf, game_win_rect = make_text("YOU HAVE ACHIEVED MAX LEVEL", WHITE, BLACK, 0,0)


    while True:
        run_game()

def run_game():
    # initial values are set to defaul for easy reset
    global FPSCLOCK, DISPLAYSURF, main_character, NUMSOFTREES
    global moveDown, moveLeft, moveRight, moveUp, camera_x, camera_y, attackKey
    global gameOverMode, winMode, immortalityMode, immortalityStartTime, trees_objs, enemy1, enemy1_objs
    immortalityMode = False
    immortalityStartTime = 0
    gameOverMode = False        
    winMode = False     


    camera_x = 0
    camera_y = 0
    enemy1_objs = []
    # creating a Player Character
    main_character = Hero(RHEROIMG, HALFWINWIDTH, HALFWINHEIGHT, STARTLEVEL, MAXHEALTH , HEARTIMG, RBLACKHEARTIMG, LBLACKHEARTIMG)
    enemy1 = Enemy(LENEMYIMG,RENEMYIMG,100,100,5,20)
    enemy1_objs.append(enemy1)
    enemy2 = Enemy(LENEMYIMG,RENEMYIMG,300,300,5,20)
    enemy1_objs.append(enemy2)
    moveLeft = False
    moveRight = False   
    moveUp = False
    moveDown = False
    attackKey = False

    #draw background
    start_x = -camera_x % grass_tile_size - grass_tile_size
    start_y = -camera_y % grass_tile_size - grass_tile_size

    for x in range(start_x, WINWIDTH + grass_tile_size, grass_tile_size):
        for y in range(start_y, WINHEIGHT + grass_tile_size, grass_tile_size):
            DISPLAYSURF.blit(GRASSIMG, (x, y))
    #draw trees
    trees_objs = []
    for i in range(0, NUMSOFTREES):
            tree = Tree(TREEIMG, 0, 0, treeimgwidth, treeimgheight)
            tree.get_random_position(MAXOFFSCREENPOS, WINWIDTH, WINHEIGHT)
            trees_objs.append((tree))


    #game loop 
    while True:
        # update players values and movement
        if moveLeft:
            main_character.position_x -= MOVERATE
        if moveRight:
            main_character.position_x += MOVERATE
        if moveUp:
            main_character.position_y -= MOVERATE
        if moveDown:
            main_character.position_y += MOVERATE
        # checking for invicible mode
        if immortalityMode and time.time() - immortalityStartTime > NOHITTIME:
            immortalityMode = False

        # movement of all enemies

        # checking for deleting objects if they are outside of screen area
        for (tree) in trees_objs:
            if tree.is_off_screen(camera_x, camera_y, MAXOFFSCREENPOS, WINWIDTH, WINHEIGHT):
                #print("tree removed at", tree.position_x, tree.position_y)
                trees_objs.remove(tree)

        while len(trees_objs) < NUMSOFTREES:
            #print()
            t = generate_new_tree()
            trees_objs.append(t)
        #print(len(trees_objs))
        # adding more objects


        # draw background

        draw_background()

        # draw trees
        
            #print("tree pos x", tree.position_x, "tree pos y", tree.position_y)
        draw_trees(trees_objs)
           
        # draw all objects

        # draw player and other entities
        draw_hero(main_character,camera_x,camera_y,attackKey)
        main_character.draw_health_bar(DISPLAYSURF)

        for (enemy1) in enemy1_objs:
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
                elif event.key == K_q:
                    attackKey = True

            # stop players movement if keyup
            elif event.type == KEYUP:
                if event.key in (K_LEFT, K_a):
                    moveLeft = False
                elif event.key in (K_RIGHT, K_d):
                    moveRight = False
                elif event.key in (K_UP, K_w):
                    moveUp = False
                elif event.key in (K_DOWN, K_s):
                    moveDown = False
                elif event.key == K_q:
                    attackKey = False
                elif event.key == K_ESCAPE:
                    terminate()

        print(attackKey)

        
        # players movement
        moving_hero(main_character, moveLeft, moveRight, moveUp, moveDown) 
        #print("hero pos x", main_character.position_x, "hero pos y", main_character.position_y)
        # camera movement
        moving_camera(main_character)
        #print(f"camera slack cords x {camera_x} y {camera_y}")

        # test for player and camera cors
        #print(f"hero pos x {main_character.position_x}, hero pos y {main_character.position_y},camera x {camera_x}, camera y{camera_y}")


        # pohyb hraca ak je vsetko ok a nie je game over alebo win

        # sledujem ci nenastala kolizia s enemy alebo inym objektom
        # ak nastala kolizia tak zoberem zivot hracovi a nastavim mu cas kedy je nezranitelny alebo hrac znici enemyho zalezi
        # od ich levelu alebo niecoho ineho

        # sledujem ci som nedosiahol nejake win condition alebo ci som nezomrel

        # ak som zomrel tak nastavim gameOverMode na True a ak som vyhral tak nastavim winMode na True

        pygame.display.update()
        FPSCLOCK.tick(FPS)
    

def terminate(): # end game
    pygame.quit()
    sys.exit()

def make_text(text, color, bg_color, top, left): # make text on screen
    text_surf = BASICFONT.render(text, True, color, bg_color)
    text_rect = text_surf.get_rect()
    text_rect.topleft = (top, left)
    return text_surf, text_rect

def draw_entity(hero, camera_x, camera_y): # draw player on screen
    heroRect = hero.image.get_rect()
    heroRect.center = (hero.position_x - camera_x, hero.position_y - camera_y)
    DISPLAYSURF.blit(hero.image, heroRect)

def draw_hero(hero, camera_x, camera_y,attackKey): # draw player on screen
    heroRect = hero.image.get_rect()
    heroRect.center = (hero.position_x - camera_x, hero.position_y - camera_y)
    DISPLAYSURF.blit(hero.image, heroRect)
    if attackKey == True:
            hero_attack(main_character)


def moving_hero(hero, moveLeft, moveRight, moveUp, moveDown): # move player
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

def moving_camera(hero): # check for camera movement if needed
    global camera_x, camera_y
    if hero.position_x < camera_x + CAMERASLACK:
        camera_x -= MOVERATE
    if hero.position_x > camera_x + WINWIDTH - CAMERASLACK:
        camera_x += MOVERATE
    if hero.position_y < camera_y + CAMERASLACK:
        camera_y -= MOVERATE
    if hero.position_y > camera_y + WINHEIGHT - CAMERASLACK:
        camera_y += MOVERATE

def generate_new_tree():
    t = Tree(TREEIMG, 0, 0 , treeimgwidth, treeimgheight)
    x,y = t.get_random_position_off_screen(moveUp, moveDown,moveLeft, moveRight,MAXOFFSCREENPOS, WINWIDTH, WINHEIGHT)
    t.position_x = camera_x + x
    t.position_y = camera_y + y
    #print(f"added tree {t.position_x} {t.position_y}")
    return t

def hero_attack(hero):
    if hero.image == RHEROIMG:
        hero.image = R2HEROIMG
        draw_background()
        draw_trees(trees_objs)
        for (enemy1) in enemy1_objs:
            draw_entity(enemy1, camera_x, camera_y)
        hero.draw_health_bar(DISPLAYSURF)
        draw_entity(hero,camera_x-10,camera_y)
        pygame.display.update()
        pygame.time.wait(5)
        particlesRect = RSWORDPARTICLES.get_rect()
        particlesRect.center = (hero.position_x+30 - camera_x, hero.position_y - camera_y)
        DISPLAYSURF.blit(RSWORDPARTICLES, particlesRect)
        pygame.display.update()
        hero.image = R3HEROIMG
        draw_background()
        draw_trees(trees_objs)
        for (enemy1) in enemy1_objs:
            draw_entity(enemy1, camera_x, camera_y)
        draw_entity(hero,camera_x-10,camera_y)
        DISPLAYSURF.blit(RSWORDPARTICLES, particlesRect)
        pygame.display.update()
        hero.image = RHEROIMG

        particles_width = RSWORDPARTICLES.get_width()
        particles_height = RSWORDPARTICLES.get_height()
        particlesRect = pygame.Rect(hero.position_x +30 -camera_x - particles_width//2,hero.position_y-camera_y-particles_height//2, particles_width, particles_height)
        for (enemy1) in enemy1_objs:
            enemy_width = enemy1.image.get_width()
            enemy_height = enemy1.image.get_height()
            enemyRect = pygame.Rect(enemy1.position_x-camera_x - enemy_width//2, enemy1.position_y-camera_y-enemy_height//2, enemy_width, enemy_height)
            if particlesRect.colliderect(enemyRect):
                enemy1.current_health -= 1
                print(enemy1.current_health)
                if enemy1.current_health == 0:
                    enemy1_objs.remove(enemy1)
                

    if hero.image == LHEROIMG:
        hero.image = L2HEROIMG
        draw_background()
        draw_trees(trees_objs)
        for (enemy1) in enemy1_objs:
            draw_entity(enemy1, camera_x, camera_y)
        hero.draw_health_bar(DISPLAYSURF)
        draw_entity(hero,camera_x-10,camera_y)
        pygame.display.update()
        pygame.time.wait(5)
        particlesRect = LSWORDPARTICLES.get_rect()
        particlesRect.center = (hero.position_x-30 - camera_x, hero.position_y - camera_y)
        DISPLAYSURF.blit(LSWORDPARTICLES, particlesRect)
        pygame.display.update()
        hero.image = L3HEROIMG
        draw_background()
        draw_trees(trees_objs)
        for (enemy1) in enemy1_objs:
            draw_entity(enemy1, camera_x, camera_y)
        draw_entity(hero,camera_x-10,camera_y)
        DISPLAYSURF.blit(LSWORDPARTICLES, particlesRect)
        pygame.display.update()
        hero.image = LHEROIMG

        particles_width = RSWORDPARTICLES.get_width()
        particles_height = RSWORDPARTICLES.get_height()
        particlesRect = pygame.Rect(hero.position_x +30 -camera_x - particles_width//2,hero.position_y-camera_y-particles_height//2, particles_width, particles_height)
        for (enemy1) in enemy1_objs:
            enemy_width = enemy1.image.get_width()
            enemy_height = enemy1.image.get_height()
            enemyRect = pygame.Rect(enemy1.position_x-camera_x - enemy_width//2, enemy1.position_y-camera_y-enemy_height//2, enemy_width, enemy_height)
            if particlesRect.colliderect(enemyRect):
                enemy1.current_health -= 1
                print(enemy1.current_health)
                if enemy1.current_health == 0:
                    enemy1_objs.remove(enemy1)
    pass

def draw_background():
    start_x = -camera_x % grass_tile_size - grass_tile_size
    start_y = -camera_y % grass_tile_size - grass_tile_size

    for x in range(start_x, WINWIDTH + grass_tile_size, grass_tile_size):
        for y in range(start_y, WINHEIGHT + grass_tile_size, grass_tile_size):
            DISPLAYSURF.blit(GRASSIMG, (x, y))
    pass

def draw_trees(trees_objs):
    for tree in trees_objs:
        treeRect = tree.image.get_rect()
        treeRect.center = (tree.position_x - camera_x, tree.position_y - camera_y)
        DISPLAYSURF.blit(tree.image, treeRect)
    pass

if __name__ == '__main__':
    main()


"""
spravit FUNKCIE/METODY na tieto veci:

vykreslit nejaky health bar - DONE -> hero.draw_health_bar()
ziskat nejaku nahodnu rychlost enemy
tvorba noveho enemy
tvorba nejakeho novehu objektu (nejaky item ktory sa da ziskat koliziuou a ziskam z neho nieco)
nejaky vypocet toho bounnce pohybu hraca/enemy - NE->pohyby vyresime na DiscorduRSWORDPARTICLES


Pridal jsem textury - graphics, jsou jen prozatim
"""
