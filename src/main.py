"""
BUCKEYE TETRIS
Coded by:  Adam Buynak in collaboration w/ The Ohio State University's OHI/O
Distributed under the MIT LICENSE.
"""
################################################################################

import arcade
import random
import PIL


from game_state import State
from game_variables import *

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

    def newGame(self): #width, height, title removed
        """ Initial Setup """
        print("GameView Opened!")

        #self.background = None
        self.board = None
        self.frame_count = 0                #reset game frame counter
        self.game_over = False              #reset game end state
        self.paused = False
        self.board_sprite_list = None

        #self.state = State.PLAYING


        # initial score
        self.score = None
        self.level = None
        self.GAME_SPEED = None

        # The texture for the start and game over screens.
        self.menus = {'exit':        arcade.load_texture(EXIT_BUTTON),
                      'gameover':    arcade.load_texture(GAME_OVER),
                      'play':        arcade.load_texture(PLAY_BUTTON),
                      'leaderboard': arcade.load_texture(LEADERBOARD_BUTTON),
                      'menu':        arcade.load_texture(MENU_BUTTON)}
    def on_show(self):
        #arcade.set_background_color(arcade.color.BLACK)
        #self.background = arcade.load_texture(BACKGROUNDS[0])                   #Set Background
        texture = arcade.load_texture(BACKGROUNDS[0])
        arcade.draw_texture_rectangle(self.width // 2, self.height // 2, self.texture.width, self.texture.height, self.texture, 0)

        # Hide mouse cursor
        self.window.set_mouse_visible(False)

    def setup(self):

        #Initialize Scoring System & Game Components
        self.board = new_board()
        self.score = 0
        self.level = 0
        self.GAME_SPEED = INITIAL_GAME_SPEED

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

#    def draw_background(self):
#        """        Draws the background.        """
#        arcade.draw_texture_rectangle(self.width // 2, self.height // 2, self.background.width, self.background.height,
#                                      self.background, 0)

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
                            print(self.score)
                            break
                    else:
                        break
                self.update_board()
                self.new_stone()
				##-------------------- switch to next stone command for Future stone feature

    def rotate_stone(self):
        """ Rotate the stone, check collision. """
        if not self.game_over and not self.paused:
            new_stone = rotate_clockwise(self.stone)
            if not check_collision(self.board, new_stone, (self.stone_x, self.stone_y)):
                self.stone = new_stone

    def update(self, dt):
        """ Update, drop stone if warrented
		------------------------------------ FRAME RATE CONTROLLING """
        self.frame_count += 1
        if self.frame_count % self.GAME_SPEED == 0:
            self.drop()

        self.build_mscb()

        #GAME SPEED UPDATER-----------------------------------------------------SPEED CONTROLLER
        if self.score >= ((self.level+1) * 2):
            self.level += 1
            if self.GAME_SPEED > 0:
                self.GAME_SPEED -= 1

##      #TEMPORARY HOME UNTIL SCREEN SWITCHING SETUP
        arcade.draw_texture_rectangle(150, 700, 100, 100, arcade.load_texture(LOGO_TITLE), 0)              #FIXME FIXME FIXME FIXME FIXME FIXME

    def build_mscb(self):
        """ Draw the mini score board when the player start playing. """
        score_text = f"{self.score}"
        level_text = f"{self.level}"
        arcade.draw_rectangle_outline(e_mscb_xposn, e_mscb_yposn, e_mscb_width, e_mscb_height, [0,153,153], 2)
        arcade.draw_text("SCORE", e_mscb_xposn-138, e_mscb_yposn-20, arcade.color.BLACK, 12, width=170, align="left", anchor_x="center", anchor_y="center")
        arcade.draw_text(score_text, e_mscb_xposn-90, e_mscb_yposn, arcade.color.BLACK, 30, width=100, align="left", anchor_x="center", anchor_y="center")

        arcade.draw_text("LEVEL", e_mscb_xposn+138, e_mscb_yposn-20, arcade.color.BLACK, 12, width=170, align="right", anchor_x="center", anchor_y="center")
        arcade.draw_text(level_text, e_mscb_xposn+90, e_mscb_yposn, arcade.color.BLACK, 30, width=100, align="right", anchor_x="center", anchor_y="center")


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

#        self.draw_background()
        self.board_sprite_list.draw()
        self.draw_grid(self.stone, self.stone_x, self.stone_y)

        ## MASTER GAME STATE SWITCHER ##----------------------------------------fixme fixme
        if self.state == State.MAIN_MENU:
            # Show the main menu

            texture = arcade.load_texture(BACKGROUNDS[0])
            arcade.draw_texture_rectangle(self.width // 2, self.height // 2, self.texture.width, self.texture.height, self.texture, 0)

            # FIXME FIXME: ADD BUTTONS TO FRONT MENU

            #texture = self.menus['start']
            #arcade.draw_texture_rectangle(self.width//2, self.height//2 + 50, texture.width, texture.height, texture, 0)

        elif self.state == State.PLAYING:
            self.build_mscb()
            #x = 'fixme'






        elif self.state == State.GAME_OVER:                                     #FIXME FIXME
            # Draw the game over menu if the player lost + draw the score board.
            texture = self.menus['gameover']
            #arcade.draw_texture_rectangle(self.width//2, self.height//2 + 50, texture.width, texture.height, texture, 0)
            #texture = self.menus['play']
            #arcade.draw_texture_rectangle(self.width//2, self.height//2 - 100, texture.width, texture.height, texture, 0)

class MenuView(arcade.View):

    def on_show(self):
        # Set Background. Required. Do not delete def!
        arcade.set_background_color(arcade.color.GREEN)

    def on_draw(self):
        arcade.start_render()

        # BACKGROUND
        self.background = arcade.load_texture(BACKGROUNDS[1])
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, self.background.width-180, self.background.height-555, self.background, 0)

        # TEXT
        arcade.draw_text("[S] BEGIN GAME", SCREEN_WIDTH/2, SCREEN_HEIGHT/2,
                         arcade.color.CADET_GREY, font_size=15, font_name='arial',
                         align="center", anchor_x="center", anchor_y="center")
        arcade.draw_text("[L] LEADER BOARD", SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 30,
                         arcade.color.CADET_GREY, font_size=15, font_name='arial',
                         align="center", anchor_x="center", anchor_y="center")

        # BUTTONS
        ############# ADD STUFF HERE ###############
        ############# ADD STUFF HERE ###############


    def on_mouse_press(self, x, y, button, modifiers):
        print("toast... clicking doesn't do anything")

    def on_key_press(self, key, modifiers):
        if key == 115: # S key
            next_view = GameView()
            next_view.newGame()
            next_view.setup()
            self.window.show_view(next_view)
        if key == 108: # L key
            print("CALL TO SWITCH TO LEADER_BOARD VIEW")
            #next_view = LBView()
            #next_view.setup()
            #self.window.show_view(next_view)


def main():
    """ Create the game window, setup, run
        #TO-DO load leaderboard file and send to game (?)
    """
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.total_score = 0
    menu_view = MenuView()   #start game in MenuView()
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()
