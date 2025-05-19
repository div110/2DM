import random, sys, time, math, pygame
from pygame.locals import *

from enemies_classes.boss import Boss
from enemies_classes.magic_pillar import Magic_Pillar
from main import draw_background, draw_entity, draw_hero, check_for_fire_shot_collision, terminate, moving_camera, moving_hero, check_for_damage

def boss_stage1(main_character, HALFWINWIDTH, HALFWINHEIGHT, BOSSIMG, BOSSBARIERIMG, BOSSPILLAR, MOVERATE, immortalityStartTime,NOHITTIME,
               DISPLAYSURF, FPS, FPSCLOCK, RHEROIMG ,RHEROMAGEIMG , LHEROIMG ,LHEROMAGEIMG        ):
    """boss stage - its not done yet"""
    global demon_lord1, magic_pillars_obj, fire_shot_objs
    immortalityMode = False

    fire_shot_objs = []
    # reset camera
    camera_x = 0
    camera_y = 0

    main_character.position_x = HALFWINWIDTH
    main_character.position_y = HALFWINHEIGHT
    

    # reset movement
    moveLeft = False
    moveRight = False  
    moveUp = False
    moveDown = False
    attackKey = False
    demon_lord = Boss(BOSSIMG, BOSSBARIERIMG, 130, HALFWINHEIGHT, 200)
    magic_pillar1 = Magic_Pillar(BOSSPILLAR, 100,100,25)
    magic_pillar2 = Magic_Pillar(BOSSPILLAR, 250,200,25)
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
            draw_entity(demon_lord2,camera_x, camera_y)
            #print(demon_lord2.current_health)

        for (magic_pillar7) in magic_pillars_obj:
            draw_entity(magic_pillar7,camera_x, camera_y)

        # draw player and health bar
        draw_hero(main_character,camera_x,camera_y,attackKey)
        main_character.draw_health_bar(DISPLAYSURF)

        # check for collision between enemies and fireshot projectiles
        for (fireshot1) in fire_shot_objs:
            check_for_fire_shot_collision(main_character, fireshot1, fireshot1.image, demon_lord1)
            check_for_fire_shot_collision(main_character, fireshot1, fireshot1.image, magic_pillars_obj)

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
        # camera movement
        moving_camera(main_character)
        # scheck for collision between player and enemies and apply damage on player
        check_for_damage()
        
        #update display and time
        pygame.display.update()
        FPSCLOCK.tick(FPS)