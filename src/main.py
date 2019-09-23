"""
BUCKEYE TETROMINOES
Coded by:  Adam Buynak in collaboration w/ The Ohio State University's OHI/O
Game Logic Sourced from Arcade Sample Code library.
Distributed under the MIT LICENSE.
"""
################################################################################

import arcade
import random
import PIL

from game_variables import *
from game_scores import *

################################################################################

################################################################################


def create_textures():
    """ Create a list of images for sprites based on the global colors.
	    !!! SHOULD be able to add custom images in here instead of the general colors."""
    texture_list = []
    for color in colors:
        image = PIL.Image.new('RGB', (WIDTH, HEIGHT), color)
        texture_list.append(arcade.Texture(str(color), image=image))
    return texture_list

texture_list = create_textures()

def rotate_clockwise(shape):
    """ Rotates a matrix clockwise """
    return [[shape[y][x] for y in range(len(shape))] for x in range(len(shape[0]) - 1, -1, -1)]
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
    board += [[1 for x in range(COLUMN_COUNT)]]
    return board

class GameView(arcade.View):
    global ALL_SCORES

    def newGame(self, player_name):
        self.resetGame(player_name)
        self.setup()
    def resetGame(self, player_name): #width, height, title removed
        """ Reset Last Gameplay and Reset Game Class Variables """

        self.board = None
        self.frame_count = 0                #reset game frame counter
        self.game_over = False              #reset game end state

        self.paused = False
        self.addedScore = False

        self.board_sprite_list = None
        self.background = None

        # initialize score & player
        self.player_name = player_name
        self.score = None
        self.level = None
        self.GAME_SPEED = None

        #Output Announcement
        print("---- Game Board, Mechanics, Stats == Reset")
    def setup(self):
        """ Initialize Scoring System & Game Components """
        self.board = new_board()
        self.score = 0
        self.level = 0
        self.GAME_SPEED = INITIAL_GAME_SPEED
        self.background = arcade.load_texture(BACKGROUNDS[0])

        self.board_sprite_list = arcade.SpriteList()
        for row in range(len(self.board)):
            for column in range(len(self.board[0])):
                sprite = arcade.Sprite()
                for texture in texture_list:
                    sprite.append_texture(texture)
                sprite.set_texture(0)
                sprite.center_x = (MARGIN + WIDTH) * column + SCREEN_MARGIN + WIDTH // 2                                # MAY NEED FIXED WITH NEW SCREEN SIZE
                sprite.center_y = TETRIS_HEIGHT - HIDE_BOTTOM - (MARGIN + HEIGHT) * row + SCREEN_MARGIN + HEIGHT // 2   # MAY NEED FIXED WITH NEW SCREEN SIZE

                self.board_sprite_list.append(sprite)

        self.new_stone()
        self.update_board()


        print("---- Game Board, Mechanics, Stats == SETUP Confirm")

    def on_show(self):
        print("GameView Opened!")
        arcade.set_background_color(arcade.color.GREEN)                         # Set Background. Required. Do not delete def!
        self.window.set_mouse_visible(False)                                    # Hide mouse cursor


#-- Stone Actions

    def new_stone(self):
        """
        Randomly grab a new stone and set the stone location to the top.
        If we immediately collide, then game-over.
        """
        self.stone = random.choice(tetris_shapes)
        self.stone_x = int(COLUMN_COUNT / 2 - len(self.stone[0]) / 2)
        self.stone_y = 0

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
                while True:
                    for i, row in enumerate(self.board[:-1]):
                        if 0 not in row:
                            self.board = remove_row(self.board, i)
                            self.score = self.score + 1  # 40*(self.level+1)    ##------------ADD GAME SCORE COUNTER LINE HERE
                            print("Score:  " + str(self.score))
                            break
                    else:
                        break
                self.update_board()
                self.new_stone()

    def hard_drop(self):
        """
        Drop the stone until collision
        Join
        Check for rows to remove
        Create new stone
        """
        if not self.game_over and not self.paused:
            while not check_collision(self.board, self.stone, (self.stone_x, self.stone_y)):
                self.stone_y += 1
            self.board = join_matrixes(self.board, self.stone, (self.stone_x, self.stone_y))
            while True:
                for i, row in enumerate(self.board[:-1]):
                    if 0 not in row:
                        self.board = remove_row(self.board, i)
                        self.score = self.score + 1  # 40*(self.level+1)    ##------------ADD GAME SCORE COUNTER LINE HERE
                        print(self.score)
                        break
                else:
                    break
            self.update_board()
            self.new_stone()

    def rotate_stone(self):
        """ Rotate the stone, check collision. """
        if not self.game_over and not self.paused:
            new_stone = rotate_clockwise(self.stone)
            # if rotates off board move back
            if self.stone_x > COLUMN_COUNT - len(self.stone):
                self.stone_x = COLUMN_COUNT - len(self.stone)
            if not check_collision(self.board, new_stone, (self.stone_x, self.stone_y)):
                self.stone = new_stone

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


#-- Screen Elements

    def draw_background(self):
        """ Draws the most epic background ever imaginable. """
        #backing = arcade.load_texture(BACKGROUNDS[0])
        arcade.draw_texture_rectangle(  center_x = SCREEN_WIDTH // 2,  center_y = SCREEN_HEIGHT // 2,
                                        width    = SCREEN_WIDTH,       height   = SCREEN_HEIGHT,
                                        texture  = self.background )

    def draw_grid(self, grid, offset_x, offset_y):
        """
        Draw the grid. Used to draw the falling stones. The board is drawn by the sprite list.
        """
        # Draw the grid
        for row in range(len(grid)):
            for column in range(len(grid[0])):
                # Figure out what color to draw the box
                if grid[row][column]:
                    color = colors[grid[row][column]]
                    # Do the math to figure out where the box is
                    x = (MARGIN + WIDTH) * (column + offset_x) + SCREEN_MARGIN + WIDTH // 2                    #MAY NEED FIXED WITH NEW SCREEN SIZE
                    y = TETRIS_HEIGHT - HIDE_BOTTOM - (MARGIN + HEIGHT) * (row + offset_y) + SCREEN_MARGIN + HEIGHT // 2     #MAY NEED FIXED WITH NEW SCREEN SIZE

                    # Draw the box
                    arcade.draw_rectangle_filled(x, y, WIDTH, HEIGHT, color)

    def on_draw(self):
        """ Render the screen. """

        # This command has to happen before we start drawing
        arcade.start_render()

        self.draw_background()
        self.build_mscb()
        self.write_name()

        self.board_sprite_list.draw()
        self.draw_grid(self.stone, self.stone_x, self.stone_y)

        if self.game_over == True and self.addedScore == False :
            ALL_SCORES.append( [ self.score, self.player_name, self.level ] )       #calls to function to add player to leaderboard
            self.addedScore = True
            ALL_SCORES.sort(reverse = True )
            saveScores(ALL_SCORES)
            print("Added score & Sorted Scoreboard")
            print(ALL_SCORES)

    def write_name(self):
        """ Draw the mini score board when the player start playing. """
        player_name = f"{self.player_name}"
        arcade.draw_text("- CURRENT CHALLENGER -", SCREEN_WIDTH/2, SCREEN_HEIGHT*0.94, arcade.color.CADET_GREY,  float(SCREEN_HEIGHT*0.021), align="center", anchor_x="center", anchor_y="center")
        arcade.draw_text(player_name, SCREEN_WIDTH/2, SCREEN_HEIGHT*0.90, arcade.color.CADET_GREY,  float(SCREEN_HEIGHT*0.02), bold=True, width=340, align="center", anchor_x="center", anchor_y="center")


    def build_mscb(self):
        """ Draw the mini score board when the player start playing. """
        score_text = f"{self.score}"
        level_text = f"{self.level}"
        arcade.draw_rectangle_outline(e_mscb_xposn, e_mscb_yposn, e_mscb_width, e_mscb_height, [0,153,153], 2)
        arcade.draw_text("SCORE",    e_mscb_xposn-int(0.35*SCREEN_WIDTH),  e_mscb_yposn - e_mscb_height*0.25, arcade.color.BLACK, float(SCREEN_HEIGHT*0.013),  bold = True, align="left", anchor_x="center", anchor_y="center")
        arcade.draw_text(score_text, e_mscb_xposn-int(0.22*SCREEN_WIDTH),   e_mscb_yposn - e_mscb_height*0.25, arcade.color.BLACK, float(SCREEN_HEIGHT*0.015), bold = True, align="left", anchor_x="center", anchor_y="center")
        arcade.draw_text("LEVEL",    e_mscb_xposn-int(0.35*SCREEN_WIDTH),  e_mscb_yposn + e_mscb_height*0.25, arcade.color.BLACK, float(SCREEN_HEIGHT*0.013),  bold = True, align="right", anchor_x="center", anchor_y="center")
        arcade.draw_text(level_text, e_mscb_xposn-int(0.22*SCREEN_WIDTH),   e_mscb_yposn + e_mscb_height*0.25, arcade.color.BLACK, float(SCREEN_HEIGHT*0.015), bold = True, align="left", anchor_x="center", anchor_y="center")


#-- Game Logic

    def update(self, dt):
        """ Update, drop stone if warrented. Called by Arcade Class every 1/60 sec
		------------------------------------ FRAME RATE CONTROLLING """
        self.frame_count += 1
        if self.frame_count % self.GAME_SPEED == 0:
            self.drop()

        #GAME LEVEL CONTROLLER & SPEED UPDATER----------------------------------SPEED CONTROLLER
        if self.score >= ((self.level+1) * 2):
            self.level += 1
            print("Level:  " + str(self.level) )
            if self.GAME_SPEED > 0:
                self.GAME_SPEED -= 1

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
        # GAME Play Commands
        if key == arcade.key.LEFT:
            self.move(-1)
        elif key == arcade.key.RIGHT:
            self.move(1)
        elif key == arcade.key.UP:
            self.rotate_stone()
        elif key == arcade.key.DOWN:
            self.drop()
        elif key == arcade.key.SPACE:
            self.hard_drop()

        # GAME Central Commands
        elif key == 65470:
            print("---- Switch to MAIN MENU")
            next_view = MenuView()
            self.window.show_view(next_view)
        elif key == 65471:
            print("---- Switch to LEADER BOARD")
            next_view = LBView()
            next_view.setup()
            self.window.show_view(next_view)
        elif key == 65472:
            print("RESET GAME")
            next_view = GameView()
            next_view.newGame('')
            self.window.show_view(next_view)
        elif key == 65473:
            print("ENTER NAME")
            next_view = PNameView()
            next_view.setup()
            self.window.show_view(next_view)


#===============================================================================
class MenuView(arcade.View):

    def on_show(self):
        arcade.set_background_color(arcade.color.GREEN)                         # Set Background. Required. Do not delete def!

    def on_draw(self):
        arcade.start_render()

        # BACKGROUND
        self.background = arcade.load_texture(BACKGROUNDS[1])
        arcade.draw_texture_rectangle(  center_x = SCREEN_WIDTH // 2,  center_y = SCREEN_HEIGHT // 2,
                                        width    = SCREEN_WIDTH,    height   = SCREEN_HEIGHT,
                                        texture  = self.background )
        # BUTTON GRAPHICS :D
        # Buttons are not intended to be clickable
        button = arcade.load_texture(BUTTONS[0])
        arcade.draw_texture_rectangle(  center_x=SCREEN_WIDTH // 2, center_y=SCREEN_HEIGHT // 2,
                                        width= SCREEN_WIDTH*0.58, height= SCREEN_HEIGHT*0.04, texture=button)
        button = arcade.load_texture(BUTTONS[1])
        arcade.draw_texture_rectangle(  center_x=SCREEN_WIDTH // 2, center_y=SCREEN_HEIGHT // 2 - (SCREEN_HEIGHT*0.05),
                                        width= SCREEN_WIDTH*0.58, height= SCREEN_HEIGHT*0.04, texture=button)
        button = arcade.load_texture(BUTTONS[2])
        arcade.draw_texture_rectangle(  center_x=SCREEN_WIDTH // 2, center_y=SCREEN_HEIGHT // 2 - (SCREEN_HEIGHT*0.1),
                                        width= SCREEN_WIDTH*0.58, height= SCREEN_HEIGHT*0.04, texture=button)


        # TEXT - using graphic/textures for buttons now
        #arcade.draw_text("[S] BEGIN GAME", SCREEN_WIDTH/2, SCREEN_HEIGHT/2,
        #                 arcade.color.CADET_GREY, font_size=15, font_name='arial',
        #                 align="center", anchor_x="center", anchor_y="center")
        #arcade.draw_text("[L] LEADER BOARD", SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 30,
        #                 arcade.color.CADET_GREY, font_size=15, font_name='arial',
        #                 align="center", anchor_x="center", anchor_y="center")


    def on_mouse_press(self, x, y, button, modifiers):
        print("toast... clicking doesn't do anything")

    def on_key_press(self, key, modifiers):
        if key == 65470:
            print("RELOAD MAIN MENU")
            next_view = MenuView()
            self.window.show_view(next_view)
        if key == 65471:
            print("---- Switch to LEADER BOARD")
            next_view = LBView()
            next_view.setup()
            self.window.show_view(next_view)
        if key == 65472:
            print("START NEW GAME")
            next_view = GameView()
            next_view.newGame('')
            self.window.show_view(next_view)
        if key == 65473:
            print("ENTER NAME")
            next_view = PNameView()
            next_view.setup()
            self.window.show_view(next_view)
        if key == 65307: arcade.close_window()

#===============================================================================
class LBView(arcade.View):

    def on_show(self):
        # Set Background. Required. Do not delete def!
        arcade.set_background_color(arcade.color.GREEN)

    def on_draw(self):
        arcade.start_render()

        # BACKGROUND
        self.background = arcade.load_texture(BACKGROUNDS[2])
        arcade.draw_texture_rectangle(  center_x = SCREEN_WIDTH // 2,  center_y = SCREEN_HEIGHT // 2,
                                        width    = SCREEN_WIDTH,       height   = SCREEN_HEIGHT,
                                        texture  = self.background )

        # Populate Leaderboard
        currentRowHeight = SCREEN_HEIGHT * 0.8
        for row in ALL_SCORES[0:34]:
            arcade.draw_text( str(row[0]), start_x= SCREEN_WIDTH * 0.353, start_y= currentRowHeight,
                              anchor_x = "center", anchor_y = "center",
                              color= arcade.color.WHITE,
                              font_size=float(SCREEN_HEIGHT*0.015),
                              font_name='arial',
                              align= "center", bold = True)
            arcade.draw_text( str(row[1]), start_x= SCREEN_WIDTH * 0.718, start_y= currentRowHeight,
                              anchor_x = "center", anchor_y = "center",
                              color= arcade.color.WHITE,
                              font_size=float(SCREEN_HEIGHT*0.015),
                              font_name='arial-bold',
                              align= "center", bold = True)
            currentRowHeight -= SCREEN_HEIGHT * 0.018055



    def setup(self):
        print("FIXME - Build 'Setup' in LeaderBoard")

    def on_mouse_press(self, x, y, button, modifiers):
        print("toast... clicking doesn't do anything")

    def on_key_press(self, key, modifiers):
        if key == 65470:
            print("SWITCH TO MAIN MENU")
            next_view = MenuView()
            self.window.show_view(next_view)
        if key == 65471:
            print("RELOAD LEADER BOARD")
            next_view = LBView()
            next_view.setup()
            self.window.show_view(next_view)
        if key == 65472:
            print("START NEW GAME")
            next_view = GameView()
            next_view.newGame('')
            self.window.show_view(next_view)
        if key == 65473:
            print("ENTER NAME")
            next_view = PNameView()
            next_view.setup()
            self.window.show_view(next_view)
#===============================================================================
class PNameView(arcade.View):

    def on_show(self):
        # Set Background. Required. Do not delete def!
        arcade.set_background_color(arcade.color.GREEN)

    def on_draw(self):
        arcade.start_render()

        # BACKGROUND
        self.background = arcade.load_texture(BACKGROUNDS[3])
        arcade.draw_texture_rectangle(  center_x = SCREEN_WIDTH // 2,  center_y = SCREEN_HEIGHT // 2,
                                        width    = SCREEN_WIDTH,    height   = SCREEN_HEIGHT,
                                        texture  = self.background )
        self.write_name()

    def setup(self):
        self.player_name = ''

    def on_mouse_press(self, x, y, button, modifiers):
        print("toast... clicking doesn't do anything")

    def on_key_press(self, key, modifiers):
        if key == 65470:
            print("SWITCH TO MAIN MENU")
            next_view = MenuView()
            self.window.show_view(next_view)
        if key == 65471:
            print("LEADER BOARD")
            next_view = LBView()
            next_view.setup()
            self.window.show_view(next_view)
        if key == 65472 or key==65293 or key==65421:
            print("START NEW GAME")
            next_view = GameView()
            next_view.newGame(self.player_name)
            self.window.show_view(next_view)
        if key == 65473:
            print("RELOAD ENTER NAME")
            next_view = PNameView()
            next_view.setup()
            self.window.show_view(next_view)
        # For name input
        if 96 < key < 123:
            self.player_name += str(['a', 'b', 'c', 'd', 'e', 'f', 'g',
                'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
                's', 't', 'u', 'v', 'w', 'x', 'y', 'z'][key-97])
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
  

    def write_name(self):
        """ Draw the mini score board when the player start playing. """
        player_name = f"{self.player_name}"
        arcade.draw_text(player_name, 46, 530, arcade.color.BLACK, 20, width=250, align="center")
        
        # ADAM REVIEW
        #arcade.draw_text("- CURRENT CHALLENGER -", SCREEN_WIDTH/2, SCREEN_HEIGHT*0.94, arcade.color.CADET_GREY,  float(SCREEN_HEIGHT*0.021), align="center", anchor_x="center", anchor_y="center")
        #arcade.draw_text(player_name, SCREEN_WIDTH/2, SCREEN_HEIGHT*0.90, arcade.color.CADET_GREY,  float(SCREEN_HEIGHT*0.02), bold=True, width=340, align="center", anchor_x="center", anchor_y="center")


#===============================================================================


def main():
    """ Create the game window, setup, run
        #TO-DO load leaderboard file and send to game (?)
    """

    # Initialize
    global ALL_SCORES
    ALL_SCORES = [   [0,"Brutus",   0],
                     [1,"TomWDavis",0]  ]
    FULL_SCREEN = False

    # Setup Questions
    askScores = input("Import Scores? (y/null): ")
    if input("Full Screen?   (y/null): ") == 'y': FULL_SCREEN = True

    # Import Old Scoreboard
    if askScores == "y": ALL_SCORES = importScores()
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
