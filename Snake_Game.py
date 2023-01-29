
import pygame
import sys
import random
from pygame.math import Vector2


class SCORE:
    def __init__(self):
        # position of the score counters
        self.score_x = 50
        self.score_y = 42
        self.score = 0

        # make the highscore file if it doesn't exist and put a 0 in it
        try:
            self.hi_score_file = open("highscore.txt", "x")
        except FileExistsError:
            pass
        else:
            self.hi_score_file = open("highscore.txt", "w")
            self.hi_score_file.write("0")
            self.hi_score_file.close()

        # find the previous high score
        self.hi_score_file = open("highscore.txt", "r")
        self.hi_score = self.hi_score_file.read()
        self.hi_score_file.close()

    def update_score(self, points):
        self.score += points

    def draw_score(self):
        # set the score text and put it on the screen
        score_text = score_font.render("Score: " + str(self.score), True, (0, 0, 0))
        screen.blit(score_text, (self.score_x, self.score_y))
        # set the high score text and put it on the screen
        hi_score_text = score_font.render("High Score: " + str(self.hi_score), True, (0, 0, 0))
        screen.blit(hi_score_text, (self.score_x, self.score_y + 40))

    def reset(self):
        # determine whether it was a high score or not
        if self.score > int(self.hi_score):
            self.hi_score_file = open("highscore.txt", "w")
            self.hi_score_file.write(str(self.score))
            self.hi_score_file.close()
            self.hi_score = self.score
            self.score = 0
        else:
            self.score = 0


class SNAKE:
    def __init__(self):
        # randomize starting position and direction
        self.start_dir = random.randint(1, 4)
        self.start_x = random.randint(2, cell_number - 3)
        self.start_y = random.randint(2, cell_number - 3)

        # other needed variables
        self.no_move = 0
        # 1 = no going down
        # 2 = no going right
        # 3 = no going up
        # 4 = no going left
        self.body = []
        self.find_snake()
        self.direction = Vector2(0, 0)
        self.new_block = False
        self.can_move = True

    def find_snake(self):
        # determine the position of the snake based on previously randomized variables
        if self.start_dir == 1:
            self.body = [Vector2(self.start_x, self.start_y), Vector2(self.start_x, self.start_y - 1),
                         Vector2(self.start_x, self.start_y - 2)]
            self.no_move = 1
        if self.start_dir == 2:
            self.body = [Vector2(self.start_x, self.start_y), Vector2(self.start_x + 1, self.start_y),
                         Vector2(self.start_x + 2, self.start_y)]
            self.no_move = 2
        if self.start_dir == 3:
            self.body = [Vector2(self.start_x, self.start_y), Vector2(self.start_x, self.start_y + 1),
                         Vector2(self.start_x, self.start_y + 2)]
            self.no_move = 3
        if self.start_dir == 4:
            self.body = [Vector2(self.start_x, self.start_y), Vector2(self.start_x - 1, self.start_y),
                         Vector2(self.start_x - 2, self.start_y)]
            self.no_move = 4

    def draw_snake(self):
        # draw the square at each body part with the head being a special color
        self.head = True
        for block in self.body:
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            if self.head:
                self.head = False
                pygame.draw.rect(screen, (183, 100, 122), block_rect)
            elif not self.head:
                pygame.draw.rect(screen, (183, 111, 122), block_rect)

    def move_snake(self):
        # if new block then inset a new block at index 0 and copy the whole list over
        if self.new_block > 0:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block -= 1
            self.can_move = True
        # otherwise insert a new block at index 0 and copy all but the last index
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.can_move = True

    def add_block(self, amount):
        self.new_block = amount

    def reset(self):
        # re-randomize the pos variables and find the snake again
        self.direction = Vector2(0, 0)
        self.start_dir = random.randint(1, 4)
        self.start_x = random.randint(2, cell_number - 3)
        self.start_y = random.randint(2, cell_number - 3)
        self.no_move = 0

        self.find_snake()


class FRUIT:
    def __init__(self):
        self.randomize()
        self.super_amount = 3
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)
        self.fruit_color = (255, 33, 33)
        self.super_fruit_color = (170, 29, 5)
        self.super_fruit = random.randint(0, 9)

    def draw_fruit(self):
        # determine the square and draw the fruit
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        pygame.draw.rect(screen, self.fruit_color, fruit_rect)

    def draw_super_fruit(self):
        if self.super_fruit == 1:
            # determine the square and draw the fruit
            fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
            pygame.draw.rect(screen, self.super_fruit_color, fruit_rect)
        else:
            self.draw_fruit()

    def randomize(self):
        # randomize the position of the fruit
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)
        self.super_fruit = random.randint(0, 9)


class MAIN:
    def __init__(self):
        # make all the previous classes a subset of this class
        self.snake = SNAKE()
        self.fruit = FRUIT()
        self.score = SCORE()
        self.paused = False
        self.direction_temp = Vector2(0, 0)

    def update(self):
        # unless the snake is not moving, move it and check for collision
        if self.snake.direction != Vector2(0, 0):
            self.snake.move_snake()
            self.check_collision()
            self.check_fail()

    def draw_elements(self):
        # draw the various parts
        self.draw_grass()
        self.fruit.draw_super_fruit()
        self.snake.draw_snake()
        self.score.draw_score()
        if self.paused:
            self.draw_pause()

    def check_collision(self):
        # check for eating the fruit
        if self.fruit.pos == self.snake.body[0]:
            if self.fruit.super_fruit == 1:
                self.snake.add_block(self.fruit.super_amount)
                self.score.update_score(self.fruit.super_amount)
            else:
                self.snake.add_block(1)
                self.score.update_score(1)
            self.fruit.randomize()

        # if the fruit spawns in the body, re-roll it
        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()

    def check_fail(self):
        # check if hit the wall
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()

        # check for hitting yourself
        for i in self.snake.body[1:]:
            if i == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        # reset the snake and score
        self.snake.reset()
        self.score.reset()

    def draw_grass(self):
        grass_color = (167, 209, 61)

        # draw the checkerboard of squares
        for row in range(cell_number):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)
            else:
                for col in range(cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)

    def pause(self):
        # print("paused")
        self.paused = True
        self.direction_temp = self.snake.direction
        self.snake.direction = Vector2(0, 0)

    def unpause(self):
        # print("unpaused")
        self.paused = False
        self.snake.direction = self.direction_temp

    def draw_pause(self):
        pause_text = pause_font.render("Paused", True, (0, 0, 0))
        screen.blit(pause_text, (self.score.score_x, self.score.score_y + 80))


# initialize pygame and set up system variables
pygame.init()
score_font = pygame.font.SysFont('Times New Roman', 30)
pause_font = pygame.font.SysFont('Times New Roman', 20)
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()
pygame.display.set_caption("Snake")

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 120)

main_game = MAIN()

run = True
while run:
    for event in pygame.event.get():
        # manage exiting the game
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.WINDOWMINIMIZED:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False

        # manage movement key presses
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                if main_game.snake.can_move and main_game.snake.no_move != 1 and not main_game.paused:
                    main_game.snake.direction = Vector2(0, -1)
                    main_game.snake.can_move = False
                    main_game.snake.no_move = 3
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                if main_game.snake.can_move and main_game.snake.no_move != 3 and not main_game.paused:
                    main_game.snake.direction = Vector2(0, 1)
                    main_game.snake.can_move = False
                    main_game.snake.no_move = 1
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                if main_game.snake.can_move and main_game.snake.no_move != 4 and not main_game.paused:
                    main_game.snake.direction = Vector2(-1, 0)
                    main_game.snake.can_move = False
                    main_game.snake.no_move = 2
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                if main_game.snake.can_move and main_game.snake.no_move != 2 and not main_game.paused:
                    main_game.snake.direction = Vector2(1, 0)
                    main_game.snake.can_move = False
                    main_game.snake.no_move = 4
            if event.key == pygame.K_p:
                if main_game.paused:
                    main_game.unpause()
                elif not main_game.paused:
                    main_game.pause()

    # set the background, draw the elements, and update the screen
    screen.fill((175, 215, 70))
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60)

# stop the program
pygame.quit()
sys.exit()
