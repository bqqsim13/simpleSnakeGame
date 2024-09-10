import pygame, sys, random, os
from pygame.math import Vector2

class SNAKE:
    def __init__(self):
        
        # Get the directory where the script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))

        self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)]
        self.direction = Vector2(1,0)
        self.new_block = False

        # Sprites
        self.head_up = pygame.image.load(os.path.join(script_dir, 'spriteAssets/head_up.png')).convert_alpha()
        self.head_down = pygame.image.load(os.path.join(script_dir, 'spriteAssets/head_down.png')).convert_alpha()
        self.head_right = pygame.image.load(os.path.join(script_dir, 'spriteAssets/head_right.png')).convert_alpha()
        self.head_left = pygame.image.load(os.path.join(script_dir, 'spriteAssets/head_left.png')).convert_alpha()

        self.tail_up = pygame.image.load(os.path.join(script_dir, 'spriteAssets/tail_down.png')).convert_alpha()
        self.tail_down = pygame.image.load(os.path.join(script_dir, 'spriteAssets/tail_up.png')).convert_alpha()
        self.tail_right = pygame.image.load(os.path.join(script_dir, 'spriteAssets/tail_right.png')).convert_alpha()
        self.tail_left = pygame.image.load(os.path.join(script_dir, 'spriteAssets/tail_left.png')).convert_alpha()

        self.body_vertical = pygame.image.load(os.path.join(script_dir, 'spriteAssets/body_vertical.png')).convert_alpha()
        self.body_horizontal = pygame.image.load(os.path.join(script_dir, 'spriteAssets/body_horizontal.png')).convert_alpha()

        self.body_topright = pygame.image.load(os.path.join(script_dir, 'spriteAssets/body_topright.png')).convert_alpha()
        self.body_topleft = pygame.image.load(os.path.join(script_dir, 'spriteAssets/body_topleft.png')).convert_alpha()
        self.body_bottomright = pygame.image.load(os.path.join(script_dir, 'spriteAssets/body_bottomright.png')).convert_alpha()
        self.body_bottomleft = pygame.image.load(os.path.join(script_dir, 'spriteAssets/body_bottomleft.png')).convert_alpha()

        # Sounds
        self.crunch_sound = pygame.mixer.Sound(os.path.join(script_dir, 'soundFontAssets/smw_coin.wav'))
        self.die_sound = pygame.mixer.Sound(os.path.join(script_dir, 'soundFontAssets/smw_koopa_kid_falls_into_lava.wav'))

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index,block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)

            block_rect = pygame.Rect(x_pos,y_pos,cell_size,cell_size)
        
            if index == 0:
                 screen.blit(self.head,block_rect)
            elif index == len(self.body) - 1:
                 screen.blit(self.tail, block_rect)
            else:
                 previous_block = self.body[index + 1] - block
                 next_block = self.body[index - 1] - block
                 if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical,block_rect)
                 elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal,block_rect)
                 else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_topleft,block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bottomleft,block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_topright,block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_bottomright,block_rect)


    def update_head_graphics(self):
         head_relation = self.body[1] - self.body[0]
         if head_relation == Vector2(1,0): self.head = self.head_left
         elif head_relation == Vector2(-1,0): self.head = self.head_right
         elif head_relation == Vector2(0,1): self.head = self.head_up
         elif head_relation == Vector2(0,-1): self.head = self.head_down
    
    
    def update_tail_graphics(self):
         tail_relation = self.body[-2] - self.body[-1]
         if tail_relation == Vector2(1,0): self.tail = self.tail_left
         elif tail_relation == Vector2(-1,0): self.tail = self.tail_right
         elif tail_relation == Vector2(0,1): self.tail = self.tail_down
         elif tail_relation == Vector2(0,-1): self.tail = self.tail_up
        

    def move_snake(self):
        if self.new_block == True:
             body_copy = self.body[:]
             body_copy.insert(0,body_copy[0] + self.direction)
             self.body = body_copy[:]
             self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0,body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

    def play_munch_sound(self):
        self.crunch_sound.play()
    
    def play_die_sound(self):
        self.die_sound.play()




class FRUIT:
    def __init__(self):
        self.randomification()

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(fraudBoy,fruit_rect)
        #pygame.draw.rect(screen,(0,255,255), fruit_rect)

    def randomification(self):
        self.x = random.randint(0, (cell_num - 1))
        self.y = random.randint(0, (cell_num - 1))
        self.pos = Vector2(self.x, self.y)

class MAIN:
    def __init__(self) -> None:
        self.snake = SNAKE()
        self.fruit = FRUIT()
        self.score = 0

    def update(self):
        self.snake.move_snake()
        self.check_eatery()
        self.check_failing()

    def draw_elements(self):
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()
        

    def check_eatery(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomification()
            self.snake.add_block()
            self.snake.play_munch_sound()
            self.score += 1
        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomification()

    def check_failing(self):
        if not 0 <=  self.snake.body[0].x < cell_num or not 0 <=  self.snake.body[0].y < cell_num:
            self.game_over()

        for block in self.snake.body[1:]:
             if block == self.snake.body[0]:
                  self.game_over()
                  

    
    def game_over(self):
        self.snake.play_die_sound()
        pygame.time.delay(1200)  # delay for 2000 milliseconds (2 seconds)
        pygame.quit()
        sys.exit()



    def draw_grass(self):
        grass_colour = (121, 217, 104)
        for row in range(cell_num):
            if row % 2 == 0:
                for col in range(cell_num):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * cell_size,row * cell_size,cell_size,cell_size)
                        pygame.draw.rect(screen, grass_colour, grass_rect)
            else:
                for col in range(cell_num):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * cell_size,row * cell_size,cell_size,cell_size)
                        pygame.draw.rect(screen, grass_colour, grass_rect)

    def draw_score(self):
        score_text = "SCORE: " + str(self.score) 
        score_surface = gameFont.render(score_text,True,(56,74,12))
        score_x = int((cell_size * cell_num) - 500)
        score_y = int((cell_size * cell_num) - 760)
        score_rect = score_surface.get_rect(center = (score_x,score_y))
        fraudy_rect = fraudBoy.get_rect(midright = (score_rect.left,score_rect.centery))
        bg_rect = pygame.Rect(fraudy_rect.left,fraudy_rect.top,fraudy_rect.width + score_rect.width + 6,fraudy_rect.height + 2)

        pygame.draw.rect(screen,(132, 217, 104),bg_rect)
        screen.blit(score_surface,score_rect)
        screen.blit(fraudBoy,fraudy_rect)
        pygame.draw.rect(screen,(56,74,12),bg_rect, 3)


pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()
cell_size = 40
cell_num = 20
#40 and 20
screen = pygame.display.set_mode((cell_num * cell_size,cell_num * cell_size))
clock = pygame.time.Clock()
fraudBoy = pygame.image.load('/Users/bqqsim/projies/snakeGame!/spriteAssets/eatme.jpg').convert_alpha()
fraudBoy = pygame.transform.scale(fraudBoy, (cell_size * int(1.5), cell_size * int(1.5)))
gameFont = pygame.font.Font('/Users/bqqsim/projies/snakeGame!/soundFontAssets/osaka-re.ttf', 40)


test_surface = pygame.Surface((100,200))
test_surface.fill((0,0,255))

test_rect = test_surface.get_rect(center = (200,250))

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

main_game = MAIN()

#game loop
while True:
    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            sys.exit()
        if event.type == SCREEN_UPDATE:
             main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                    if main_game.snake.direction.y != 1:
                        main_game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_LEFT:
                    if main_game.snake.direction.x != 1:
                        main_game.snake.direction = Vector2(-1, 0)
            if event.key == pygame.K_DOWN:
                    if main_game.snake.direction.y != -1:
                        main_game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_RIGHT:
                    if main_game.snake.direction.x != -1:
                        main_game.snake.direction = Vector2(1, 0)


    #screenRefresh/colour 
    screen.fill((132, 217, 104))
    main_game.draw_elements()
    pygame.display.update()
    #max while loop per second
    clock.tick(60)