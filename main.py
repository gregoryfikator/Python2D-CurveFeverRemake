import pygame
import os
import math
import time
from random import seed, randint

WIDTH, HEIGHT = 1280, 720
BOARD_WIDTH, BOARD_HEIGHT = 800, 600

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)

BACKGROUND_DARK = (64, 56, 198)
BACKGROUND_LIGHT = (83, 122, 205)

GRAY = (128, 128, 128)
LIGHT_GRAY = (192, 192, 192) #only for grid in the background

KEY_COLOR = (255, 0, 180) # color used for removing background

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
VIEW = pygame.Surface((BOARD_WIDTH, BOARD_HEIGHT)) # play area
BOARD = pygame.Surface((BOARD_WIDTH, BOARD_HEIGHT)) # board area
BACKGROUND = pygame.Surface((WIDTH, HEIGHT)) # gradient background layer
UI = pygame.Surface((WIDTH, HEIGHT)) # ui layer

colour_rect = pygame.Surface((2, 2))
pygame.draw.line(colour_rect, BACKGROUND_DARK, (0, 0), (0, 1))
pygame.draw.line(colour_rect, BACKGROUND_LIGHT, (1, 0), (1, 1))
colour_rect = pygame.transform.smoothscale(colour_rect, (WIDTH, HEIGHT))
BACKGROUND.blit(colour_rect, (0, 0))

BACKGROUND.set_alpha(64)
BOARD.set_alpha(10)

pygame.display.set_caption("Curve Fever Remake - projekt PPP 2D")

SNAKE_COLORS = [RED, GREEN, BLUE, YELLOW, PURPLE]

FPS = 60
CENTER_X = BOARD_WIDTH // 2
CENTER_Y = BOARD_HEIGHT // 2

PLAYERS_COUNT = 0
MAX_PLAYERS = 2

PLAYER_AVATAR_WIDTH = 32
PLAYER_AVATAR_HEIGHT = 32

BOARD_MARGIN_X = 16
BOARD_MARGIN_Y = 16

TEXT_MARGIN = 8

PLAYER1_X = WIDTH - BOARD_WIDTH - BOARD_MARGIN_X
PLAYER1_Y = (((HEIGHT - BOARD_HEIGHT) // 2) - PLAYER_AVATAR_HEIGHT) // 2

PLAYER2_X = WIDTH - PLAYER_AVATAR_WIDTH - BOARD_MARGIN_X
PLAYER2_Y = HEIGHT - ((((HEIGHT - BOARD_HEIGHT) // 2) + PLAYER_AVATAR_HEIGHT) // 2)

GAME_OVER = False

ROUND_START_TIME = 0
ROUND_END_TIME = 0

POST_ROUND_STAGE = False
PRE_ROUND_STAGE = True

POST_ROUND_INTERVAL = 4000
PRE_ROUND_INTERVAL = 4000

PRE_ROUND_TIMER = 3
POST_ROUND_TIMER = 3

DRAWING_PAUSE_LENGTH = 250

DRAWING_PAUSE_SHORT_INTERVAL_LENGTH = 100
DRAWING_PAUSE_MEDIUM_INTERVAL_LENGTH = 250
DRAWING_PAUSE_LONG_INTERVAL_LENGTH = 500

DRAWING_PAUSE_TIMESPANS = [
  [DRAWING_PAUSE_LENGTH], # single break 
  [DRAWING_PAUSE_LENGTH, DRAWING_PAUSE_SHORT_INTERVAL_LENGTH, DRAWING_PAUSE_LENGTH], # two breaks with short interval
  [DRAWING_PAUSE_LENGTH, DRAWING_PAUSE_MEDIUM_INTERVAL_LENGTH, DRAWING_PAUSE_LENGTH], # two breaks with medium interval
  [DRAWING_PAUSE_LENGTH, DRAWING_PAUSE_LONG_INTERVAL_LENGTH, DRAWING_PAUSE_LENGTH], # two breaks with long interval
  [DRAWING_PAUSE_LENGTH, DRAWING_PAUSE_SHORT_INTERVAL_LENGTH, DRAWING_PAUSE_LENGTH, DRAWING_PAUSE_SHORT_INTERVAL_LENGTH, DRAWING_PAUSE_LENGTH],
  [DRAWING_PAUSE_LENGTH, DRAWING_PAUSE_SHORT_INTERVAL_LENGTH, DRAWING_PAUSE_LENGTH, DRAWING_PAUSE_MEDIUM_INTERVAL_LENGTH, DRAWING_PAUSE_LENGTH],
  [DRAWING_PAUSE_LENGTH, DRAWING_PAUSE_SHORT_INTERVAL_LENGTH, DRAWING_PAUSE_LENGTH, DRAWING_PAUSE_LONG_INTERVAL_LENGTH, DRAWING_PAUSE_LENGTH],
  [DRAWING_PAUSE_LENGTH, DRAWING_PAUSE_MEDIUM_INTERVAL_LENGTH, DRAWING_PAUSE_LENGTH, DRAWING_PAUSE_SHORT_INTERVAL_LENGTH, DRAWING_PAUSE_LENGTH],
  [DRAWING_PAUSE_LENGTH, DRAWING_PAUSE_MEDIUM_INTERVAL_LENGTH, DRAWING_PAUSE_LENGTH, DRAWING_PAUSE_MEDIUM_INTERVAL_LENGTH, DRAWING_PAUSE_LENGTH],
  [DRAWING_PAUSE_LENGTH, DRAWING_PAUSE_MEDIUM_INTERVAL_LENGTH, DRAWING_PAUSE_LENGTH, DRAWING_PAUSE_LONG_INTERVAL_LENGTH, DRAWING_PAUSE_LENGTH],
  [DRAWING_PAUSE_LENGTH, DRAWING_PAUSE_LONG_INTERVAL_LENGTH, DRAWING_PAUSE_LENGTH, DRAWING_PAUSE_SHORT_INTERVAL_LENGTH, DRAWING_PAUSE_LENGTH],
  [DRAWING_PAUSE_LENGTH, DRAWING_PAUSE_LONG_INTERVAL_LENGTH, DRAWING_PAUSE_LENGTH, DRAWING_PAUSE_MEDIUM_INTERVAL_LENGTH, DRAWING_PAUSE_LENGTH],
  [DRAWING_PAUSE_LENGTH, DRAWING_PAUSE_LONG_INTERVAL_LENGTH, DRAWING_PAUSE_LENGTH, DRAWING_PAUSE_LONG_INTERVAL_LENGTH, DRAWING_PAUSE_LENGTH],
]

pygame.font.init()
main_font = pygame.font.SysFont('Arial', 16)
main_font_mid = pygame.font.SysFont('Arial', 32)
main_font_big = pygame.font.SysFont('Arial', 128)

DIAMOND = pygame.transform.scale(pygame.image.load('diamond.jpg'), (32, 32))

BOOST_SPEED_UP_ME = pygame.transform.scale(pygame.image.load('boost_speed_up_me.png'), (64, 64))
BOOST_SPEED_UP_ENEMY = pygame.transform.scale(pygame.image.load('boost_speed_up_enemy.png'), (64, 64))

BOOST_SLOW_DOWN_ME = pygame.transform.scale(pygame.image.load('boost_slow_down_me.png'), (64, 64))
BOOST_SLOW_DOWN_ENEMY = pygame.transform.scale(pygame.image.load('boost_slow_down_enemy.png'), (64, 64))

KEY_A_ICON = pygame.transform.scale(pygame.image.load('key_a.png'), (64, 64))
KEY_D_ICON = pygame.transform.scale(pygame.image.load('key_d.png'), (64, 64))
KEY_LEFT_ARROW_ICON = pygame.transform.scale(pygame.image.load('key_left_arrow.png'), (64, 64))
KEY_RIGHT_ARROW_ICON = pygame.transform.scale(pygame.image.load('key_right_arrow.png'), (64, 64))

POWERUPS = [
  BOOST_SPEED_UP_ME,
  BOOST_SPEED_UP_ENEMY,
  BOOST_SLOW_DOWN_ME,
  BOOST_SLOW_DOWN_ENEMY
]

POWERUP_SIZE = 64
POWERUP_DURATION = 5000

seed(time.time())

class Powerup(object):
    type_id: int

    collection_time: int
    remaining_duration: int

    pos: pygame.Vector2()

    is_collected: bool
    is_finished: bool

    affected_players: list()

    def __init__(self):
        self.type_id = randint(0, len(POWERUPS) - 1)
        self.pos = pygame.Vector2(randint(POWERUP_SIZE / 2, BOARD_WIDTH - (POWERUP_SIZE / 2)), randint(POWERUP_SIZE / 2, BOARD_HEIGHT - (POWERUP_SIZE / 2)))
        self.is_collected = False
        self.is_finished = False
        self.affected_players = []

    def get_position(self):
        return self.pos

    def get_type_id(self):
        return self.type_id

    def collect(self, collector, enemies):
        if self.is_collected == True:
            return
        
        self.is_collected = True
        self.remaining_duration = 5000
        self.collection_time = pygame.time.get_ticks()
        if self.type_id == 0:
            collector.change_speed(0.25)
            self.affected_players.append(collector)
        elif self.type_id == 1:
            for enemy in enemies:
                enemy.change_speed(0.25)
                self.affected_players.append(enemy)
        elif self.type_id == 2:
            collector.change_speed(-0.25)
            self.affected_players.append(collector)
        elif self.type_id == 3:
            for enemy in enemies:
                enemy.change_speed(-0.25)
                self.affected_players.append(enemy)

    def end_affection(self):
        for player in self.affected_players:
            if self.type_id == 0 or self.type_id == 1:
                player.change_speed(-0.25)
            elif self.type_id == 2 or self.type_id == 3:
                player.change_speed(0.25)

    def render(self):
        if self.is_collected == False:
            VIEW.blit(POWERUPS[self.type_id], (self.pos.x - 32, self.pos.y - 32), (0, 0, BOARD_WIDTH, BOARD_HEIGHT))

    def update(self):
        if self.is_collected == True:
            self.remaining_duration = POWERUP_DURATION - (pygame.time.get_ticks() - self.collection_time)

            if self.remaining_duration <= 0:
                self.is_finished = True
                self.end_affection()

class Snake(object):
    line_segments: list

    pos: pygame.Vector2()

    id: int
    name: str
    size: int
    points: int
    color: tuple

    speed: float
    speed_from_boosts: float
    angle: int
    prev_angle: int

    is_drawing_paused: bool
    was_drawing_paused: bool

    drawing_timer: int
    drawing_break_delay: int
    drawing_break_type: int
    drawing_timestamp_index: int

    has_active_timer: bool

    is_alive: bool

    collected_powerups: list()

    def __init__(self, name):
        global PLAYERS_COUNT

        self.line_segments = list()
        self.size = 8
        self.name = name
        self.speed = 0.1
        self.speed_from_boosts = 1.0
        self.id = PLAYERS_COUNT
        self.points = 0

        self.is_drawing_paused = False
        self.was_drawing_paused = False
        self.has_active_timer = False

        self.drawing_timer = None
        self.drawing_break_delay = None
        self.drawing_break_type = None
        self.drawing_timestamp_index = None

    def set_on_board(self, pos, angle, color):
        self.line_segments.clear()
        self.line_segments.append((pygame.Vector2(pos), pygame.Vector2(pos)))
        self.angle = angle
        self.prev_angle = angle
        self.is_alive = True
        self.color = color
        self.pos = pos
    
    def set_position(self, pos_x, pos_y):
        self.pos[0] = pos_x
        self.pos[1] = pos_y

    def get_position(self):
        return self.pos

    def get_points(self):
        return self.points

    def add_points(self, points_to_add):
        global GAME_OVER

        self.points += points_to_add

        if self.points == 3:
            GAME_OVER = True

    def clear_points(self):
        self.points = 0

    def get_id(self):
        return self.id

    def get_line_segments(self):
        return self.line_segments

    def get_color(self):
        return self.color

    def get_name(self):
        return self.name

    def change_speed(self, value):
        self.speed_from_boosts += value

        if self.speed_from_boosts < 0.25:
            self.speed_from_boosts = 0.25

    def setup_drawing_break(self):
        if (self.has_active_timer == False):
            self.drawing_break_type = DRAWING_PAUSE_TIMESPANS[randint(0, len(DRAWING_PAUSE_TIMESPANS) - 1)].copy()
            duration = sum(self.drawing_break_type)
            self.drawing_break_type.insert(0, randint(500, max(5000 - duration, 2500)))
            self.drawing_timestamp_index = 0
            self.drawing_timer = pygame.time.get_ticks()
            pygame.time.set_timer(pygame.USEREVENT + 1, self.drawing_break_type[0], 1)
            self.has_active_timer = True

    def handle_drawing_break_event(self):
        if (self.has_active_timer == False):
            return

        self.is_drawing_paused = (not self.is_drawing_paused and self.drawing_timestamp_index > 0)
        
        if self.drawing_timestamp_index + 1 == len(self.drawing_break_type):
            pygame.time.set_timer(pygame.USEREVENT + 1, self.drawing_break_type[self.drawing_timestamp_index], True)
            self.drawing_timestamp_index = None
            self.drawing_timer = None
            del(self.drawing_break_type)
            self.drawing_break_type = None
            self.is_drawing_paused = False
            self.has_active_timer = False
            return

        pygame.time.set_timer(pygame.USEREVENT + 1, self.drawing_break_type[self.drawing_timestamp_index + 1], True)

        self.drawing_timestamp_index += 1

    def update_drawing_break(self):
        if (self.has_active_timer == True):
            return

        if self.drawing_timestamp_index == len(self.drawing_break_type):
            self.drawing_timestamp_index = None
            self.drawing_timer = None
            del(self.drawing_break_type)
            self.drawing_break_type = None
            self.is_drawing_paused = False
            return

        current_time = pygame.time.get_ticks()

        if self.drawing_break_type[self.drawing_timestamp_index] < current_time - self.drawing_timer:
            self.is_drawing_paused = (not self.is_drawing_paused and self.drawing_timestamp_index > 0)

            self.drawing_timestamp_index += 1
            self.drawing_timer = current_time

    def is_snake_alive(self):
        return self.is_alive

    def check_board_collision(self):
        half_size = self.size // 2
        return self.pos[0] - half_size < 0 or self.pos[0] + half_size > BOARD_WIDTH or self.pos[1] - half_size < 0 or self.pos[1] + half_size > BOARD_HEIGHT

    def check_self_collision(self):
        if self.is_drawing_paused == True:
            return False

        Q = self.pos
        r = self.size // 2
        for (start, end) in self.line_segments[:-10]:
            P1 = start
            V = end - P1
            if V.length() == 0:
                continue
            
            a = V.dot(V)
            b = 2 * V.dot(P1 - Q)
            c = P1.dot(P1) + Q.dot(Q) - 2 * P1.dot(Q) - r**2

            disc = b**2 - 4 * a * c
            if disc < 0:
                continue

            sqrt_disc = math.sqrt(disc)
            t1 = (-b + sqrt_disc) / (2 * a)
            t2 = (-b - sqrt_disc) / (2 * a)

            if not (0 < t1 < 1 or 0 < t2 < 1):
                continue

            return True

        return False

    def check_enemy_collision(self, snakes):
        if self.is_drawing_paused == True:
            return False

        snakes_copy = snakes.copy()
        snakes_copy = [snake for snake in snakes_copy if snake.get_id() != self.id]

        for snake in snakes_copy:
            Q = self.pos
            r = self.size // 2
            for (start, end) in snake.get_line_segments():
                P1 = start
                V = end - P1
                if V.length() == 0:
                    return False
                
                a = V.dot(V)
                b = 2 * V.dot(P1 - Q)
                c = P1.dot(P1) + Q.dot(Q) - 2 * P1.dot(Q) - r**2

                disc = b**2 - 4 * a * c
                if disc < 0:
                    continue

                sqrt_disc = math.sqrt(disc)
                t1 = (-b + sqrt_disc) / (2 * a)
                t2 = (-b - sqrt_disc) / (2 * a)

                if not (0 <= t1 <= 1 or 0 <= t2 <= 1):
                    continue

                return True

        return False

    def check_powerup_collision(self, powerups, enemies):
        for powerup in powerups:
            center = powerup.get_position()
            x2 = (self.pos.x - center.x) * (self.pos.x - center.x)
            y2 = (self.pos.y - center.y) * (self.pos.y - center.y)
            r2 = (POWERUP_SIZE / 2) * (POWERUP_SIZE / 2)
            if (x2 + y2 <= r2) == True:
                powerup.collect(self, enemies)

    def kill(self):
        self.is_alive = False

    def update(self, powerups, enemies):
        if self.is_alive == False:
            return

        self.check_powerup_collision(powerups, enemies)

        #self.update_drawing_break()

        if self.is_drawing_paused == True:
            self.prev_angle = self.angle
            self.was_drawing_paused = True
            return
        
        if self.was_drawing_paused == True:
            self.was_drawing_paused = False
            self.prev_angle = self.angle
            self.line_segments.append((pygame.Vector2(self.pos), pygame.Vector2(self.pos)))

        (last_line_start, last_line_end) = self.line_segments[-1]

        if self.angle != self.prev_angle or (last_line_end - last_line_start).length() > self.size // 4:
          
            self.prev_angle = self.angle

            self.line_segments.append((
                last_line_end,
                pygame.Vector2(self.pos)
            ))
        else:
            last_line_end[0] = self.pos[0]
            last_line_end[1] = self.pos[1]
            self.line_segments[-1] = (last_line_start, last_line_end)

    def render(self):
        for (start, end) in self.line_segments:
            pygame.draw.line(VIEW, self.color, (start[0], start[1]), (end[0], end[1]), self.size) #draw lines behind snake

        if self.is_alive == True:
            pygame.draw.circle(VIEW, self.color, (self.pos[0], self.pos[1]), self.size) #draw player circle

class Player(Snake):
    key_left: int
    key_right: int 

    def __init__(self, name, key_mapping):
        global PLAYERS_COUNT
        PLAYERS_COUNT += 1
        super().__init__(name)
        self.key_left = key_mapping[0]
        self.key_right = key_mapping[1]

    def move(self, dt):
        global PRE_ROUND_STAGE

        if self.is_alive == False:
            return

        if PRE_ROUND_STAGE == True:
            return

        keys = pygame.key.get_pressed()

        if keys[self.key_left]:
            self.angle += (math.pi / 75)

        if keys[self.key_right]:
            self.angle -= (math.pi / 75)

        pos = self.get_position()

        pos[0] += math.sin(self.angle) * self.speed * dt * self.speed_from_boosts
        pos[1] += math.cos(self.angle) * self.speed * dt * self.speed_from_boosts

        self.set_position(pos[0], pos[1])

def render_window(snakes: Snake, powerups: Powerup):
    global PRE_ROUND_STAGE
    global PRE_ROUND_TIMER
    global POST_ROUND_STAGE
    global GAME_OVER
    global ROUND_START_TIME
    global ROUND_END_TIME

    WIN.fill(BLACK)
    VIEW.fill(BLACK)
    BOARD.fill(WHITE)

    BACKGROUND.blit(colour_rect, (0, 0))

    WIN.blit(BACKGROUND, (0, 0))
    WIN.blit(BOARD, (WIDTH - BOARD_WIDTH - BOARD_MARGIN_X, (HEIGHT - BOARD_HEIGHT) // 2), (0, 0, BOARD_WIDTH, BOARD_HEIGHT))

    pygame.draw.rect(VIEW, WHITE, (0, 0, BOARD_WIDTH, BOARD_HEIGHT), 5)

    for snake in snakes:
        snake.render()

    for powerup in powerups:
        powerup.render()

    if GAME_OVER == True:
        i = 0
        for snake in snakes:
            if snake.points == 3:
                break
            i += 1

        post_round_summaries_counter = main_font_mid.render('{0} won the game!'.format(snakes[i].get_name()), True, WHITE)
        counter_width = post_round_summaries_counter.get_width()
        counter_height = post_round_summaries_counter.get_height()
        VIEW.blit(post_round_summaries_counter, ((BOARD_WIDTH - counter_width) // 2, (BOARD_HEIGHT - counter_height) // 2))
    elif POST_ROUND_STAGE == True:
        i = 0
        for snake in snakes:
            if snake.is_alive == True:
                break
            i += 1

        post_round_summaries = ''
        plural_suffix = ''

        time = math.ceil((ROUND_END_TIME - ROUND_START_TIME) // 1000)
        if time != 1:
            plural_suffix = 's'

        if i == len(snakes):
            post_round_summaries = main_font_mid.render('Round drawn in {0} second{1}!'.format(str(time), plural_suffix), True, WHITE)
        else:
            post_round_summaries = main_font_mid.render('{0} won the round in {1} second{2}!'.format(snakes[i].get_name(), str(time), plural_suffix), True, WHITE)

        counter_width = post_round_summaries.get_width()
        counter_height = post_round_summaries.get_height()
        VIEW.blit(post_round_summaries, ((BOARD_WIDTH - counter_width) // 2, (BOARD_HEIGHT - counter_height) // 2))
    elif PRE_ROUND_STAGE == True:
        round_begin_counter = main_font_big.render(str(PRE_ROUND_TIMER), True, WHITE)
        counter_width = round_begin_counter.get_width()
        counter_height = round_begin_counter.get_height()
        VIEW.blit(round_begin_counter, ((BOARD_WIDTH - counter_width) // 2, (BOARD_HEIGHT - counter_height) // 2))

    WIN.blit(VIEW, (WIDTH - BOARD_WIDTH - BOARD_MARGIN_X, (HEIGHT - BOARD_HEIGHT) // 2), (0, 0, BOARD_WIDTH, BOARD_HEIGHT))

def render_help_section():
    reference_pos_y = (HEIGHT - BOARD_HEIGHT) // 2
    single_boost_with_padding = 64 + 16

    WIN.blit(BOOST_SPEED_UP_ME, (32, reference_pos_y))
    WIN.blit(BOOST_SPEED_UP_ENEMY, (32, reference_pos_y + single_boost_with_padding))
    WIN.blit(BOOST_SLOW_DOWN_ME, (32, reference_pos_y + 2 * single_boost_with_padding))
    WIN.blit(BOOST_SLOW_DOWN_ENEMY, (32, reference_pos_y + 3 * single_boost_with_padding))

    boost1_description = main_font.render('Speed up me for 5 seconds', True, WHITE)
    WIN.blit(boost1_description, (32 + 64 + TEXT_MARGIN * 2, reference_pos_y + 32 - boost1_description.get_height() // 2))

    boost2_description = main_font.render('Speed up enemy for 5 seconds', True, WHITE)
    WIN.blit(boost2_description, (32 + 64 + TEXT_MARGIN * 2, reference_pos_y + single_boost_with_padding + 32 - boost2_description.get_height() // 2))

    boost3_description = main_font.render('Slow down me for 5 seconds', True, WHITE)
    WIN.blit(boost3_description, (32 + 64 + TEXT_MARGIN * 2, reference_pos_y + 2 * single_boost_with_padding + 32 - boost3_description.get_height() // 2))

    boost4_description = main_font.render('Slow down enemy for 5 seconds', True, WHITE)
    WIN.blit(boost4_description, (32 + 64 + TEXT_MARGIN * 2, reference_pos_y + 3 * single_boost_with_padding + 32 - boost4_description.get_height() // 2))

    WIN.blit(KEY_A_ICON, (32, reference_pos_y + 5 * single_boost_with_padding))
    WIN.blit(KEY_D_ICON, (32 + 64 + 32, reference_pos_y + 5 * single_boost_with_padding))

    player1_controls_description = main_font.render('Player 1 controls', True, WHITE)
    WIN.blit(player1_controls_description, (32 + 128 + 32 + TEXT_MARGIN * 2, reference_pos_y + 5 * single_boost_with_padding + 32 - player1_controls_description.get_height() // 2))

    WIN.blit(KEY_LEFT_ARROW_ICON, (32, reference_pos_y + 6 * single_boost_with_padding))
    WIN.blit(KEY_RIGHT_ARROW_ICON, (128, reference_pos_y + 6 * single_boost_with_padding))

    player2_controls_description = main_font.render('Player 2 controls', True, WHITE)
    WIN.blit(player2_controls_description, (32 + 128 + 32 + TEXT_MARGIN * 2, reference_pos_y + 6 * single_boost_with_padding + 32 - player2_controls_description.get_height() // 2))

def render_ui(player1, player2):
    UI.fill(KEY_COLOR)
    UI.set_colorkey(KEY_COLOR)

    #player 1
    pygame.draw.rect(WIN, player1.get_color(), (PLAYER1_X, PLAYER1_Y, PLAYER_AVATAR_WIDTH, PLAYER_AVATAR_HEIGHT))
    pygame.draw.rect(WIN, WHITE, (PLAYER1_X, PLAYER1_Y, PLAYER_AVATAR_WIDTH, PLAYER_AVATAR_HEIGHT), 2)

    player1_name = main_font.render(player1.get_name(), True, WHITE)
    WIN.blit(player1_name, (PLAYER1_X + PLAYER_AVATAR_WIDTH + TEXT_MARGIN, PLAYER1_Y + TEXT_MARGIN))

    player1_points = player1.get_points()
    i = 0

    while (i < player1_points):
        WIN.blit(DIAMOND, (PLAYER1_X + PLAYER_AVATAR_WIDTH + TEXT_MARGIN + player1_name.get_width() + 4 + 32 * i, PLAYER1_Y))
        i += 1

    #player 2
    pygame.draw.rect(WIN, player2.get_color(), (PLAYER2_X, PLAYER2_Y, PLAYER_AVATAR_WIDTH, PLAYER_AVATAR_HEIGHT))
    pygame.draw.rect(WIN, WHITE, (PLAYER2_X, PLAYER2_Y, PLAYER_AVATAR_WIDTH, PLAYER_AVATAR_HEIGHT), 2)

    player2_name = main_font.render(player2.get_name(), True, WHITE)
    WIN.blit(player2_name, (PLAYER2_X - player2_name.get_width() - TEXT_MARGIN, PLAYER2_Y + TEXT_MARGIN))

    player2_points = player2.get_points()
    i = 0
    
    while (i < player2_points):
        WIN.blit(DIAMOND, (PLAYER2_X - player2_name.get_width() - TEXT_MARGIN - 36 * (i + 1), PLAYER2_Y))
        i += 1

    render_help_section()

def add_points(snakes):
    global POST_ROUND_STAGE
    global ROUND_END_TIME

    count = 0
    for snake in snakes:  
        if snake.is_alive == True:
            snake.add_points(1)
            count += 1

    if count <= 1:
        POST_ROUND_STAGE = True
        ROUND_END_TIME = pygame.time.get_ticks()

def detect_deadly_collisions(snakes):
    collision = False
    for snake in snakes:
        if snake.is_alive == True:
            if snake.check_board_collision() == True or snake.check_self_collision() == True or snake.check_enemy_collision(snakes) == True:
                snake.kill()
                collision = True
    if collision == True:       
        add_points(snakes)  

def main():
    global PRE_ROUND_STAGE
    global PRE_ROUND_TIMER

    global POST_ROUND_STAGE
    global POST_ROUND_TIMER

    global ROUND_START_TIME
    global ROUND_END_TIME

    global GAME_OVER

    pygame.init()

    player1 = Player('Player 1', (pygame.K_a, pygame.K_d))
    player2 = Player('Player 2', (pygame.K_LEFT, pygame.K_RIGHT))

    player1.set_on_board(pygame.Vector2(randint(80, (BOARD_WIDTH // 2) - 20), randint(80, BOARD_HEIGHT - 80)), randint(0, 360), RED)
    player2.set_on_board(pygame.Vector2(randint((BOARD_WIDTH // 2) + 20, BOARD_WIDTH - 80), randint(80, BOARD_HEIGHT - 80)), randint(0, 360), BLUE)

    snakes = list()
    snakes.append(player1)
    snakes.append(player2)

    powerups = list()
    powerups.append(Powerup())

    clock = pygame.time.Clock()

    isRunning = True

    start_time = pygame.time.get_ticks()
    # player1.setup_drawing_break()
    # player2.setup_drawing_break()
    dt = 0

    ROUND_START_TIME = pygame.time.get_ticks()

    while (isRunning):
        if pygame.time.get_ticks() - start_time > 5000 and POST_ROUND_STAGE == False and GAME_OVER == False:
            powerups.append(Powerup())
            start_time = pygame.time.get_ticks()
        #     player1.setup_drawing_break()
        #     player2.setup_drawing_break()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isRunning = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    isRunning = False
                    break
                elif event.key == pygame.K_SPACE:
                    GAME_OVER = False

                    player1.set_on_board(pygame.Vector2(randint(80, (BOARD_WIDTH // 2) - 20), randint(80, BOARD_HEIGHT - 80)), randint(0, 360), RED)
                    player2.set_on_board(pygame.Vector2(randint((BOARD_WIDTH // 2) + 20, BOARD_WIDTH - 80), randint(80, BOARD_HEIGHT - 80)), randint(0, 360), BLUE)

                    player1.clear_points()
                    player2.clear_points()

                    dt = 0

                    ROUND_START_TIME = pygame.time.get_ticks()
                    ROUND_END_TIME = 0
                    PRE_ROUND_STAGE = True

            if event.type == pygame.USEREVENT + 1:
                player1.handle_drawing_break_event()
                player2.handle_drawing_break_event()

        if PRE_ROUND_STAGE == False and POST_ROUND_STAGE == False and GAME_OVER == False:
            player1.move(dt)
            player2.move(dt)

            for powerup in powerups:
                powerup.update()

            powerups = [x for x in powerups if x.is_finished == False]

            player1.update(powerups, [player2])
            player2.update(powerups, [player1])

            detect_deadly_collisions(snakes)
        elif PRE_ROUND_STAGE == True:
            diff = pygame.time.get_ticks() - ROUND_START_TIME
            PRE_ROUND_TIMER = math.ceil((PRE_ROUND_INTERVAL - diff) // 1000)

            if PRE_ROUND_TIMER <= 0:
                PRE_ROUND_STAGE = False
                ROUND_START_TIME = pygame.time.get_ticks()
                # player1.setup_drawing_break()
                # player2.setup_drawing_break()
        elif POST_ROUND_STAGE == True:
            diff = pygame.time.get_ticks() - ROUND_END_TIME
            POST_ROUND_TIMER = math.ceil((POST_ROUND_INTERVAL - diff) // 1000)

            if POST_ROUND_TIMER <= 0:
                POST_ROUND_STAGE = False

                player1.set_on_board(pygame.Vector2(randint(80, (BOARD_WIDTH // 2) - 20), randint(80, BOARD_HEIGHT - 80)), randint(0, 360), RED)
                player2.set_on_board(pygame.Vector2(randint((BOARD_WIDTH // 2) + 20, BOARD_WIDTH - 80), randint(80, BOARD_HEIGHT - 80)), randint(0, 360), BLUE)

                dt = 0

                powerups.clear()

                start_time = pygame.time.get_ticks()
                ROUND_START_TIME = pygame.time.get_ticks()
                ROUND_END_TIME = 0
                if GAME_OVER == False:
                    PRE_ROUND_STAGE = True

        render_window(snakes, powerups)

        render_ui(player1, player2)

        pygame.display.flip()

        dt = clock.tick(FPS)

    del(player1)
    del(player2)
    del(snakes)

    pygame.quit()

if __name__ == "__main__":
    main()
