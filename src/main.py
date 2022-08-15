"""
BUCKEYE TETROMINOES
Coded by:  Adam Buynak in collaboration w/ The Ohio State University's OHI/O
Game Logic Sourced from Arcade Sample Code library.
Distributed under the MIT LICENSE.
"""


#############
## Imports ##
#############

import arcade
import PIL
import random
import time
import timeit

# Import Support Files
from game_variables import *
from game_scores import *


##########################
## Setup Global Sprites ##
##########################

def create_textures():
    """ Create a list of images for sprites based on the global colors.
        !!! SHOULD be able to add custom images in here instead of the general colors."""
    texture_list = []
    for color in colors:
        image = PIL.Image.new('RGB', (WIDTH, HEIGHT), color)
        texture_list.append(arcade.Texture(str(color), image=image))
    return texture_list


texture_list = create_textures()



###################################
## Support Functions to GameView ##
###################################

def rotate_clockwise(shape):
    """ Rotates a matrix clockwise """
    return [[shape[len(shape)-y-1][x] for y in range(len(shape))] for x in range(len(shape[0]))]

def check_collision(board, shape, offset):
    """
    See if the matrix stored in the shape will intersect anything
    on the board based on the offset. Offset is an (x, y) coordinate.
    """
    off_x, off_y = offset
    for cy, row in enumerate(shape):
        for cx, cell in enumerate(row):
            if cell and board[cy + off_y][cx + off_x]:
                return True
    return False

def remove_row(board, row):
    """ Remove a row from the board, add a blank row on top. """
    del board[row]
    #print("--[tetris] Deleted Row #",row)
    return [[0 for i in range(COLUMN_COUNT)]] + board

def join_matrixes(matrix_1, matrix_2, matrix_2_offset):
    """ Copy matrix 2 onto matrix 1 based on the passed in x, y offset coordinate """
    offset_x, offset_y = matrix_2_offset
    for cy, row in enumerate(matrix_2):
        for cx, val in enumerate(row):
            matrix_1[cy + offset_y - 1][cx + offset_x] += val
    return matrix_1

def new_board():
    """ Create a grid of 0's. Add 1's to the bottom for easier collision detection. """
    # Create the main board of 0's
    board = [[0 for x in range(COLUMN_COUNT)] for y in range(ROW_COUNT)]
    # Add a bottom border of 1's
    board += [[8 for x in range(COLUMN_COUNT)]]
    return board



#################
## Class: Game ##
#################

class GameView(arcade.View):
    global ALL_SCORES
    global GAME_SPEED_FLOOR

    def __init__(self):
        super(GameView, self).__init__()

        ## Static Content
        # Advertisement Note
        self.st_adtxt = arcade.Text(text="REGISTER TODAY @ HACK.OSU.EDU/2022",
                                    start_x=WINDOW_WIDTH / 2,
                                    start_y=73,
                                    color=arcade.color.WHITE,
                                    font_size=float(11),
                                    width=SCREEN_WIDTH,
                                    bold=True,
                                    align="center",
                                    multiline=False,
                                    anchor_x="center",
                                    anchor_y="center")

        # Current Player Info
        self.st_player_title = arcade.Text("- CURRENT CHALLENGER -",
                                           SCREEN_WIDTH / 2 + WINDOW_MARGIN,
                                           SCREEN_HEIGHT * 0.9,
                                           width=SCREEN_WIDTH-2,
                                           color=arcade.color.BLACK,
                                           font_size=float(SCREEN_HEIGHT * 0.015),
                                           align="center",
                                           anchor_x="center",
                                           anchor_y="center")
        self.st_player_name = arcade.Text("",
                                          SCREEN_WIDTH / 2 + WINDOW_MARGIN,
                                          SCREEN_HEIGHT * 0.87,
                                          width=SCREEN_WIDTH - 2,
                                          color=arcade.color.BLACK,
                                          font_size=float(SCREEN_HEIGHT * 0.02),
                                          bold=True,
                                          align="center",
                                          anchor_x="center",
                                          anchor_y="center")

        # Setup Diagnostics Panel
        h_1 = rx_yposn + (rx_height / 2) - 175  # Frame Counter
        h_2 = rx_yposn + (rx_height / 2) - 275  # Levels
        h_3 = rx_yposn + (rx_height / 2) - 200  # FPS
        h_4 = rx_yposn + (rx_height / 2) - 225  # Time to Update
        h_5a = rx_yposn + (rx_height / 2) - 75  # Floor Speed
        h_5b = rx_yposn + (rx_height / 2) - 100  # Current Speed
        self.st_d_header = arcade.Text("Game Diagnostics",
                                       rx_xposn - (rx_width / 2) + 20,
                                       rx_yposn + (rx_height / 2) - 30,
                                       arcade.color.BLACK,
                                       float(20),
                                       bold=True,
                                       align="left")
        self.st_d_setfloor = arcade.Text("Set Floor: ",
                                         rx_xposn - (rx_width / 2) + 20,
                                         h_5a,
                                         arcade.color.BLACK,
                                         float(15),
                                         bold=True,
                                         align="left")
        self.st_d_adjustupdown = arcade.Text("Adjust w PAGE_UP/_DOWN",
                                             rx_xposn - (rx_width / 2) + 350,
                                             h_5a,
                                             arcade.color.GRAY,
                                             float(7),
                                             bold=True,
                                             align="left")
        self.st_d_t5a = arcade.Text("temp_filler_t5a",
                                         rx_xposn - (rx_width / 2) + 200,
                                         h_5a,
                                         arcade.color.BRIGHT_NAVY_BLUE,
                                         float(15),
                                         bold=True,
                                         align="left")
        self.st_d_currentspeed = arcade.Text("Current Speed: ",
                                             rx_xposn - (rx_width / 2) + 20,
                                             h_5b,
                                             arcade.color.BLACK,
                                             float(15),
                                             bold=True,
                                             align="left")
        self.st_d_speedcalcnote = arcade.Text("Speed = (# of Levels) - Current Level + GAME_SPEED_FLOOR",
                                              rx_xposn - (rx_width / 2) + 20,
                                              h_5b - 25,
                                              arcade.color.GRAY,
                                              float(7),
                                              bold=True,
                                              align="left")
        self.st_d_framecounttitle = arcade.Text("Frame Counter: ",
                                                rx_xposn - (rx_width / 2) + 20,
                                                h_1,
                                                arcade.color.BLACK,
                                                float(15),
                                                bold=True,
                                                align="left")
        self.st_d_framecount = arcade.Text("filler_frame_count",
                                           rx_xposn - (rx_width / 2) + 200,
                                           h_1,
                                           arcade.color.BRIGHT_NAVY_BLUE,
                                           float(15),
                                           bold=True,
                                           align="left")
        self.st_d_fpstitle = arcade.Text("FPS: ",
                                         rx_xposn - (rx_width / 2) + 20,
                                         h_3,
                                         arcade.color.BLACK,
                                         float(15),
                                         bold=True,
                                         align="left")
        self.st_d_fps = arcade.Text("filler_t_4a",
                                    rx_xposn - (rx_width / 2) + 200,
                                    h_3,
                                    arcade.color.BRIGHT_NAVY_BLUE,
                                    float(15),
                                    bold=True,
                                    align="left")
        self.st_d_t4b = arcade.Text("filler_t_4b",
                                    rx_xposn - (rx_width / 2) + 200,
                                    h_4,
                                    arcade.color.BRIGHT_NAVY_BLUE,
                                    float(15),
                                    bold=True,
                                    align="left")
        self.st_d_time2update = arcade.Text("Time To Update: ",
                                            rx_xposn - (rx_width / 2) + 20,
                                            h_4,
                                            arcade.color.BLACK,
                                            float(15),
                                            bold=True,
                                            align="left")
        self.st_d_lvladvance = arcade.Text("Level Advance: ",
                                           rx_xposn - (rx_width / 2) + 20,
                                           h_2,
                                           arcade.color.BLACK,
                                           float(15),
                                           bold=True,
                                           align="left")
        self.st_d_t2a = arcade.Text("filler_t_2a",
                                    rx_xposn - (rx_width / 2) + 200,
                                    h_2,
                                    arcade.color.BRIGHT_NAVY_BLUE,
                                    float(15),
                                    bold=True,
                                    align="left")
        self.st_d_t2b = arcade.Text("filler_t_2b",
                                    rx_xposn - (rx_width / 2) + 200,
                                    h_2 - 30,
                                    arcade.color.BRIGHT_NAVY_BLUE,
                                    float(15),
                                    bold=True,
                                    align="left")
        self.st_d_t5b = arcade.Text("filler_t_5b",
                                    rx_xposn - (rx_width / 2) + 200,
                                    h_5b,
                                    arcade.color.BRIGHT_NAVY_BLUE,
                                    float(15),
                                    bold=True,
                                    align="left")

        # Setup Mini-Scoreboard (mscb)
        self.st_mscb_scoretitle = arcade.Text("SCORE",
                                              e_mscb_xposn - 65,
                                              e_mscb_yposn - e_mscb_height * 0,
                                              arcade.color.BLACK,
                                              float(SCREEN_HEIGHT * 0.013),
                                              bold=True,
                                              align="left",
                                              anchor_y="center")
        self.st_mscb_score = arcade.Text("",
                                         e_mscb_xposn - 50,
                                         e_mscb_yposn - e_mscb_height * 0.3,
                                         arcade.color.BLACK,
                                         float(SCREEN_HEIGHT * 0.030),
                                         bold=True,
                                         align="left",
                                         anchor_y="center")
        self.st_mscb_leveltitle = arcade.Text("LEVEL",
                                              e_mscb_xposn - 65,
                                              e_mscb_yposn + e_mscb_height * 0.4,
                                              arcade.color.BLACK,
                                              float(SCREEN_HEIGHT * 0.013),
                                              bold=True,
                                              align="left",
                                              anchor_y="center")
        self.st_mscb_level = arcade.Text("",
                                         e_mscb_xposn + 00,
                                         e_mscb_yposn + e_mscb_height * 0.2,
                                         arcade.color.BLACK,
                                         float(SCREEN_HEIGHT * 0.030),
                                         bold=True,
                                         align="left",
                                         anchor_y="center")

    def newGame(self, player_name):
        self.resetGame(player_name)
        self.setup()

    def resetGame(self, player_name):  # width, height, title removed
        """ Reset Last Gameplay and Reset Game Class Variables """

        self.board = None
        self.frame_count = 0  # reset game frame counter
        self.game_over = False  # reset game end state

        self.hdrop_wait = False  # Hard Drop Frequency Limiter
        self.hdrop_last_frame = 0

        self.paused = False
        self.addedScore = False

        self.board_sprite_list = None
        self.background = None

        # initialize score & player
        self.player_name = player_name
        self.st_player_name.value = f"{self.player_name}"
        self.score = None
        self.level = None
        self.GAME_SPEED = None

        self.left_pressed = False
        self.right_pressed = False
        self.down_pressed = False
        self.pos = 0
        self.new_stones = tetris_shapes.copy()
        random.shuffle(self.new_stones)

        # Output Announcement
        print("---- Game Board, Mechanics, Stats == Reset")

    def setup(self):
        """ Initialize Scoring System & Game Components """
        self.board = new_board()
        self.score = 0
        self.level = 0
        self.GAME_SPEED = INITIAL_GAME_SPEED
        self.background = arcade.load_texture(BACKGROUNDS[0])

        # Set Game Levels 1-9
        # self.GAME_LEVEL_FRAMES = [ 0, 300, 600,950,1300,1650,2050,2450,2900]
        self.GAME_LEVEL_FRAMES = [0, 200, 400, 600, 900, 1150, 1600, 1900, 2200]

        # RX & Statistics
        self.processing_time = 0
        self.draw_time = 0
        self.fps_start_timer = None
        self.fps = None

        self.board_sprite_list = arcade.SpriteList()
        for row in range(len(self.board)):
            for column in range(len(self.board[0])):
                sprite = arcade.Sprite()
                for texture in texture_list:
                    sprite.append_texture(texture)
                sprite.set_texture(0)
                sprite.center_x = (MARGIN + WIDTH) * column + SCREEN_MARGIN + WIDTH // 2 + WINDOW_MARGIN                # MAY NEED FIXED WITH NEW SCREEN SIZE
                sprite.center_y = TETRIS_HEIGHT - HIDE_BOTTOM - (MARGIN + HEIGHT) * row + SCREEN_MARGIN + HEIGHT // 2   # MAY NEED FIXED WITH NEW SCREEN SIZE

                self.board_sprite_list.append(sprite)

        # - JOYSTICK
        # Check for System Installed Joysticks. Make instance of it.
        joysticks = arcade.get_joysticks()
        if joysticks:
            self.joystick = joysticks[0]
            self.joystick.open()
        else:
            print("----NO JOYSTICK CONTROLLER WAS FOUND.")
            self.joystick = None

        # - Initial Stone
        self.new_stone()
        self.update_board()

        print("---- Game Board, Mechanics, Stats == SETUP Confirm")

    def on_show_view(self):
        print("GameView Opened!")
        arcade.set_background_color([187, 0, 0])  # Set Background. Required. Do not delete def!
        self.window.set_mouse_visible(False)  # Hide mouse cursor

    # -- Stone Actions

    def new_stone(self):
        """
        Randomly grab a new stone and set the stone location to the top.
        If we immediately collide, then game-over.        self.new_stone()
        """
        self.stone = self.new_stones.pop()
        if len(self.new_stones) is 0:
            self.new_stones = tetris_shapes.copy()
            random.shuffle(self.new_stones)
        self.stone_x = int(COLUMN_COUNT / 2 - len(self.stone[0]) / 2)
        self.stone_y = 0
        self.pos = 0
        if check_collision(self.board, self.stone, (self.stone_x, self.stone_y)):
            self.game_over = True
            ##--- ADD COMMAND TO SWITCH STATES TO "GAME-OVER" STATE WHEN GAME-ENDS

    def drop(self):
        """
        Drop the stone down one place.
        Check for collision.
        If collided, then
          join matrixes
          Check for rows we can remove
          Update sprite list with stones
          Create a new stone
        """
        if not self.game_over and not self.paused:
            self.stone_y += 1
            if check_collision(self.board, self.stone, (self.stone_x, self.stone_y)):
                self.board = join_matrixes(self.board, self.stone, (self.stone_x, self.stone_y))
                rows_cleared = 0
                for i, row in enumerate(self.board[:-1]):
                    if 0 not in row:
                        self.board = remove_row(self.board, i)
                        rows_cleared += 1
                    if i is 21:
                        self.score += [0, 40, 100, 300, 1200][rows_cleared] * (
                                    self.level + 1)  # self.score + 1   ##------------ADD GAME SCORE COUNTER LINE HERE
                print("Score:  " + str(self.score))
                self.update_board()
                self.new_stone()

    def hard_drop(self):
        """
        Drop the stone until collision
        Join
        Check for rows to remove
        Create new stone
        """

        if not self.game_over and not self.paused and (self.hdrop_last_frame + 10 < self.frame_count):
            while not check_collision(self.board, self.stone, (self.stone_x, self.stone_y)):
                self.stone_y += 1
            self.board = join_matrixes(self.board, self.stone, (self.stone_x, self.stone_y))
            while True:
                rows_cleared = 0
                for i, row in enumerate(self.board[:-1]):
                    if 0 not in row:
                        self.board = remove_row(self.board, i)
                        rows_cleared += 1
                    if i is 21:
                        self.score += [0, 40, 100, 300, 1200][rows_cleared] * (
                                    self.level + 1)  # self.score + 1   ##------------ADD GAME SCORE COUNTER LINE HERE
                else:
                    self.hdrop_last_frame = self.frame_count
                    break
                print("Score:  " + str(self.score))
            self.update_board()
            self.new_stone()

    def rotate_stone(self):
        """ Rotate the stone, check collision. """
        if not self.game_over and not self.paused:
            new_stone = rotate_clockwise(self.stone)
            new_pos = (self.pos + 1) % 4
            new_x = self.stone_x
            new_y = self.stone_y

            d = abs(len(self.stone) - len(self.stone[0]))
            if d is 3:
                x = 0
                if new_pos is 1:
                    new_x += 2
                    new_y -= 1
                elif new_pos is 2:
                    new_x -= 2
                    new_y += 2
                elif new_pos is 3:
                    new_x += 1
                    new_y -= 2
                else:
                    new_x -= 1
                    new_y += 1
            else:
                if new_pos is 1:
                    new_x += d
                elif new_pos is 2:
                    new_x -= d
                    new_y += d
                elif new_pos is 3:
                    new_y -= d

            # if rotates off board move back
            if new_x < 0:
                new_x = 0
            if new_x > COLUMN_COUNT - len(self.stone):
                new_x = COLUMN_COUNT - len(self.stone)
            if not check_collision(self.board, new_stone, (new_x, new_y)):
                self.stone = new_stone
                self.stone_x = new_x
                self.stone_y = new_y
                self.pos = new_pos

    def update(self, dt):
        """ Update, drop stone if warrented. Called by Arcade Class every 1/60 sec
        ------------------------------------ FRAME RATE CONTROLLING """
        self.frame_count += 1
        if self.frame_count % self.GAME_SPEED == 0:
            self.drop()

        if self.frame_count % 3 == 0:
            if self.down_pressed and self.frame_count - self.down_pressed > 10:
                self.drop()
            if not self.right_pressed and self.left_pressed and self.frame_count - self.left_pressed > 10:
                self.move(-1)
            elif not self.left_pressed and self.right_pressed and self.frame_count - self.right_pressed > 10:
                self.move(1)

    def move(self, delta_x):
        """ Move the stone back and forth based on delta x. """
        if not self.game_over and not self.paused:
            new_x = self.stone_x + delta_x
            if new_x < 0:
                new_x = 0
            if new_x > COLUMN_COUNT - len(self.stone[0]):
                new_x = COLUMN_COUNT - len(self.stone[0])
            if not check_collision(self.board, self.stone, (new_x, self.stone_y)):
                self.stone_x = new_x

    # -- Screen Elements

    def draw_background(self):
        """ Draws the most epic background ever imaginable. """
        arcade.draw_texture_rectangle(center_x=WINDOW_WIDTH // 2, center_y=SCREEN_HEIGHT // 2,
                                      width=SCREEN_WIDTH, height=SCREEN_HEIGHT,
                                      texture=self.background)

    def draw_next_stone(self):
        next_stone = self.new_stones[-1]
        color = max(next_stone[0])

        if color is 6:
            arcade.draw_rectangle_filled(next_xposn + WIDTH / 2 + MARGIN, next_yposn, WIDTH, HEIGHT, colors[6])
            arcade.draw_rectangle_filled(next_xposn - WIDTH / 2, next_yposn, WIDTH, HEIGHT, colors[6])
            arcade.draw_rectangle_filled(next_xposn + 1.5 * WIDTH + 2 * MARGIN, next_yposn, WIDTH, HEIGHT, colors[6])
            arcade.draw_rectangle_filled(next_xposn - 1.5 * WIDTH - MARGIN, next_yposn, WIDTH, HEIGHT, colors[6])
        elif color is 7:
            arcade.draw_rectangle_filled(next_xposn + WIDTH / 2 + MARGIN, next_yposn - HEIGHT / 2, WIDTH, HEIGHT,
                                         colors[7])
            arcade.draw_rectangle_filled(next_xposn - WIDTH / 2, next_yposn - HEIGHT / 2, WIDTH, HEIGHT, colors[7])
            arcade.draw_rectangle_filled(next_xposn + WIDTH / 2 + MARGIN, next_yposn + HEIGHT / 2 + MARGIN, WIDTH,
                                         HEIGHT, colors[7])
            arcade.draw_rectangle_filled(next_xposn - WIDTH / 2, next_yposn + HEIGHT / 2 + MARGIN, WIDTH, HEIGHT,
                                         colors[7])
        else:
            for x in range(3):
                for y in range(2):
                    if next_stone[y][x] is not 0:
                        arcade.draw_rectangle_filled(next_xposn + (x - 1) * (WIDTH + MARGIN),
                                                     next_yposn + (y * -2 + 1) * (HEIGHT / 2 + MARGIN),
                                                     WIDTH,
                                                     HEIGHT,
                                                     colors[color])

    def draw_diagnostics(self):

        # Box Outline
        arcade.draw_rectangle_outline(rx_xposn, rx_yposn, rx_width, rx_yposn, [0, 153, 153], 2)

        # Update Text Values
        self.st_d_framecount.value = str(self.frame_count)
        t_2a = str(self.GAME_LEVEL_FRAMES[0:5])
        t_2b = str(self.GAME_LEVEL_FRAMES[6:])
        self.st_d_t2a.value = t_2a
        self.st_d_t2b.value = t_2b

        if self.fps is not None:
            t_4a = f"{self.fps:.2f}"
            self.st_d_fps.value = t_4a
        if self.processing_time is not None:
            t_4b = f"{self.processing_time:.8f} seconds"
            self.st_d_t4b.value = t_4b

        t_5a = f"{GAME_SPEED_FLOOR} frames"  # Game Floor Speed
        self.st_d_t5a.value = t_5a

        if self.GAME_SPEED is not None:
            t_5b = f"{self.GAME_SPEED} frames"
            self.st_d_t5b.value = t_5b

        # Draw Text
        self.st_d_header.draw()
        self.st_d_setfloor.draw()
        self.st_d_adjustupdown.draw()
        self.st_d_t5a.draw()
        self.st_d_currentspeed.draw()
        self.st_d_speedcalcnote.draw()
        self.st_d_framecounttitle.draw()
        self.st_d_framecount.draw()
        self.st_d_fpstitle.draw()
        self.st_d_fps.draw()
        self.st_d_t4b.draw()
        self.st_d_time2update.draw()
        self.st_d_lvladvance.draw()
        self.st_d_t2a.draw()
        self.st_d_t2b.draw()
        self.st_d_t5b.draw()

    def draw_grid(self, grid, offset_x, offset_y):
        """ Draw the grid. Used to draw the falling stones. The board is drawn by the sprite list. """
        # Draw the grid
        for row in range(len(grid)):
            for column in range(len(grid[0])):
                # Figure out what color to draw the box
                if grid[row][column]:
                    color = colors[grid[row][column]]
                    # Do the math to figure out where the box is
                    x = (MARGIN + WIDTH) * (
                                column + offset_x) + SCREEN_MARGIN + WIDTH // 2 + WINDOW_MARGIN  # MAY NEED FIXED WITH NEW SCREEN SIZE
                    y = TETRIS_HEIGHT - HIDE_BOTTOM - (MARGIN + HEIGHT) * (
                                row + offset_y) + SCREEN_MARGIN + HEIGHT // 2  # MAY NEED FIXED WITH NEW SCREEN SIZE

                    # Draw the box
                    arcade.draw_rectangle_filled(x, y, WIDTH, HEIGHT, color)

    def on_draw(self):
        """ Render the screen. """

        # RX & Statistics
        start_time = timeit.default_timer()
        fps_calc_freq = 60
        if self.frame_count % fps_calc_freq == 0:
            if self.fps_start_timer is not None:
                t_total = timeit.default_timer() - self.fps_start_timer
                self.fps = fps_calc_freq / t_total
            self.fps_start_timer = timeit.default_timer()  # restart timer

        # Setup Rendering Environment
        arcade.start_render()

        # Individual Render Functions
        self.draw_background()
        self.draw_next_stone()
        self.draw_current_player()
        self.draw_mscb()
        self.draw_diagnostics()

        self.board_sprite_list.draw()
        self.draw_grid(self.stone, self.stone_x, self.stone_y)

        # Draw Advert Content
        arcade.draw_rectangle_filled(WINDOW_WIDTH / 2, 72, SCREEN_WIDTH, HEIGHT, arcade.color.BLACK)
        self.st_adtxt.draw()

        # Game State Control Elements
        if self.game_over and not self.addedScore:
            ALL_SCORES.append(
                [self.score, self.player_name, self.level])  # calls to function to add player to leaderboard
            self.addedScore = True
            ALL_SCORES.sort(reverse=True)
            saveScores(ALL_SCORES)
            print("Added score & Sorted Scoreboard")
            print(ALL_SCORES)

        if self.game_over:
            self.game_over_cover()

    def game_over_cover(self):
        time.sleep(.2)
        arcade.draw_rectangle_filled(WINDOW_WIDTH / 2,
                                     SCREEN_HEIGHT / 2,
                                     SCREEN_WIDTH,
                                     SCREEN_HEIGHT,
                                     (0, 0, 0, 200))

        gameover = arcade.load_texture(GAME_OVER)
        arcade.draw_texture_rectangle(center_x=WINDOW_WIDTH // 2,
                                      center_y=SCREEN_HEIGHT * 5 / 6,
                                      width=SCREEN_WIDTH * 0.7,
                                      height=SCREEN_WIDTH * 0.4,
                                      texture=gameover)

        # player and score
        name = self.player_name
        score = str(self.score)
        goc_t1 = arcade.Text("CHALLENGER",
                    WINDOW_WIDTH / 2,
                    SCREEN_HEIGHT * 7 / 12,
                    width=SCREEN_WIDTH,
                    color=arcade.color.WHITE,
                    font_size=30,
                    bold=True,
                    align="center",
                    anchor_x="center",
                    anchor_y="center")
        goc_t2 = arcade.Text(name,
                    WINDOW_WIDTH / 2,
                    SCREEN_HEIGHT * 7 / 12 - 80,
                    width=SCREEN_WIDTH,
                    color=arcade.color.WHITE,
                    font_size=40,
                    bold=True,
                    align="center",
                    anchor_x="center")
        goc_t3 = arcade.Text("SCORE",
                    WINDOW_WIDTH / 2,
                    SCREEN_HEIGHT * 5 / 12,
                    width=SCREEN_WIDTH,
                    color=arcade.color.WHITE,
                    font_size=30,
                    bold=True,
                    align="center",
                    anchor_x="center",
                    anchor_y="center")
        goc_t4 = arcade.Text(score,
                    WINDOW_WIDTH / 2,
                    SCREEN_HEIGHT * 5 / 12 - 60,
                    width=SCREEN_WIDTH,
                    color=arcade.color.WHITE,
                    font_size=40,
                    bold=True,
                    align="center",
                    anchor_x="center",
                    anchor_y="center")

        goc_t1.draw()
        goc_t2.draw()
        goc_t3.draw()
        goc_t4.draw()

    def switch_to_leaderboard(self):
        time.sleep(3)
        next_view = LBView()
        next_view.setup(self.score, self.player_name)
        self.window.show_view(next_view)

    def draw_current_player(self):
        """ Draw the current player name over the mini score board. """
        self.st_player_title.draw()
        self.st_player_name.draw()

    def draw_mscb(self):
        """ Draw the mini score board when the player start playing. """

        # Update Text Content
        self.st_mscb_score.value = f"{self.score}"
        self.st_mscb_level.value = f"{self.level}"

        # Draw
        arcade.draw_rectangle_outline(e_mscb_xposn, e_mscb_yposn, e_mscb_width, e_mscb_height, [0, 153, 153], 2)
        self.st_mscb_scoretitle.draw()
        self.st_mscb_score.draw()
        self.st_mscb_leveltitle.draw()
        self.st_mscb_level.draw()
        arcade.draw_rectangle_outline(next_xposn, next_yposn, next_width, next_height, [0, 153, 153], 2)

    # -- Game Logic

    def update(self, dt):
        """ Update, drop stone if warranted. Called by Arcade Class every 1/60 sec"""

        # RX & Statistics (start timer)
        start_time = timeit.default_timer()

        # ------------------------------------ FRAME RATE CONTROL
        self.frame_count += 1

        if self.game_over == True:
            self.switch_to_leaderboard()

        if self.frame_count % self.GAME_SPEED == 0:
            if self.joystick and (self.joystick.y > 0.6):   self.drop()  # DOWN (vertical is flipped on input)
            self.drop()

            # - Update Game Speed
            self.level_up()

        # - JOYSTICK
        # if self.joystick and (self.frame_count % 3 == 0):
        #     """JoyStick Control Input"""
        #     if self.joystick.x < -0.6:   self.move(-1)        # LEFT
        #     if self.joystick.x > 0.6:   self.move(1)          # RIGHT
        #     if self.joystick.y < -0.6:   self.hard_drop()     # UP

        # - KEYBOARD
        if self.frame_count % 3 == 0:
            if self.down_pressed and self.frame_count - self.down_pressed > 10:
                self.drop()
            if not self.right_pressed and self.left_pressed and self.frame_count - self.left_pressed > 10:
                self.move(-1)
            elif not self.left_pressed and self.right_pressed and self.frame_count - self.right_pressed > 10:
                self.move(1)

        # RX & Statistics (stop timer)
        self.processing_time = timeit.default_timer() - start_time

    def level_up(self):
        """ increase game speed as game progresses. ie. Get's faster the longer you play"""

        idx = len(self.GAME_LEVEL_FRAMES) - 1
        while idx >= 0:
            if self.GAME_LEVEL_FRAMES[idx] < self.frame_count:
                self.level = idx
                self.GAME_SPEED = len(self.GAME_LEVEL_FRAMES) - idx + GAME_SPEED_FLOOR
                break
            idx -= 1

    def update_board(self):
        """
        Update the sprite list to reflect the contents of the 2d grid
        """
        for row in range(len(self.board)):
            for column in range(len(self.board[0])):
                v = self.board[row][column]
                i = row * COLUMN_COUNT + column
                self.board_sprite_list[i].set_texture(v)

    def on_key_press(self, key, modifiers):
        """
        Handle user key presses
        User goes left, move -1
        User goes right, move 1
        Rotate stone,
        or drop down

        F1 = MENU
        F2 = LeaderBoard
        F3 = Game Reset
        """
        global GAME_SPEED_FLOOR

        # GAME Play Commands
        if key == arcade.key.LEFT:
            self.left_pressed = self.frame_count
            self.move(-1)
        elif key == arcade.key.RIGHT:
            self.right_pressed = self.frame_count
            self.move(1)
        elif key == arcade.key.UP:
            self.rotate_stone()
        elif key == arcade.key.DOWN or key == 101:
            self.down_pressed = self.frame_count
            self.drop()
        elif key == arcade.key.SPACE or key == 113:
            self.hard_drop()

        # GAME Central Commands
        elif key == 65470:
            print("---- MAIN MENU")
            next_view = MenuView()
            self.window.show_view(next_view)
        elif key == 65471 or key == 65474:
            print("---- LEADER BOARD")
            next_view = LBView()
            next_view.setup()
            self.window.show_view(next_view)
        elif key == 65472:
            print("---- NEW PLAYER")
            next_view = PNameView()
            next_view.setup()
            self.window.show_view(next_view)

        elif key == 65365:
            GAME_SPEED_FLOOR += 1
            print("---- GAME_SPEED_FLOOR = " + str(GAME_SPEED_FLOOR))
        elif key == 65366:
            if GAME_SPEED_FLOOR > 0: GAME_SPEED_FLOOR -= 1
            print("---- GAME_SPEED_FLOOR = " + str(GAME_SPEED_FLOOR))

    def on_key_release(self, key, modifiers):
        """
        Handle user key presses
        User goes left, move -1
        User goes right, move 1
        Rotate stone,
        or drop down

        F1 = MENU
        F2 = LeaderBoard
        F3 = Game Reset
        """
        # GAME Play Commands
        if key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.RIGHT:
            self.right_pressed = False
        elif key == arcade.key.DOWN:
            self.down_pressed = False



######################
## Class: Main Menu ##
######################

class MenuView(arcade.View):

    def on_show_view(self):
        arcade.set_background_color([187,0,0])                                  # Set Background. Required. Do not delete def!

    def on_draw(self):
        arcade.start_render()

        # BACKGROUND
        self.background = arcade.load_texture(BACKGROUNDS[1])
        arcade.draw_texture_rectangle(  center_x = WINDOW_WIDTH // 2,  center_y = SCREEN_HEIGHT // 2,
                                        width    = SCREEN_WIDTH,    height   = SCREEN_HEIGHT,
                                        texture  = self.background )

        # BUTTON GRAPHICS :D
        # Buttons are not intended to be clickable
        button = arcade.load_texture(BUTTONS[0])
        arcade.draw_texture_rectangle(  center_x=WINDOW_WIDTH // 2, center_y=SCREEN_HEIGHT // 2 + TOWER_BUFFER,
                                        width= SCREEN_WIDTH*0.58, height= SCREEN_HEIGHT*0.04, texture=button)
        button = arcade.load_texture(BUTTONS[1])
        arcade.draw_texture_rectangle(  center_x=WINDOW_WIDTH // 2, center_y=SCREEN_HEIGHT // 2 - (SCREEN_HEIGHT*0.05) + TOWER_BUFFER,
                                        width= SCREEN_WIDTH*0.58, height= SCREEN_HEIGHT*0.04, texture=button)
        button = arcade.load_texture(BUTTONS[2])
        arcade.draw_texture_rectangle(  center_x=WINDOW_WIDTH // 2, center_y=SCREEN_HEIGHT // 2 - (SCREEN_HEIGHT*0.1) + TOWER_BUFFER,
                                        width= SCREEN_WIDTH*0.58, height= SCREEN_HEIGHT*0.04, texture=button)

    def on_mouse_press(self, x, y, button, modifiers):
        print("Clicking doesn't do anything")

    def on_key_press(self, key, modifiers):
        if key == 65470:
            print("---- RELOAD MAIN MENU")
            next_view = MenuView()
            self.window.show_view(next_view)
        if key == 65471 or key == 65474:
            print("---- LEADER BOARD")
            next_view = LBView()
            next_view.setup()
            self.window.show_view(next_view)
        if key == 65472:
            print("---- NEW PLAYER")
            next_view = PNameView()
            next_view.setup()
            self.window.show_view(next_view)

        if key == 65307: arcade.close_window()



#######################
## Class: New Player ##
#######################

class PNameView(arcade.View):

    def __init__(self):
        """
        Setup variables for view class
        """
        super(PNameView, self).__init__()

        # Load Texture Content
        self.background = arcade.load_texture(BACKGROUNDS[3])

        # Default Logic
        self.player_name = ''
        self.READY_TO_PLAY = False

        # Active Content (declaration only)
        self.txt_name = arcade.Text(self.player_name,
                                    start_x=WINDOW_WIDTH // 2 - 127,
                                    start_y=SCREEN_HEIGHT * 0.54,
                                    color=arcade.color.BLACK,
                                    font_size=20,
                                    width=int(SCREEN_WIDTH * 0.731),
                                    align="center")
        self.txt_ready = arcade.Text("READY TO PLAY",
                                     start_x=SCREEN_WIDTH / 2 + WINDOW_MARGIN,
                                     start_y=SCREEN_HEIGHT * 0.482,
                                     color=arcade.color.BLACK,
                                     font_size=float(SCREEN_HEIGHT * 0.02),
                                     bold=True,
                                     width=SCREEN_WIDTH - 2,
                                     align="center",
                                     anchor_x="center",
                                     anchor_y="center")

    def setup(self):
        """Reset logic"""
        self.player_name = ''
        self.READY_TO_PLAY = False

    def on_show_view(self):
        """Called once when first shown. Loads static visuals."""
        arcade.start_render()  # Clear current window before starting

        # Background
        arcade.set_background_color([187, 0, 0])  # Set base color. Required.

    def on_draw(self):
        self.clear()

        # Background
        arcade.draw_texture_rectangle(center_x=WINDOW_WIDTH // 2,
                                      center_y=SCREEN_HEIGHT // 2,
                                      width=SCREEN_WIDTH,
                                      height=SCREEN_HEIGHT,
                                      texture=self.background)

        # Update current players name
        self.txt_name.value = self.player_name
        self.txt_name.draw()

        # Player ready notice
        if self.READY_TO_PLAY:
            self.txt_ready.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        print("Clicking doesn't do anything")

    def on_key_press(self, key, modifiers):

        if key == 65470:
            print("---- MAIN MENU")
            next_view = MenuView()
            self.window.show_view(next_view)

        if key == 65471:                     #exclude Console Control Button F5
            print("---- LEADER BOARD")
            next_view = LBView()
            next_view.setup()
            self.window.show_view(next_view)

        if key == 65472:
            print("---- RELOAD NEW PLAYER")
            next_view = PNameView()
            next_view.setup()
            self.window.show_view(next_view)
        if key==65293 or key==65421:   #USES ENTER KEYS OR F4
            self.READY_TO_PLAY = True

        if not self.READY_TO_PLAY:
            # For name input
            if 96 < key < 123:
                self.player_name += str(['a', 'b', 'c', 'd', 'e', 'f', 'g',
                                         'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
                                         's', 't', 'u', 'v', 'w', 'x', 'y', 'z'][key-97]).upper()
            elif 47 < key < 58:
                self.player_name += str(key-48)
            elif 65455 < key <65466:
                self.player_name += str(key-65456)
            elif key == 65454:
                self.player_name += '.'
            elif key == arcade.key.PERIOD:
                self.player_name += '.'
            elif key == arcade.key.BACKSPACE:
                self.player_name = self.player_name[:-1]
            elif key == 45 or key == 65453:
                self.player_name += '-'

        elif self.READY_TO_PLAY:
            if key == 65361 or key == 65362 or key == 65363 or key == 65364 or key==32 or key==65473: #uses any keyboard motion key or F4
                if len(self.player_name) is 0:
                    print("Name can't be empty")
                    self.setup()
                    return

                # Create new instance of game and switch to that view
                print("---- LAUNCH GAME")
                next_view = GameView()
                next_view.newGame(self.player_name)
                self.window.show_view(next_view)



########################
## Class: Leaderboard ##
########################

class LBView(arcade.View):

    def __init__(self):
        super(LBView, self).__init__()

        # Background Texture
        self.background = arcade.load_texture(BACKGROUNDS[2])

    def on_show_view(self):
        """Called once when view switched to this class. Writes all static elements"""

        # Set Background. Required. Do not delete def!
        arcade.set_background_color([187,0,0])

        # Clear pixels from current window
        self.clear()

        # Draw Background Texture
        arcade.draw_texture_rectangle(center_x=WINDOW_WIDTH // 2,
                                      center_y=SCREEN_HEIGHT // 2,
                                      width=SCREEN_WIDTH,
                                      height=SCREEN_HEIGHT,
                                      texture=self.background)

        # Populate Leaderboard
        currentRowHeight = SCREEN_HEIGHT * 0.813 + 1
        for row in ALL_SCORES[0:34]:
            if row[0] is self.score and str(row[1]) is self.name:
                arcade.draw_rectangle_filled(WINDOW_WIDTH//2 - 48, currentRowHeight-1, 84, 15, [49,142,203])
                arcade.draw_rectangle_filled(WINDOW_WIDTH//2 + 70, currentRowHeight-1, 150, 15, [49,142,203])
            arcade.draw_text( str(row[0]),
                         start_x=WINDOW_WIDTH//2 - 50,
                         start_y=currentRowHeight,
                         anchor_x="center",
                         anchor_y="center",
                         width=SCREEN_WIDTH,
                         color=arcade.color.WHITE,
                         font_size=float(SCREEN_HEIGHT*0.010),
                         font_name='arial',
                         align="center",
                         bold=False)
            arcade.draw_text( str(row[1]),
                         start_x=WINDOW_WIDTH//2 + 70,
                         start_y=currentRowHeight,
                         anchor_x="center",
                         anchor_y="center",
                         width=SCREEN_WIDTH,
                         color=arcade.color.WHITE,
                         font_size=float(SCREEN_HEIGHT*0.010),
                         font_name='arial',
                         align="center",
                         bold=True)
            currentRowHeight -= SCREEN_HEIGHT * 0.01685

    def on_draw(self):
        pass

    def setup(self, score = None, name = None):
        print("Setup Leaderboard")
        self.score = score
        self.name = name

    def on_mouse_press(self, x, y, button, modifiers):
        print("Clicking doesn't do anything")

    def on_key_press(self, key, modifiers):
        if key == 65470:
            print("---- MAIN MENU")
            next_view = MenuView()
            self.window.show_view(next_view)
        if key == 65471 or key == 65474:
            print("---- RELOAD LEADER BOARD")
            next_view = LBView()
            next_view.setup()
            self.window.show_view(next_view)
        if key == 65472:
            print("---- NEW PLAYER")
            next_view = PNameView()
            next_view.setup()
            self.window.show_view(next_view)



##########
## Main ##
##########

def main():
    """ Create the game window, setup, run
        #TO-DO load leaderboard file and send to game (?)
    """

    # Initialize
    global ALL_SCORES
    global GAME_SPEED_FLOOR

    ALL_SCORES = [   [0,"Brutus",   0],
                     [1,"TomWDavis",0]  ]
    GAME_SPEED_FLOOR = 5
    FULL_SCREEN = False

    # Setup Questions
    askScores = input("Import Scores? (n/null): ")
    if input("Full Screen?   (y/null): ") != 'n': FULL_SCREEN = True

    # Import Old Scoreboard
    if askScores != "n" or askScores != "N": ALL_SCORES = importScores()
    print(ALL_SCORES)


    # Game launch
    window = arcade.Window(width=SCREEN_WIDTH, height=SCREEN_HEIGHT, title=SCREEN_TITLE, fullscreen=FULL_SCREEN, resizable=True)
    window.set_mouse_visible(False)

    # Launch Game
    menu_view = MenuView()   #start game in MenuView()
    window.show_view(menu_view)

    arcade.run()


if __name__ == "__main__":
    main()
