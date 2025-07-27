import pygame
from def2 import *
import random

NUMLEVELS = 1


# author : Kaiyue Wang
class Level1:
    def __init__(self):
        self.info = 'level1'
        self.fruit_image_path = 'resources/images/fruit.png'

    # author : Kaiyue Wang
    def setupWalls(self, wall_color):
        self.wall_sprites = pygame.sprite.Group()
        wall_positions = [[0, 0, 6, 600],
                          [0, 0, 600, 6],
                          [0, 600, 606, 6],
                          [600, 0, 6, 606],
                          [480, 420, 6, 66],
                          [180, 540, 6, 66],
                          [270, 540, 6, 66],
                          [360, 540, 6, 66],
                          [240, 180, 66, 6],
                          [240, 60, 6, 66],
                          [450, 0, 6, 66],
                          [60, 60, 126, 6],
                          [330, 60, 36, 6],
                          [60, 120, 66, 6],
                          [540, 510, 66, 6],
                          [180, 240, 66, 6],
                          [60, 120, 6, 126],
                          [180, 120, 126, 6],
                          [420, 120, 126, 6],
                          [120, 180, 66, 6],
                          [120, 180, 6, 126],
                          [360, 180, 126, 6],
                          [480, 180, 6, 126],
                          [180, 240, 6, 66],
                          [240, 240, 126, 54],
                          [180, 360, 100, 6],
                          [330, 360, 94, 6],
                          [420, 240, 6, 126],
                          [240, 240, 126, 6],
                          [0, 300, 66, 6],
                          [540, 300, 66, 6],
                          [540, 180, 66, 6],
                          [60, 360, 66, 6],
                          [60, 360, 6, 66],
                          [480, 360, 66, 6],
                          [540, 360, 6, 66],
                          [240, 420, 126, 6],
                          [120, 420, 6, 66],
                          [420, 480, 6, 66],
                          [180, 480, 66, 6],
                          [120, 480, 6, 66],
                          ]
        for wall_position in wall_positions:
            wall = Wall(*wall_position, wall_color)
            self.wall_sprites.add(wall)
        return self.wall_sprites

    # author : Kaiyue Wang
    def setupGate(self, gate_color):
        self.gate_sprites = pygame.sprite.Group()
        self.gate_sprites.add(Wall(282, 242, 42, 2, gate_color))
        return self.gate_sprites

    # author : Kaiyue Wang
    def setupPlayers(self, hero_image_path, ghost_images_path):
        self.hero_sprites = pygame.sprite.Group()
        self.ghost_sprites = pygame.sprite.Group()

        self.hero_sprites.add(Player(287, 439, hero_image_path))
        generated_positions = set()
        generated_positions.add((287, 439))

        for each in ghost_images_path[:3]:
            max_attempts = 100
            attempts = 0
            while attempts < max_attempts:
                random_x = random.randint(0, 18) * 30 + 15
                random_y = random.randint(0, 18) * 30 + 15
                if (random_x, random_y) not in generated_positions:
                    ghost = Player(random_x, random_y, each)
                    is_collide = pygame.sprite.spritecollide(ghost, self.wall_sprites, False) or \
                                 pygame.sprite.spritecollide(ghost, self.hero_sprites, False)
                    if not is_collide:
                        generated_positions.add((random_x, random_y))
                        self.ghost_sprites.add(ghost)
                        break
                attempts += 1
        return self.hero_sprites, self.ghost_sprites

    # author : Shuaicheng Chen
    def setupFood(self, food_color, fruit_image_paths):
        self.food_sprites = pygame.sprite.Group()
        self.fruit_sprites = pygame.sprite.Group()

        generated_positions = set()

        if food_color:
            for row in range(19):
                for col in range(19):
                    if (row == 7 or row == 8) and (col == 8 or col == 9 or col == 10):
                        continue
                    else:
                        x, y = 30 * col + 32, 30 * row + 32
                        food = Food(x, y, 6, 6, food_color)
                        is_collide = pygame.sprite.spritecollide(food, self.wall_sprites, False)
                        if not is_collide:
                            self.food_sprites.add(food)
                            generated_positions.add((x, y))

        if fruit_image_paths:
            available_positions = list(generated_positions)
            random.shuffle(available_positions)

            for _ in range(2):
                if available_positions:
                    random_x, random_y = available_positions.pop()

                    for food in self.food_sprites:
                        if food.rect.x == random_x and food.rect.y == random_y:
                            self.food_sprites.remove(food)
                            break

                    fruit = Food(random_x - 10, random_y - 10, 20, 20, None, image_path=self.fruit_image_path)

                    self.fruit_sprites.add(fruit)

        return self.food_sprites, self.fruit_sprites


