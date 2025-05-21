#!/usr/bin/python3

import random, sys, time, math, pygame
from pygame.locals import *


from last_score.qr import get_qr
from hero import Hero
from enemies_classes.enemy import Enemy
from objects_classes.tree import Tree
from enemies_classes.goblin_mage import Goblin_Mage
from enemies_classes.small_goblin import Small_Goblin
from enemies_classes.wolf import Wolf
from enemies_classes.boss import Boss
from enemies_classes.magic_pillar import Magic_Pillar
from fire_shot import Fire_Shot
from enemies_classes.boss_bluefire_shot import Bluefire_Shot

FPS = 30
WINWIDTH = 4* 240
WINHEIGHT = 3* 240
HALFWINWIDTH = int(WINWIDTH / 2)
HALFWINHEIGHT = int(WINHEIGHT / 2)


# Colors
BGCOLOR = (25, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
DARKRED = (75,0,0)
BLACK = (0, 0, 0)
GREEN = (0, 150, 0)
DARKGREEN = (0,75,0)

CAMERASLACK = 180     # how much hero needs to move to move the camera
MOVERATE = 10     # speed of the player   
BOUNCERATE = 6      
BOUNCEHEIGHT = 30    
STARTLEVEL = 1
STARTHEALTH = 5
WINLEVEL = 300   
NOHITTIME = 0.15    # invicible time
MAXHEALTH = 20  

NUMSENEMY = 10
NUMSGOBLINMAGE = 2
NUMSWOLF = 1
ENEMYMINSPEED = 3
ENEMYMAXSPEED = 7
DIRCHANGEFREQ = 2 # direction change frequency - ako casto sa enemy pohybuju nahodne do novej strany ??div110: netusim co to je
ENEMYHEALTH = 1

NUMSOFTREES = 3 
MAXOFFSCREENPOS = 200 # max distance (in pixels??) of a object



def main():
    """initialize pygame, load images, start the game loop"""
    global FPSCLOCK, DISPLAYSURF, BASICFONT, BASICFONTLARGE, NUMSOFTREES
    global main_character, RHEROIMG, LHEROIMG, LENEMYIMG, RENEMYIMG, TREEIMG, treeimgheight, treeimgwidth,grass_tile_size, GRASSIMG, HEARTIMG, RBLACKHEARTIMG, LBLACKHEARTIMG
    global RSWORDPARTICLES, LSWORDPARTICLES, R2HEROIMG,L2HEROIMG, R3HEROIMG, L3HEROIMG, LGOBLINMAGEIMG, RGOBLINMAGEIMG, LSMALLGOBLINIMG, RSMALLGOBLINIMG
    global RWOLF, LWOLF, RHEROMAGEIMG, LHEROMAGEIMG, MANUALIMG, RHEROMAGEATTIMG, LHEROMAGEATTIMG, RMAGEPROJEKTIL, LMAGEPROJEKTIL, no_key_pressed
    global BOSSIMG, BOSSBARIERIMG, BOSSPILLAR, BOSSGRASSIMG, LBOSSPROJEKTIL,  RBOSSPROJEKTIL, GRASSIMG2
    
    #initialize pygame
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT))
    pygame.display.set_caption('2DM')

    #load font
    BASICFONT = pygame.font.Font('freesansbold.ttf', 32)
    BASICFONTLARGE = pygame.font.Font('freesansbold.ttf', 128)

    #load and scale all images
    # hero imgs:
    RHEROIMG = pygame.image.load('graphics/hero_img/hero_v3.png') #load basic hero with sword image
    RHEROIMG = pygame.transform.scale(RHEROIMG,(100, 100))
    LHEROIMG = pygame.transform.flip(RHEROIMG, True, False)

    R2HEROIMG = pygame.image.load('graphics/hero_img/sword_up_hero.png') #load hero with sword pointing up image
    R2HEROIMG = pygame.transform.scale(R2HEROIMG,(100, 100))
    L2HEROIMG = pygame.transform.flip(R2HEROIMG, True, False)

    R3HEROIMG = pygame.image.load('graphics/hero_img/sword_down_hero.png') #load hero with sword pointing down image
    R3HEROIMG = pygame.transform.scale(R3HEROIMG,(100, 100))
    L3HEROIMG = pygame.transform.flip(R3HEROIMG, True, False)

    RHEROMAGEIMG = pygame.image.load('graphics/hero_img/hero_mage.png') #load basic hero with mage wand image
    RHEROMAGEIMG = pygame.transform.scale(RHEROMAGEIMG,(100, 100))
    LHEROMAGEIMG = pygame.transform.flip(RHEROMAGEIMG, True, False)

    RHEROMAGEATTIMG = pygame.image.load('graphics/hero_img/hero_mage_attack.png') # load hero with mage wand in attacking mode image
    RHEROMAGEATTIMG = pygame.transform.scale(RHEROMAGEATTIMG,(120, 120))
    LHEROMAGEATTIMG = pygame.transform.flip(RHEROMAGEATTIMG, True, False)

    #enemy imgs:
    LENEMYIMG = pygame.image.load('graphics/enemies_img/skull_enemy.png') # load basic enemy image
    LENEMYIMG = pygame.transform.scale(LENEMYIMG,(130, 100))
    RENEMYIMG = pygame.transform.flip(LENEMYIMG,True, False)

    LGOBLINMAGEIMG = pygame.image.load('graphics/enemies_img/goblin_mage.png') # load goblin mage image
    LGOBLINMAGEIMG = pygame.transform.scale(LGOBLINMAGEIMG,(80, 120))
    RGOBLINMAGEIMG = pygame.transform.flip(LGOBLINMAGEIMG,True, False)

    LSMALLGOBLINIMG = pygame.image.load('graphics/enemies_img/small_goblin_v2.png') # load small goblin image
    LSMALLGOBLINIMG = pygame.transform.scale(LSMALLGOBLINIMG,(80, 80))
    RSMALLGOBLINIMG = pygame.transform.flip(LSMALLGOBLINIMG,True, False)
    
    RWOLF = pygame.image.load('graphics/enemies_img/wolf.png') # load wolf image
    RWOLF = pygame.transform.scale(RWOLF,(100,100))
    LWOLF = pygame.transform.flip(RWOLF,True,False)

    #objs imgs
    TREEIMG = pygame.image.load('graphics/other_img/tree_v2.png') # load tree image
    TREEIMG = pygame.transform.scale(TREEIMG, (250,250))

    # other imgs
    GRASSIMG = pygame.image.load('graphics/other_img/grass_v8.png') # load grass image
    GRASSIMG = pygame.transform.scale(GRASSIMG,(WINWIDTH,WINWIDTH))

    GRASSIMG2 = pygame.image.load('graphics/other_img/grass_v8.png') # load grass image
    GRASSIMG2 = pygame.transform.scale(GRASSIMG2,(WINWIDTH,WINWIDTH))

    BOSSGRASSIMG = pygame.image.load('graphics/other_img/boss_stage_grass_v2.png')
    BOSSGRASSIMG = pygame.transform.scale(BOSSGRASSIMG,(WINWIDTH,WINWIDTH))

    MANUALIMG = pygame.image.load('graphics/other_img/manual.png') # load manual image
    MANUALIMG = pygame.transform.scale(MANUALIMG,(250,200))

    #heats imgs
    HEARTIMG = pygame.image.load('graphics/hero_img/heart.png') # load red full heart image
    HEARTIMG = pygame.transform.scale(HEARTIMG, (20,20))
    RBLACKHEARTIMG = pygame.image.load('graphics/hero_img/black_heart_r.png') # load half of black heart image
    RBLACKHEARTIMG = pygame.transform.scale(RBLACKHEARTIMG, (20,20))
    LBLACKHEARTIMG = pygame.transform.flip(RBLACKHEARTIMG, True, False)

    #animations imgs
    RMAGEPROJEKTIL = pygame.image.load('graphics/hero_img/hero_mage_projektil.png') # load fireshot projectile image
    RMAGEPROJEKTIL = pygame.transform.scale(RMAGEPROJEKTIL, (50,50) )
    LMAGEPROJEKTIL = pygame.transform.flip(RMAGEPROJEKTIL, True, False)

    LBOSSPROJEKTIL = pygame.image.load('graphics/enemies_img/boss_fire_projectile_shot.png') # load fireshot projectile image
    LBOSSPROJEKTIL = pygame.transform.scale(LBOSSPROJEKTIL, (200,200) )
    RBOSSPROJEKTIL = pygame.transform.flip(LBOSSPROJEKTIL, True, False)


    RSWORDPARTICLES = pygame.image.load('graphics/hero_img/sword_particles.png') # load swordparticles image
    RSWORDPARTICLES = pygame.transform.scale(RSWORDPARTICLES, (120,180) )
    LSWORDPARTICLES = pygame.transform.flip(RSWORDPARTICLES, True, False)

    #boss stage imgs

    BOSSIMG = pygame.image.load('graphics/enemies_img/boss_without_barier.png') # load boss  imge
    BOSSIMG = pygame.transform.scale(BOSSIMG,(300, 300))

    BOSSBARIERIMG = pygame.image.load('graphics/enemies_img/boss_with_barier.png') # load boss barier image
    BOSSBARIERIMG = pygame.transform.scale(BOSSBARIERIMG,(350, 350))

    BOSSPILLAR = pygame.image.load('graphics/enemies_img/boss_pilar.png') # load boss pillar img
    BOSSPILLAR = pygame.transform.scale(BOSSPILLAR,(120, 120))

    # calculate objects width/height
    treeimgwidth = TREEIMG.get_width()
    treeimgheight = TREEIMG.get_height()
    grass_tile_size = GRASSIMG.get_width()

    

    no_key_pressed = True
    

    #enter the game loop
    while True:
        run_game()

def run_game():
    """prepare game, reset game state, spawn objects, run game"""
    # initial values are set to defaul for easy reset
    global FPSCLOCK, DISPLAYSURF, main_character, NUMSOFTREES, NUMSENEMY, GRASSIMG
    global moveDown, moveLeft, moveRight, moveUp, camera_x, camera_y, attackKey
    global gameOverMode, winMode, immortalityMode, immortalityStartTime, trees_objs, enemy1, enemy1_objs, goblinmage1_objs, smallgoblin1_objs, fire_shot_objs, wolf_objs
    global enemy_level_multiplayer, current_max_enemy, current_killed_enemy, current_max_goblinmage, current_goblinmage_killed, pause, boss_stage_unlocked
    
    #reset stats and time
    immortalityMode = False
    immortalityStartTime = 0
    gameOverMode = False        
    winMode = False     

    GRASSIMG = GRASSIMG2
    # reset camera
    camera_x = 0
    camera_y = 0

    #initialize lists for objects
    enemy1_objs = []
    goblinmage1_objs = []
    smallgoblin1_objs = []
    fire_shot_objs = []
    wolf_objs = []

    # creating a Player Character
    main_character = Hero(RHEROIMG, HALFWINWIDTH, HALFWINHEIGHT, STARTLEVEL, MAXHEALTH , HEARTIMG, RBLACKHEARTIMG, LBLACKHEARTIMG, RHEROMAGEIMG, LHEROMAGEIMG, LHEROIMG, Fire_Shot,
                          RMAGEPROJEKTIL, LMAGEPROJEKTIL)
    

    # reset movement
    moveLeft = False
    moveRight = False  
    moveUp = False
    moveDown = False
    attackKey = False
    boss_stage_unlocked = False
    
    #reset level
    enemy_level_multiplayer = 1.02
    current_max_enemy = NUMSENEMY
    current_max_goblinmage = NUMSGOBLINMAGE
    current_max_wolf = NUMSWOLF
    current_killed_enemy = 0
    current_goblinmage_killed = 0
    pause = 0
    # spawn initial enemies
    # basic enemy enemy
    for enemy1 in range(NUMSENEMY):
        enemy1= Enemy(LENEMYIMG,RENEMYIMG,0,0,5,20)
        enemy1.get_random_position_off_screen(moveUp, moveDown, moveLeft, moveRight, MAXOFFSCREENPOS, WINWIDTH, WINHEIGHT)
        enemy1_objs.append(enemy1)
    # goblin mage enemy
    for goblinmage1 in range(NUMSGOBLINMAGE):
        goblinmage1= Goblin_Mage(LGOBLINMAGEIMG,RGOBLINMAGEIMG,0,0,3,20, Small_Goblin, LSMALLGOBLINIMG, RSMALLGOBLINIMG)
        goblinmage1.get_random_position_off_screen(moveUp, moveDown, moveLeft, moveRight, MAXOFFSCREENPOS, WINWIDTH, WINHEIGHT)
        goblinmage1_objs.append(goblinmage1)

    #wolf enemy
    for wolf in range(NUMSWOLF):
        wolf = Wolf(LWOLF,RWOLF,0,0,1,5)
        wolf.get_random_position_off_screen(moveUp, moveDown, moveLeft, moveRight, MAXOFFSCREENPOS, WINWIDTH, WINHEIGHT)
        wolf_objs.append(wolf)


    #draw background
    #draw grass floor
    start_x = -camera_x % grass_tile_size - grass_tile_size
    start_y = -camera_y % grass_tile_size - grass_tile_size

    for x in range(start_x, WINWIDTH + grass_tile_size, grass_tile_size):
        for y in range(start_y, WINHEIGHT + grass_tile_size, grass_tile_size):
            DISPLAYSURF.blit(GRASSIMG, (x, y))

    #generate trees
    trees_objs = []
    for i in range(0, NUMSOFTREES):
            tree = Tree(TREEIMG, 0, 0, treeimgwidth, treeimgheight)
            tree.get_random_position(MAXOFFSCREENPOS, WINWIDTH, WINHEIGHT)
            trees_objs.append((tree))

    # draw trees
    draw_trees(trees_objs)

    # draw player and health bar
    draw_hero(main_character,camera_x,camera_y,attackKey)
    main_character.draw_health_bar(DISPLAYSURF)


    # draw start screen
    start_screen()


    global hero_collision
    hero_collision = False

    """core game loop"""    
    while True:
        # update players values and movement
        if hero_collision == False:
            if moveLeft:
                main_character.position_x -= MOVERATE
            if moveRight:
                main_character.position_x += MOVERATE
            if moveUp:
                main_character.position_y -= MOVERATE
            if moveDown:
                main_character.position_y += MOVERATE
            
        # checking for invicible mode and exit if its time
        if immortalityMode and time.time() - immortalityStartTime > NOHITTIME:
            immortalityMode = False

        # checking for deleting objects if they are outside of screen area
        for (tree) in trees_objs:
            if tree.is_off_screen(camera_x, camera_y, MAXOFFSCREENPOS, WINWIDTH, WINHEIGHT):
                trees_objs.remove(tree)

        # generate new objects if there is less than needed
        # generate new trees
        while len(trees_objs) < NUMSOFTREES:
            t = generate_new_tree()
            trees_objs.append(t)

        #check for pause before waves
        if pause == 0:
            # generate new basic enemy
            while len(enemy1_objs) < current_max_enemy and len(enemy1_objs) < (current_max_enemy - current_killed_enemy):
                enemy1= Enemy(LENEMYIMG,RENEMYIMG,0+camera_x,0+camera_y,5,20)
                enemy1.get_random_position_off_screen(moveUp, moveDown, moveLeft, moveRight, MAXOFFSCREENPOS, WINWIDTH, WINHEIGHT)
                enemy1.position_x += camera_x
                enemy1.position_y += camera_y
                enemy1_objs.append(enemy1)

            # generate new goblin mages
            while len(goblinmage1_objs) < current_max_goblinmage and len(goblinmage1_objs) < (current_max_goblinmage - current_goblinmage_killed):
                goblinmage1= Goblin_Mage(LGOBLINMAGEIMG,RGOBLINMAGEIMG,0,0,3,20, Small_Goblin, LSMALLGOBLINIMG,RSMALLGOBLINIMG)
                goblinmage1.get_random_position_off_screen(moveUp, moveDown, moveLeft, moveRight, MAXOFFSCREENPOS, WINWIDTH, WINHEIGHT)
                goblinmage1.position_x += camera_x
                goblinmage1.position_y += camera_y
                goblinmage1_objs.append(goblinmage1)


        ## adding more objects

        # draw background
        draw_background()

        # draw trees
        draw_trees(trees_objs)

        # draw player and health bar
        draw_hero(main_character,camera_x,camera_y,attackKey)
        main_character.draw_health_bar(DISPLAYSURF)

        # check for collision between enemies and fireshot projectiles
        for (fireshot1) in fire_shot_objs:
            current_killed_enemy = check_for_fire_shot_collision(main_character, fireshot1, fireshot1.image,enemy1_objs, current_killed_enemy)
            check_for_fire_shot_collision(main_character, fireshot1, fireshot1.image,smallgoblin1_objs)
            current_goblinmage_killed = check_for_fire_shot_collision(main_character, fireshot1, fireshot1.image,goblinmage1_objs, current_goblinmage_killed)

        #draw basic enemie
        for (enemy1) in enemy1_objs:
            draw_entity(enemy1, camera_x, camera_y)
            enemy1.move(main_character.position_x,main_character.position_y)

        #draw wolf
        for wolf in wolf_objs:
            draw_entity(wolf, camera_x, camera_y)
            wolf.move(main_character.position_x, main_character.position_y)

        ##draw_entity(wolf, camera_x, camera_y)
        ##wolf.move(main_character.position_x, main_character.position_y)
        
        # draw goblin mage and spawn new small goblins if its time
        for (goblinmage1) in goblinmage1_objs:
            draw_entity(goblinmage1, camera_x, camera_y)
            goblinmage1.move(main_character.position_x,main_character.position_y)
            goblinmage1.update() # updating time in goblinmage
            if len(smallgoblin1_objs) >= len(goblinmage1_objs)*5: # if there is less than 16 small goblins spawning new if goblinmage reached time for new spawn
                break
            for (smallgoblin1) in goblinmage1.small_goblin_objs:
                smallgoblin1_objs.append(smallgoblin1) # adding spawned goblins from goblinmage into the main
            goblinmage1.small_goblin_objs = [] # removing spawned goblins from goblinmage

        # draw small goblins
        for (smallgoblin1) in smallgoblin1_objs:         
            draw_entity(smallgoblin1, camera_x, camera_y)
            smallgoblin1.move(main_character.position_x,main_character.position_y)

        # moving, drawing on display and removing fireshots if it is outside of active area
        for fire_shot1 in fire_shot_objs[:]:
            for move in range(fire_shot1.difficulty):
                if (fire_shot1.position_x < camera_x - 300 or
                    fire_shot1.position_x > camera_x + WINWIDTH + 300 or
                    fire_shot1.position_y < camera_y - 300 or
                    fire_shot1.position_y > camera_y + WINHEIGHT + 300):
                    fire_shot_objs.remove(fire_shot1)
                    break
                draw_entity(fire_shot1, camera_x, camera_y) # draw fireshot
                fire_shot1.move() # move fireshot

        # event handling cycle
        for event in pygame.event.get():
            if event.type == QUIT: # end game and exit program if quitkey was pressed
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
                        main_character.direction = "left"
                    if main_character.image == RHEROMAGEIMG:
                        main_character.image = LHEROMAGEIMG
                        main_character.direction = "left"
                elif event.key in (K_RIGHT, K_d):
                    moveLeft = False
                    moveRight = True
                    #flipping the player right
                    if main_character.image == LHEROIMG:
                        main_character.image = RHEROIMG
                        main_character.direction = "right"
                    if main_character.image == LHEROMAGEIMG:
                        main_character.image = RHEROMAGEIMG
                        main_character.direction = "right"
                elif event.key == K_q: # starts attack
                    attackKey = True
                elif event.key == K_e: # change weapon
                    main_character.change_equipment()
                elif event.key == K_m: # change weapon
                    boss_stage_unlocked = True

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


        
        # player game state update
        # synchronize time inside hero class
        main_character.update()
        # move player


        """
        ## check hero collision with 
        
        hero_collision = False
        heroRect = main_character.get_collision_hero_rect(camera_x, camera_y,moveDown , moveLeft, moveRight, moveUp, MOVERATE)
        for (tree1) in trees_objs:
            treeRect = tree1.get_tree_rect(camera_x, camera_y)      
            if treeRect.colliderect(heroRect):
                hero_collision = True
                moveLeft = False
                moveRight = False
                moveUp = False
                moveDown = False
                
        """
                

        
        #hero movement
        if hero_collision == False:
            moving_hero(main_character, moveLeft, moveRight, moveUp, moveDown) 
        # camera movement
        moving_camera(main_character)
        # scheck for collision between player and enemies and apply damage on player
        check_for_damage()

        ## check if player kill wave and calculate new nums of enemies in new wave
        if(current_killed_enemy >= current_max_enemy) and (current_goblinmage_killed >= current_max_goblinmage):
            pause = 150
            current_killed_enemy = 0
            current_goblinmage_killed = 0
            current_max_enemy = round(NUMSENEMY * (enemy_level_multiplayer**(main_character.level)))
            current_max_goblinmage = round(NUMSGOBLINMAGE * (enemy_level_multiplayer**(main_character.level)))
            main_character.level += 1
        
        if pause > 0:
            pause -= 1
            draw_progress_bar_pause(pause, 150)
            pass
        else:
            draw_progress_bar_round(current_killed_enemy + current_goblinmage_killed, current_max_goblinmage+current_max_enemy)
            
            
        #update display and time
        pygame.display.update()
        FPSCLOCK.tick(FPS)

        if boss_stage_unlocked == True:
            enemy1_objs = []
            goblinmage1_objs = []
            smallgoblin1_objs = []
            fire_shot_objs = []
            trees_objs = []

            boss_stage1()
    

def terminate():
    """quit pygame and exit the program"""
    pygame.quit()
    sys.exit()

def draw_entity(hero, camera_x, camera_y):
    """draw entity on screen(hero,enemies,projektils)"""
    heroRect = hero.image.get_rect()
    heroRect.center = (hero.position_x - camera_x, hero.position_y - camera_y)
    DISPLAYSURF.blit(hero.image, heroRect)

def draw_hero(hero, camera_x, camera_y,attackKey):
    """draw hero on screen and make attack animation if needed"""
    heroRect = hero.image.get_rect() # gets hero rect
    heroRect.center = (hero.position_x - camera_x, hero.position_y - camera_y) # move hero rect on right position
    DISPLAYSURF.blit(hero.image, heroRect) # draw hero on display
    if attackKey == True: # check if hero attacks
            if hero.weapon_mode == "sword": #check if weapon equiped is sword
                hero_attack_sword(main_character) # make attack animation ,generate attack and check for colision between enemy and attack
            elif hero.weapon_mode == "mage": #check if weapon equiped is magewand
                hero_attack_mage(main_character) # make attack animation ,generate new fireshot projectile if its charged


def moving_hero(hero, moveLeft, moveRight, moveUp, moveDown):
    """move hero and adjust camera"""
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

def moving_camera(hero):
    """ensure camera movement when player moved on cameraslack border"""
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
    """spawn new tree off screan and return object"""
    t = Tree(TREEIMG, 0, 0 , treeimgwidth, treeimgheight) # generate new tree
    # move tree offscreen
    x,y = t.get_random_position_off_screen(moveUp, moveDown,moveLeft, moveRight,MAXOFFSCREENPOS, WINWIDTH, WINHEIGHT) 
    t.position_x = camera_x + x
    t.position_y = camera_y + y
    return t # return new off screen tree

def hero_attack_sword(hero):
    """draw sword attack animation on display and check for hits"""
    global current_killed_enemy, current_goblinmage_killed
    if hero.image == hero.rimage_sword: # attack on right side
        hero.image = R2HEROIMG # change hero image to attacking image
        # draw backgroung, enemies, objects, healtbarddd
        draw_background()
        draw_trees(trees_objs)
        for (enemy1) in enemy1_objs:
            draw_entity(enemy1, camera_x, camera_y)
        for (goblinmage1) in goblinmage1_objs:
            draw_entity(goblinmage1, camera_x, camera_y)
        for (smallgoblin1) in smallgoblin1_objs:
            draw_entity(smallgoblin1, camera_x, camera_y)
        if pause > 0:
            draw_progress_bar_pause(pause, 150)
            pass
        else:
            draw_progress_bar_round(current_killed_enemy + current_goblinmage_killed, current_max_goblinmage+current_max_enemy)
        hero.draw_health_bar(DISPLAYSURF)
        draw_entity(hero,camera_x-10,camera_y) # draw hero
        pygame.display.update() # update display
        particlesRect = RSWORDPARTICLES.get_rect() # get swordparticles rect
        particlesRect.center = (hero.position_x+30 - camera_x, hero.position_y - camera_y) # center swordparticles rect on right position
        DISPLAYSURF.blit(RSWORDPARTICLES, particlesRect) # draw swordparticles
        pygame.display.update() # update display
        hero.image = R3HEROIMG # change image to the second attacking image
        # draw backgroung, enemies, objects, healtbar
        draw_background()
        draw_trees(trees_objs)
        for (enemy1) in enemy1_objs:
            draw_entity(enemy1, camera_x, camera_y)
        for (goblinmage1) in goblinmage1_objs:
            draw_entity(goblinmage1, camera_x, camera_y)
        for (smallgoblin1) in smallgoblin1_objs:
            draw_entity(smallgoblin1, camera_x, camera_y)
        if pause > 0:
            draw_progress_bar_pause(pause, 150)
            pass
        else:
            draw_progress_bar_round(current_killed_enemy + current_goblinmage_killed, current_max_goblinmage+current_max_enemy)
        hero.draw_health_bar(DISPLAYSURF)
        draw_entity(hero,camera_x-10,camera_y) # draw hero
        DISPLAYSURF.blit(RSWORDPARTICLES, particlesRect) # draw swordparticles
        pygame.display.update() # update display
        hero.image = hero.rimage_sword # change image back to normal
        # check for collision between swordparticles and lists of enemies
        current_killed_enemy = check_for_attack_collision(hero, RSWORDPARTICLES, +30, enemy1_objs, current_killed_enemy)
        current_goblinmage_killed = check_for_attack_collision(hero, RSWORDPARTICLES, +30, goblinmage1_objs, current_goblinmage_killed)
        check_for_attack_collision(hero, RSWORDPARTICLES, +30, smallgoblin1_objs, 0)
                

    if hero.image == hero.limage_sword: # attack on left side
        hero.image = L2HEROIMG  # change hero image to attacking image
         # draw backgroung, enemies, objects, healtbar
        draw_background()
        draw_trees(trees_objs)
        for (enemy1) in enemy1_objs:
            draw_entity(enemy1, camera_x, camera_y)
        for (goblinmage1) in goblinmage1_objs:
            draw_entity(goblinmage1, camera_x, camera_y)
        for (smallgoblin1) in smallgoblin1_objs:
            draw_entity(smallgoblin1, camera_x, camera_y)
        if pause > 0:
            draw_progress_bar_pause(pause, 150)
            pass
        else:
            draw_progress_bar_round(current_killed_enemy + current_goblinmage_killed, current_max_goblinmage+current_max_enemy)
        hero.draw_health_bar(DISPLAYSURF)
        draw_entity(hero,camera_x-10,camera_y) # draw hero
        pygame.display.update()# update display
        particlesRect = LSWORDPARTICLES.get_rect() # get swordparticles rect
        particlesRect.center = (hero.position_x-30 - camera_x, hero.position_y - camera_y) # center swordparticles rect on right position
        DISPLAYSURF.blit(LSWORDPARTICLES, particlesRect)  # draw swordparticles
        pygame.display.update()
        hero.image = L3HEROIMG# change image to the second attacking image
        # draw backgroung, enemies, objects, healtbar
        draw_background()
        draw_trees(trees_objs)
        for (enemy1) in enemy1_objs:
            draw_entity(enemy1, camera_x, camera_y)
        for (goblinmage1) in goblinmage1_objs:
            draw_entity(goblinmage1, camera_x, camera_y)
        for (smallgoblin1) in smallgoblin1_objs:
            draw_entity(smallgoblin1, camera_x, camera_y)
        if pause > 0:
            draw_progress_bar_pause(pause, 150)
            pass
        else:
            draw_progress_bar_round(current_killed_enemy + current_goblinmage_killed, current_max_goblinmage+current_max_enemy)
        hero.draw_health_bar(DISPLAYSURF)
        draw_entity(hero,camera_x-10,camera_y) # draw hero
        DISPLAYSURF.blit(LSWORDPARTICLES, particlesRect) # draw swordparticles
        pygame.display.update() # update display
        hero.image = hero.limage_sword  # change image back to normal
          # check for collision between swordparticles and lists of enemies
        current_killed_enemy = check_for_attack_collision(hero, LSWORDPARTICLES, -30, enemy1_objs, current_killed_enemy)
        current_goblinmage_killed = check_for_attack_collision(hero, LSWORDPARTICLES, -30, goblinmage1_objs, current_goblinmage_killed)
        check_for_attack_collision(hero, RSWORDPARTICLES, -30, smallgoblin1_objs, 0)

        
    pass

def hero_attack_mage(hero):
    """draw mage projektil attack animation on display and check for hits"""
    if hero.fire_shot_charged: # check if fireshot attack is charged
        if hero.image == hero.rimage_mage: # shot projectile on right side
            hero.image = RHEROMAGEATTIMG # change hero image to attacking image
            # draw backgroung, enemies, objects, healtbar
            draw_background() 
            draw_trees(trees_objs)
            for (enemy1) in enemy1_objs:
                draw_entity(enemy1, camera_x, camera_y)
            for (goblinmage1) in goblinmage1_objs:
                draw_entity(goblinmage1, camera_x, camera_y)
            for (smallgoblin1) in smallgoblin1_objs:
                draw_entity(smallgoblin1, camera_x, camera_y)
            if pause > 0:
                draw_progress_bar_pause(pause, 150)
                pass
            else:
                draw_progress_bar_round(current_killed_enemy + current_goblinmage_killed, current_max_goblinmage+current_max_enemy)
            hero.draw_health_bar(DISPLAYSURF)
            draw_entity(hero,camera_x-10,camera_y) # draw hero
            pygame.display.update() # display update # time delay
            fire_shot_objs1 = hero.generate_fire_shot() # generate fireshot
            fire_shot_objs.append(fire_shot_objs1) # transfer fireshot
            draw_entity(fire_shot_objs1,camera_x,camera_y) # draw fireshot
            pygame.display.update() 
            draw_background() 
            # draw backgroung, enemies, objects, healtbar
            draw_trees(trees_objs)
            for (enemy1) in enemy1_objs:
                draw_entity(enemy1, camera_x, camera_y)
            for (goblinmage1) in goblinmage1_objs:
                draw_entity(goblinmage1, camera_x, camera_y)
            for (smallgoblin1) in smallgoblin1_objs:
                draw_entity(smallgoblin1, camera_x, camera_y)
            if pause > 0:
                draw_progress_bar_pause(pause, 150)
                pass
            else:
                draw_progress_bar_round(current_killed_enemy + current_goblinmage_killed, current_max_goblinmage+current_max_enemy)
            hero.draw_health_bar(DISPLAYSURF)
            draw_entity(hero,camera_x-10,camera_y) # draw hero
            pygame.display.update()
            hero.image = hero.rimage_mage # change hero image back to normal

        if hero.image == hero.limage_mage: # shot projectile on left side
            hero.image = LHEROMAGEATTIMG # change hero image to attacking image
             # draw backgroung, enemies, objects, healtbar
            draw_background()
            draw_trees(trees_objs)
            for (enemy1) in enemy1_objs:
                draw_entity(enemy1, camera_x, camera_y)
            for (goblinmage1) in goblinmage1_objs:
                draw_entity(goblinmage1, camera_x, camera_y)
            for (smallgoblin1) in smallgoblin1_objs:
                draw_entity(smallgoblin1, camera_x, camera_y)
            if pause > 0:
                draw_progress_bar_pause(pause, 150)
                pass
            else:
                draw_progress_bar_round(current_killed_enemy + current_goblinmage_killed, current_max_goblinmage+current_max_enemy)
            hero.draw_health_bar(DISPLAYSURF)
            draw_entity(hero,camera_x-10,camera_y) # draw hero
            pygame.display.update() # display update# time delay
            fire_shot_objs1 = hero.generate_fire_shot()# generate fireshot
            fire_shot_objs.append(fire_shot_objs1) # transfer fireshot
            draw_entity(fire_shot_objs1,camera_x,camera_y) # draw fireshot
            pygame.display.update()
            # draw backgroung, enemies, objects, healtbar
            draw_background()
            draw_trees(trees_objs)
            for (enemy1) in enemy1_objs:
                draw_entity(enemy1, camera_x, camera_y)
            for (goblinmage1) in goblinmage1_objs:
                draw_entity(goblinmage1, camera_x, camera_y)
            for (smallgoblin1) in smallgoblin1_objs:
                draw_entity(smallgoblin1, camera_x, camera_y)
            if pause > 0:
                draw_progress_bar_pause(pause, 150)
                pass
            else:
                draw_progress_bar_round(current_killed_enemy + current_goblinmage_killed, current_max_goblinmage+current_max_enemy)
            hero.draw_health_bar(DISPLAYSURF)
            draw_entity(hero,camera_x-10,camera_y)
            pygame.display.update()
            hero.image = hero.limage_mage # change hero image back to normal
        pass

def check_for_attack_collision(hero, SWORDPARTICLES, z_value, enemy_obj, killed):
    """check for collision between swordparticles and enemies"""
    # get particles width, height and rect
    particles_width = SWORDPARTICLES.get_width()
    particles_height = SWORDPARTICLES.get_height()
    particlesRect = pygame.Rect(hero.position_x + z_value -camera_x - particles_width//2,hero.position_y-camera_y-particles_height//2, particles_width, particles_height)
    # check for collision between lists of enemies and swordparticles 
    for (enemy) in enemy_obj:
        enemyRect = enemy.get_enemy_rect(camera_x,camera_y)
        if particlesRect.colliderect(enemyRect):
            enemy.is_hit(main_character.position_x,main_character.position_y, 1)# apply damage on enemy
            if enemy.current_health <= 0: # check if enemy gets killed
                killed += 1 # level up hero
                enemy_obj.remove(enemy)# remove enemy 
                if hero.current_health < hero.max_health:
                    hero.current_health += 1# heal hero
    return killed

def check_for_fire_shot_collision(hero,fireshot1, FIRESHOT, enemy_obj, count = 0):
    """check for collision between fireshot projectile and enemies"""
    # get fireshot width, height and rect
    fireshot1_width = FIRESHOT.get_width()
    fireshot1_height = FIRESHOT.get_height()
    fireshot1Rect = pygame.Rect(fireshot1.position_x-camera_x - fireshot1_width//2,fireshot1.position_y-camera_y-fireshot1_height//2, fireshot1_width, fireshot1_height) 
    # check for collision between lists of enemies and fireshot projectile
    for (enemy) in enemy_obj:
        enemyRect = enemy.get_enemy_rect(camera_x,camera_y)
        if fireshot1Rect.colliderect(enemyRect):
            enemy.is_hit(main_character.position_x,main_character.position_y, 1) # apply damage on enemy
            if enemy.current_health == 0: # check if enemy gets killed
                count += 1 # level up hero
                enemy_obj.remove(enemy) # remove enemy
                if hero.current_health < hero.max_health:
                    hero.current_health += 1 # heal hero
           
    return count

def draw_background():
    """draw 3x3 square background around player"""
    start_x = -camera_x % grass_tile_size - grass_tile_size
    start_y = -camera_y % grass_tile_size - grass_tile_size

    for x in range(start_x, WINWIDTH + grass_tile_size, grass_tile_size):
        for y in range(start_y, WINHEIGHT + grass_tile_size, grass_tile_size):
            DISPLAYSURF.blit(GRASSIMG, (x, y))
    pass

def draw_trees(trees_objs):
    """draw all trees on display from list"""
    for tree in trees_objs:
        treeRect = tree.image.get_rect() 
        treeRect.center = (tree.position_x - camera_x, tree.position_y - camera_y)
        DISPLAYSURF.blit(tree.image, treeRect)
    pass

def check_for_damage():
    """check for collision between hero and enemy and apply damage"""
    global immortalityStartTime, immortalityMode
    if immortalityMode == True: # if player have immortality mode damage does not apply on him
        return
    heroRect = main_character.get_hero_hitbox(camera_x, camera_y) # gets hero rect
    #check for collision between basic enemies and hero
    for (enemy1) in enemy1_objs:
        enemyRect = enemy1.get_enemy_attackbox(camera_x,camera_y) # gets enemy rect
        if heroRect.colliderect(enemyRect):
            main_character.current_health -= 1 # apply damage on player
            if main_character.is_alive() == False: # turn game over if hero health gets to zero
               game_over() 
            immortalityStartTime = time.time() # if player gets hit he gets 0.2 second immortality
            immortalityMode = True
            break
    #check for collision between small goblins and hero
    for (smallgoblin1) in smallgoblin1_objs:
        enemyRect = smallgoblin1.get_enemy_attackbox(camera_x,camera_y) # gets enemy rect
        if heroRect.colliderect(enemyRect):
            main_character.current_health -= 1 # apply damage on player
            if main_character.is_alive() == False:  # turn game over if hero health gets to zero
               game_over() 
            immortalityStartTime = time.time() # if player gets hit he gets 0.2 second immortality
            immortalityMode = True
            return
    
def start_screen():
    global no_key_pressed

    start_new_game_surface = BASICFONT.render("START",False, WHITE)
    #pygame.draw.rect(DISPLAYSURF,(128,128,128), (WINWIDTH//2-150, 0, 300,42))
    DISPLAYSURF.blit(start_new_game_surface,(WINWIDTH//2-65 + 5, 110 + 5))
    start_new_game_surface = BASICFONT.render("NEW  GAME",False, WHITE)
    #pygame.draw.rect(DISPLAYSURF,(128,128,128), (WINWIDTH//2-150, 50, 300,42))
    DISPLAYSURF.blit(start_new_game_surface,(WINWIDTH//2-110 + 5, 150 + 5))

    button("   PLAY", WINWIDTH//2-81, 200,WHITE,(128,128,128), 145, 42)
    DISPLAYSURF.blit(MANUALIMG,(710,525))
    while no_key_pressed:
        pygame.display.update()  
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                terminate()
            if event.type == MOUSEMOTION:
                mouse_x = pygame.mouse.get_pos()[0]
                mouse_y = pygame.mouse.get_pos()[1]
                
                if (WINWIDTH//2-81 < mouse_x < WINWIDTH//2+59) and (200 < mouse_y < 242):
                    button("   PLAY", WINWIDTH//2-81, 200,(128,128,128),WHITE, 145, 42)
                else:
                    button("   PLAY", WINWIDTH//2-81, 200,WHITE,(128,128,128), 145, 42)
            
            if event.type == MOUSEBUTTONUP:
                mouse_x = pygame.mouse.get_pos()[0]
                mouse_y = pygame.mouse.get_pos()[1]
                if (WINWIDTH//2-81 < mouse_x < WINWIDTH//2+59) and (200 < mouse_y < 242):
                    no_key_pressed = False
            if event.type == KEYDOWN:
                if event.key in (K_UP, K_w):
                    no_key_pressed = False
                elif event.key in (K_DOWN, K_s):
                    no_key_pressed = False
                elif event.key in (K_LEFT, K_a):
                    no_key_pressed = False
                elif event.key in (K_RIGHT, K_d):
                    no_key_pressed = False
                elif event.key == K_q:
                    no_key_pressed = False
                elif event.key == K_e:
                    no_key_pressed = False


    pass

def game_over():
    """display game over screen with quit and reset option"""
    main_character.position_x = 175
    main_character.position_y = 275
    DISPLAYSURF.fill(BLACK)
    text_surface = BASICFONTLARGE.render("Game Over",False,WHITE)
    level_surface = BASICFONT.render(f"Level achieved: {main_character.level}", False, WHITE)
    DISPLAYSURF.blit(text_surface,(125,50))
    DISPLAYSURF.blit(level_surface,(240,255))
    DISPLAYSURF.blit(MANUALIMG,(700,500))
    draw_hero(main_character,0,0,False)

    button("Try Again", 100, 550,WHITE,DARKGREEN, 162, 42)
    button("Quit", 2*HALFWINWIDTH-450,550,WHITE,DARKRED, 162, 42)

    try:
        get_qr(f"Hero level: {main_character.level}") # More info in the future (max wave, max hps, etc...)
        QRIMAGE = pygame.image.load('last_score/qr.png')
        DISPLAYSURF.blit(QRIMAGE,(575,175)) 
    except:
        pass
    
    while True:
        pygame.display.update()  
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                terminate()
            if event.type == MOUSEMOTION:
                mouse_x = pygame.mouse.get_pos()[0]
                mouse_y = pygame.mouse.get_pos()[1]
                

                if (100 < mouse_x < 262) and (550 < mouse_y < 592):
                    button("Try Again", 100, 550,DARKGREEN,WHITE, 162, 42)
                else:
                    button("Try Again", 100, 550, WHITE,DARKGREEN, 162, 42)

                if (2*HALFWINWIDTH-450 < mouse_x < 2*HALFWINWIDTH-288) and (550 < mouse_y < 592):
                    button("Quit", 2*HALFWINWIDTH-450,550,DARKRED,WHITE, 162, 42)
                else:
                    button("Quit", 2*HALFWINWIDTH-450,550,WHITE,DARKRED, 162, 42)

            #                if ()
            
            if event.type == MOUSEBUTTONUP:
                mouse_x = pygame.mouse.get_pos()[0]
                mouse_y = pygame.mouse.get_pos()[1]
                if (100 < mouse_x < 262) and (550 < mouse_y < 592):
                    run_game() # not sure of the recursion 
                    return
                elif (960-450 < mouse_x < 940-288) and (550 < mouse_y < 592):
                    terminate()

    
def button(text, position_x, position_y, COLOR, BACKGROUND, width, height):
    """draw button with text and ability to click on"""
    try_again_surface = BASICFONT.render(text,False, COLOR)
    pygame.draw.rect(DISPLAYSURF,BACKGROUND, (position_x, position_y, width, height))
    DISPLAYSURF.blit(try_again_surface,(position_x + 5, position_y + 5))
    
def draw_progress_bar_round(count, max):
    """draw progress bar on display"""
    pygame.draw.rect(DISPLAYSURF, (0,0,0),(WINWIDTH - 3 *240, 10, WINWIDTH/2, 20))
    pygame.draw.rect(DISPLAYSURF, (0,255,0),(WINWIDTH - 3 *240+5, 10+5, (WINWIDTH/2-10)*(max-count)/max, 20-10))
 
def draw_progress_bar_pause(count, max):
    """draw pause bar on display"""
    pygame.draw.rect(DISPLAYSURF, (0,0,0),(WINWIDTH - 3 *240, 10, WINWIDTH/2, 20))
    pygame.draw.rect(DISPLAYSURF, (0,0,255),(WINWIDTH - 3 *240+5, 10+5, (WINWIDTH/2-10)*(max-count)/max, 20-10))

def boss_stage1():
    """boss stage - its not done yet"""
    global demon_lord1, magic_pillars_obj, fire_shot_objs,boss_fire_shot_objs, GRASSIMG
    immortalityMode = False

    fire_shot_objs = []
    boss_fire_shot_objs = []
    # reset camera
    camera_x = 0
    camera_y = 0

    main_character.position_x = HALFWINWIDTH
    main_character.position_y = HALFWINHEIGHT
    if main_character.weapon_mode == "sword":
        main_character.change_equipment()
    
    GRASSIMG = BOSSGRASSIMG

    # reset movement
    moveLeft = False
    moveRight = False  
    moveUp = False
    moveDown = False
    attackKey = False
    demon_lord = Boss(BOSSBARIERIMG, BOSSBARIERIMG, BOSSIMG, 140, HALFWINHEIGHT, 250, Bluefire_Shot, RBOSSPROJEKTIL)
    magic_pillar1 = Magic_Pillar(BOSSPILLAR, 100,100,25)
    magic_pillar2 = Magic_Pillar(BOSSPILLAR, 250,180,25)
    magic_pillar3 = Magic_Pillar(BOSSPILLAR, 100,650,25)
    magic_pillar4 = Magic_Pillar(BOSSPILLAR, 200,600,25)

    demon_lord1 = []
    demon_lord1.append(demon_lord)
    magic_pillars_obj = []
    magic_pillars_obj.append(magic_pillar1)
    magic_pillars_obj.append(magic_pillar2)
    magic_pillars_obj.append(magic_pillar3)
    magic_pillars_obj.append(magic_pillar4)

    hero_collision = False

    """core game loop"""    
    while True:
        # update players values and movement
        if hero_collision == False:
            if moveLeft:
                main_character.position_x -= MOVERATE
            if moveRight:
                main_character.position_x += MOVERATE
            if moveUp:
                main_character.position_y -= MOVERATE
            if moveDown:
                main_character.position_y += MOVERATE
            
        # checking for invicible mode and exit if its time
        if immortalityMode and time.time() - immortalityStartTime > NOHITTIME:
            immortalityMode = False

        # draw background
        draw_background()

        for (demon_lord2) in demon_lord1:
            ##test to see demonlord hitbox
            print(demon_lord2.current_health)
            
            if len(demon_lord2.projectile_objs) > 0:
                boss_fire_shot_objs.append(demon_lord2.projectile_objs[0])
                demon_lord2.projectile_objs = []

            if len(magic_pillars_obj)==0:
                demon_lord2.change_barrier_state()
                magic_pillar1 = Magic_Pillar(BOSSPILLAR, 100,100,25)
                magic_pillar2 = Magic_Pillar(BOSSPILLAR, 250,180,25)
                magic_pillar3 = Magic_Pillar(BOSSPILLAR, 100,650,25)
                magic_pillar4 = Magic_Pillar(BOSSPILLAR, 200,600,25)
                magic_pillars_obj.append(magic_pillar1)
                magic_pillars_obj.append(magic_pillar2)
                magic_pillars_obj.append(magic_pillar3)
                magic_pillars_obj.append(magic_pillar4)

            demon_lord2.update()
            draw_entity(demon_lord2,camera_x, camera_y)

        for (magic_pillar7) in magic_pillars_obj:
            draw_entity(magic_pillar7,camera_x, camera_y)

        for (boss_magic_pillar7) in boss_fire_shot_objs:
            draw_entity(boss_magic_pillar7,camera_x, camera_y)

        # draw player and health bar
        boss_stage_draw_hero(main_character,camera_x,camera_y,attackKey)
        main_character.draw_health_bar(DISPLAYSURF)

        # check for collision between enemies and fireshot projectiles
        for (fireshot1) in fire_shot_objs:
            check_for_fire_shot_collision(main_character, fireshot1, fireshot1.image, demon_lord1)
            check_for_fire_shot_collision(main_character, fireshot1, fireshot1.image, magic_pillars_obj)
            check_for_fire_shot_collision(main_character,fireshot1, fireshot1.image, boss_fire_shot_objs)

        # moving, drawing on display and removing fireshots if it is outside of active area
        for fire_shot1 in fire_shot_objs[:]:
            for move in range(fire_shot1.difficulty):
                if (fire_shot1.position_x < camera_x - 300 or
                    fire_shot1.position_x > camera_x + WINWIDTH + 300 or
                    fire_shot1.position_y < camera_y - 300 or
                    fire_shot1.position_y > camera_y + WINHEIGHT + 300):
                    fire_shot_objs.remove(fire_shot1)
                    break
                draw_entity(fire_shot1, camera_x, camera_y) # draw fireshot
                fire_shot1.move() # move fireshot


        for fire_shot1 in boss_fire_shot_objs[:]:
            for move in range(fire_shot1.difficulty):
                if (fire_shot1.position_x < camera_x - 300 or
                    fire_shot1.position_x > camera_x + WINWIDTH + 300 or
                    fire_shot1.position_y < camera_y - 300 or
                    fire_shot1.position_y > camera_y + WINHEIGHT + 300):
                    boss_fire_shot_objs.remove(fire_shot1)
                    break
                draw_entity(fire_shot1, camera_x, camera_y) # draw fireshot
                fire_shot1.move(main_character.position_x,main_character.position_y) # move fireshot
        # event handling cycle
        for event in pygame.event.get():
            if event.type == QUIT: # end game and exit program if quitkey was pressed
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
                        main_character.direction = "left"
                    if main_character.image == RHEROMAGEIMG:
                        main_character.image = LHEROMAGEIMG
                        main_character.direction = "left"
                elif event.key in (K_RIGHT, K_d):
                    moveLeft = False
                    moveRight = True
                    #flipping the player right
                    if main_character.image == LHEROIMG:
                        main_character.image = RHEROIMG
                        main_character.direction = "right"
                    if main_character.image == LHEROMAGEIMG:
                        main_character.image = RHEROMAGEIMG
                        main_character.direction = "right"
                elif event.key == K_q: # starts attack
                    attackKey = True
                elif event.key == K_e: # change weapon
                    for (demon_lord2) in demon_lord1:
                        demon_lord2.change_barrier_state()
                        

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


        
        # player game state update
        # synchronize time inside hero class
        main_character.update()
        # move player
                
        #hero movement
        if hero_collision == False:
            moving_hero(main_character, moveLeft, moveRight, moveUp, moveDown) 
            pass
        # camera movement
        moving_camera(main_character)
        # scheck for collision between player and enemies and apply damage on player
        check_for_damage()
        
        if len(demon_lord1)==0:
            game_over()
        #update display and time
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def boss_stage_hero_attack_mage(hero):
    """boss stage- draw mage projektil attack animation on display and check for hits"""
    if hero.fire_shot_charged: # check if fireshot attack is charged
        if hero.image == hero.limage_mage: # shot projectile on left side
            fire_shot_objs1 = hero.generate_fire_shot()# generate fireshot
            fire_shot_objs.append(fire_shot_objs1) # transfer fireshot
            draw_entity(fire_shot_objs1,camera_x,camera_y) # draw fireshot
            pygame.display.update()
            hero.image = hero.limage_mage # change hero image back to normal
        pass

def boss_stage_draw_hero(hero, camera_x, camera_y,attackKey):
    """draw hero on screen and make attack animation if needed"""
    heroRect = hero.image.get_rect() # gets hero rect
    heroRect.center = (hero.position_x - camera_x, hero.position_y - camera_y) # move hero rect on right position
    DISPLAYSURF.blit(hero.image, heroRect) # draw hero on display
    if attackKey == True: # check if hero attacks
            if hero.weapon_mode == "mage": #check if weapon equiped is magewand
                boss_stage_hero_attack_mage(main_character) # make attack animation ,generate new fireshot projectile if its charged

"""run main if program gets executed"""
if __name__ == '__main__':
    main()

