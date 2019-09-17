# ADAM BUYNAK
# SEPTEMBER 2019


#consider setting up a separate GAME VIEW which has an internal frame which is the game frame

###############################################################################
# Announcements
print("\n\n - BUCKEYE TETRIS - ")
print("  Title: main.py\n Author: Adam Buynak\n       : Developed for & in partnership with OHI/O\n")
print(" ----> PLEASE WAIT FOR ALL DEPENDENCIES TO LOAD")
print(" ----> USER WILL BE PROMPTED WHEN PROGRAM IS READY\n\n")

###############################################################################
# IMPORT ELEMENTS FROM PACKAGES
import arcade
import random
import PIL


#from view_leaderBoard import LeaderBoardView                                    #import Karl's leaderboard view code

# examples
#from otherScript import function
#import pandas as pd                                                             # Import 'pandas' for dataframe creation and handling #shorten call name to 'pd'

###############################################################################
# FUNCTIONS



###############################################################################
#- Global Constants
SCREEN_WIDTH = 342
SCREEN_HEIGHT = 1008
SCREEN_TITLE = "BUCKEYE TETRIS"


# Original Suggested Dimensions Calculator
# SCREEN_WIDTH = (WIDTH + MARGIN) * COLUMN_COUNT + MARGIN
# SCREEN_HEIGHT = (HEIGHT + MARGIN) * ROW_COUNT + MARGIN
# SCREEN_TITLE = "Tetris"

# Set how many rows and columns we will have-------
ROW_COUNT = 20
COLUMN_COUNT = 10

# Each Grid Location's... WIDTH and HEIGHT---------
WIDTH = 25
HEIGHT = 25

# Marings between cells and screen edges-----------
MARGIN = 5

# Stone Colors-------------------------------------
colors = [
          (0,   0,   0  ),
          (255, 0,   0  ),
          (0,   150, 0  ),
          (0,   0,   255),
          (255, 120, 0  ),
          (255, 255, 0  ),
          (180, 0,   255),
          (0,   220, 220)
          ]

# Define the shapes of the single parts--------------
tetris_shapes = [
    [[1, 1, 1],
     [0, 1, 0]],

    [[0, 2, 2],
     [2, 2, 0]],

    [[3, 3, 0],
     [0, 3, 3]],

    [[4, 0, 0],
     [4, 4, 4]],

    [[0, 0, 5],
     [5, 5, 5]],

    [[6, 6, 6, 6]],

    [[7, 7],
     [7, 7]]
]

###############################################################################
# MASTER BLOCK


##--------------------------------------
#- Welcome & Menu Page
class MenuView(arcade.View):

    def on_show(self):
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        arcade.draw_text("~ BUCKEYE TETRIS ~", SCREEN_WIDTH/2, SCREEN_HEIGHT*3/4,
                        arcade.color.WHITE, font_size=20, anchor_x="center")
        arcade.draw_text("Click to advance", SCREEN_WIDTH/2, SCREEN_HEIGHT*3/4-75,
                        arcade.color.GRAY, font_size=15, anchor_x="center")

    def on_mouse_press(self, x, y, button, modifiers):
        next_view = GameView()
        self.window.show_view(next_view)

##--------------------------------------
#- Leader Board
class LeaderBoardView(arcade.View):
#    def __init__(self):

    def on_show(self):
        arcade.set_background_color(arcade.color.BLUE)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("<<LEADER BOARD>>", SCREEN_WIDTH/2, SCREEN_HEIGHT/2,
                        arcade.color.WHITE, font_size=20, anchor_x="center")
        arcade.draw_text("TO BE COMPLETED", SCREEN_WIDTH/2, SCREEN_HEIGHT/2-75,
                        arcade.color.GRAY, font_size=15, anchor_x="center")

    def on_mouse_press(self, x, y, button, modifiers):
        next_view = MenuView()
        self.window.show_view(next_view)


#################################################################################
#################################################################################


def create_textures():
    """ Create a list of images for sprites based on the global colors. """
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
    """ Main application class. """

    def on_show(self):
        """ Set up the application. """

        arcade.set_background_color(arcade.color.WHITE)

        self.board = None
        self.frame_count = 0
        self.game_over = False
        self.paused = False
        self.board_sprite_list = None

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

    def setup(self):
        self.board = new_board()

        self.board_sprite_list = arcade.SpriteList()
        for row in range(len(self.board)):
            for column in range(len(self.board[0])):
                sprite = arcade.Sprite()
                for texture in texture_list:
                    sprite.append_texture(texture)
                sprite.set_texture(0)
                sprite.center_x = (MARGIN + WIDTH) * column + MARGIN + WIDTH // 2
                sprite.center_y = SCREEN_HEIGHT - (MARGIN + HEIGHT) * row + MARGIN + HEIGHT // 2

                self.board_sprite_list.append(sprite)

        self.new_stone()
        self.update_board()

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
                            break
                    else:
                        break
                self.update_board()
                self.new_stone()

    def rotate_stone(self):
        """ Rotate the stone, check collision. """
        if not self.game_over and not self.paused:
            new_stone = rotate_clockwise(self.stone)
            if not check_collision(self.board, new_stone, (self.stone_x, self.stone_y)):
                self.stone = new_stone

    def update(self, dt):
        """ Update, drop stone if warrented """
        self.frame_count += 1
        if self.frame_count % 10 == 0:
            self.drop()

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

    def on_key_press(self, key, modifiers):
        """
        Handle user key presses
        User goes left, move -1
        User goes right, move 1
        Rotate stone,
        or drop down
        """
        if key == arcade.key.LEFT:
            self.move(-1)
        elif key == arcade.key.RIGHT:
            self.move(1)
        elif key == arcade.key.UP:
            self.rotate_stone()
        elif key == arcade.key.DOWN:
            self.drop()

    def draw_grid(self, grid, offset_x, offset_y):
        """
        Draw the grid. Used to draw the falling stones. The board is drawn
        by the sprite list.
        """
        # Draw the grid
        for row in range(len(grid)):
            for column in range(len(grid[0])):
                # Figure out what color to draw the box
                if grid[row][column]:
                    color = colors[grid[row][column]]
                    # Do the math to figure out where the box is
                    x = (MARGIN + WIDTH) * (column + offset_x) + MARGIN + WIDTH // 2
                    y = SCREEN_HEIGHT - (MARGIN + HEIGHT) * (row + offset_y) + MARGIN + HEIGHT // 2

                    # Draw the box
                    arcade.draw_rectangle_filled(x, y, WIDTH, HEIGHT, color)

    def update_board(self):
        """
        Update the sprite list to reflect the contents of the 2d grid
        """
        for row in range(len(self.board)):
            for column in range(len(self.board[0])):
                v = self.board[row][column]
                i = row * COLUMN_COUNT + column
                self.board_sprite_list[i].set_texture(v)

    def on_draw(self):
        """ Render the screen. """

        # This command has to happen before we start drawing
        arcade.start_render()
        #self.board_sprite_list.draw()#-----------------------------------------------------------++++check
        #self.draw_grid(self.stone, self.stone_x, self.stone_y)


def main():
    """ Create the game window, setup, run """
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

    next_view = MenuView()
    window.show_view(next_view)



    #my_game = GameView(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    #my_game.setup()

    arcade.run()


if __name__ == "__main__":
    main()
