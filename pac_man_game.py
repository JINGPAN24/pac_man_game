import os
import sys
import pygame
import random
import def1
from def2 import *

# author : Jingpan Wang
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
SKYBLUE = (0, 191, 255)
BGMPATH = os.path.join(os.getcwd(), 'resources/sounds/bg.mp3')
ICONPATH = os.path.join(os.getcwd(), 'resources/images/icon.png')
FONTPATH = os.path.join(os.getcwd(), 'resources/font/ALGER.TTF')
HEROPATH = os.path.join(os.getcwd(), 'resources/images/pacman.png')
BlinkyPATH = os.path.join(os.getcwd(), 'resources/images/Blinky.png')
ClydePATH = os.path.join(os.getcwd(), 'resources/images/Clyde.png')
InkyPATH = os.path.join(os.getcwd(), 'resources/images/Inky.png')
PinkyPATH = os.path.join(os.getcwd(), 'resources/images/Pinky.png')
fruitPATH = os.path.join(os.getcwd(), 'resources/images/fruit.png')
# author : Shuaicheng Chen
def startLevelGame(level, screen, font):
    clock = pygame.time.Clock()
    SCORE = 0
    wall_sprites = level.setupWalls(PURPLE)
    gate_sprites = level.setupGate(WHITE)
    hero_sprites, ghost_sprites = level.setupPlayers(HEROPATH, [BlinkyPATH, ClydePATH, InkyPATH, PinkyPATH])

    for ghost in ghost_sprites:
        ghost.image = pygame.transform.scale(ghost.image, (16, 16))
        ghost.rect = ghost.image.get_rect(center=ghost.rect.center)

    food_sprites, fruit_sprites = level.setupFood(YELLOW, [fruitPATH])
    is_clearance = False

    if not wall_sprites or not hero_sprites or not ghost_sprites or not food_sprites:
        print("Error: Game elements not properly initialized.")
        return is_clearance

    time_limit = 300
    start_ticks = pygame.time.get_ticks()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(-1)
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    for hero in hero_sprites:
                        hero.changeSpeed([-1, 0])
                        hero.is_move = True
                elif event.key == pygame.K_RIGHT:
                    for hero in hero_sprites:
                        hero.changeSpeed([1, 0])
                        hero.is_move = True
                elif event.key == pygame.K_UP:
                    for hero in hero_sprites:
                        hero.changeSpeed([0, -1])
                        hero.is_move = True
                elif event.key == pygame.K_DOWN:
                    for hero in hero_sprites:
                        hero.changeSpeed([0, 1])
                        hero.is_move = True
            if event.type == pygame.KEYUP:
                if (event.key == pygame.K_LEFT) or (event.key == pygame.K_RIGHT) or (event.key == pygame.K_UP) or (
                        event.key == pygame.K_DOWN):
                    for hero in hero_sprites:
                        hero.is_move = False

        screen.fill(BLACK)

        for hero in hero_sprites:
            hero.update(wall_sprites, gate_sprites)
        hero_sprites.draw(screen)

        for hero in hero_sprites:
            food_eaten = pygame.sprite.spritecollide(hero, food_sprites, True)
            if food_eaten:
                print(f"Eaten food: {len(food_eaten)}")
            SCORE += len(food_eaten) * 10

        for hero in hero_sprites:
            fruit_eaten = pygame.sprite.spritecollide(hero, fruit_sprites, True)
            if fruit_eaten:
                print(f"Eaten fruits: {len(fruit_eaten)}")
            SCORE += len(fruit_eaten) * 100

        wall_sprites.draw(screen)
        gate_sprites.draw(screen)
        food_sprites.draw(screen)
        fruit_sprites.draw(screen)

        for ghost in ghost_sprites:
            ghost.update(wall_sprites, None)

        ghost_sprites.draw(screen)

        score_text = font.render("Score: %s" % SCORE, True, RED)
        screen.blit(score_text, [10, 10])

        seconds = time_limit - (pygame.time.get_ticks() - start_ticks) // 1000
        if seconds <= 0:
            is_clearance = False
            break
        time_text = font.render(f"Time Left: {seconds}s", True, WHITE)
        screen.blit(time_text, [10, 50])

        print(f"Remaining food sprites: {len(food_sprites)}")
        print(f"Remaining fruit sprites: {len(fruit_sprites)}")
        if len(food_sprites) <= 3 and len(fruit_sprites) == 0:
            print("All food and fruits eaten! Level cleared.")
            is_clearance = True
            break

        if pygame.sprite.groupcollide(hero_sprites, ghost_sprites, False, False):
            print("Hero collided with a ghost!")
            is_clearance = False
            break

        pygame.display.flip()
        clock.tick(10)
    return is_clearance


# author : Jingpan Wang
def showText(screen, font, is_clearance, flag=False):
    clock = pygame.time.Clock()
    msg = 'Game Over!' if not is_clearance else 'Congratulations!'
    positions = [[235, 233], [65, 303], [170, 333]] if not is_clearance else [[145, 233], [65, 303], [170, 333]]
    surface = pygame.Surface((400, 200))
    surface.set_alpha(10)
    surface.fill((128, 128, 128))
    screen.blit(surface, (100, 200))
    texts = [font.render(msg, True, WHITE),
             font.render('Press ENTER to continue or play again.', True, WHITE),
             font.render('Press ESCAPE to quit.', True, WHITE)]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if is_clearance:
                        if not flag:
                            return
                        else:
                            main(initialize())
                    else:
                        main(initialize())
                elif event.key == pygame.K_ESCAPE:
                    sys.exit()
                    pygame.quit()
        for idx, (text, position) in enumerate(zip(texts, positions)):
            screen.blit(text, position)
        pygame.display.flip()
        clock.tick(10)

# author : Shuaicheng Chen
def initialize():
    pygame.init()
    icon_image = pygame.image.load(ICONPATH)
    pygame.display.set_icon(icon_image)
    screen = pygame.display.set_mode([606, 606])
    pygame.display.set_caption('Pac-Man')
    return screen

 # author : Shuaicheng Chen
def main(screen):
    pygame.mixer.init()
    pygame.font.init()
    font_small = pygame.font.Font(FONTPATH, 18)
    font_big = pygame.font.Font(FONTPATH, 24)
    for num_level in range(1, def1.NUMLEVELS + 1):
        if num_level == 1:
            level = def1.Level1()
            is_clearance = startLevelGame(level, screen, font_small)
            if num_level == def1.NUMLEVELS:
                showText(screen, font_big, is_clearance, True)
            else:
                showText(screen, font_big, is_clearance)


if __name__ == '__main__':
    main(initialize())
