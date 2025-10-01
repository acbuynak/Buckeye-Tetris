"""
This module contains very useful variables for the game.
"""

import os
import pathlib


# Config
asset_dir = os.path.join(pathlib.Path(__file__).parent.resolve(), "assets")

# Asset Lookup Helper
def asset_lookup(file_name: str) -> str:
    """
    Returns fully qualified path to passed directory.
    """

    abs_asset_path = os.path.join(asset_dir, file_name)
    
    if os.path.isfile(abs_asset_path):
        return abs_asset_path
    else:
        raise ValueError("Unable to validate that asset filepath exists.") 


# Image of the base background
BACKGROUNDS = [asset_lookup("bg_gamescreen.png"),
               asset_lookup("bg_mainmenu.png"),
               asset_lookup("bg_leaderboard.png"),
               asset_lookup("bg_askname.png"),
               ]
# LOGO_TITLE = asset_lookup("title_buckeyetetris.png")
#LOGO_HACKOHIO =

# Button Textures
BUTTONS = [ asset_lookup("button_play.png"),
            asset_lookup("button_leaderboard.png"),
            asset_lookup("button_exit.png"),
            asset_lookup("button_menu.png"),
            ]

# Game over text
GAME_OVER = asset_lookup("game_over.png")

# Secret Level Graphic
SECRET_LEVEL_TEXTURE = asset_lookup("secret_level.png")

#pixel multiplier
#pm = 0.0178571429


############-- MISC GLOBAL VARIABLES --##################

# GAME SPEED
# Use this to control how fast the game starts at and increments faster from
# value = update every (n) frames
INITIAL_GAME_SPEED = 10

#- TETRIS BOARD SIZE
ROW_COUNT = 22
COLUMN_COUNT = 10

# WINDOW DIMENSIONS
#SCREEN_WIDTH  = 513
#SCREEN_HEIGHT = 1512
SCREEN_WIDTH  = 342
SCREEN_HEIGHT = 1080
SCREEN_TITLE  = "BLOCK OHI/O"

TOWER_BUFFER = SCREEN_HEIGHT*0.066666666

#- Stone Components
WIDTH  = int(0.0877193 * SCREEN_WIDTH)               # og: 30  brick & cell WIDTH
HEIGHT = WIDTH                                       # og: 30  brick & cell HEIGHT
MARGIN = int(0.0666666 * 0.0877193 * SCREEN_WIDTH)   # og:  2  This sets the margin between each cell

WINDOW_WIDTH = 1920
WINDOW_MARGIN = 790
HIDE_BOTTOM   = HEIGHT+MARGIN - TOWER_BUFFER
SCREEN_MARGIN = (1/2) * (SCREEN_WIDTH - COLUMN_COUNT*( WIDTH+MARGIN ))

# TETRIS BOARD dimensions
#TETRIS_WIDTH = ((WIDTH + MARGIN) * COLUMN_COUNT + MARGIN)
TETRIS_WIDTH = SCREEN_WIDTH * 0.95
TETRIS_HEIGHT = (HEIGHT + MARGIN) * ROW_COUNT + MARGIN


############-- GAME VIEW ITEM PLACEMENT --##################
e_mscb_height = 120
e_mscb_width = 150
e_mscb_xposn  = 877
e_mscb_yposn  = TETRIS_HEIGHT + TOWER_BUFFER + (0.02*SCREEN_HEIGHT) + e_mscb_height/2 + 15

############-- NEXT STONE BOX --##################
next_height = 120
next_width = 158
next_xposn  = 1040
next_yposn  = TETRIS_HEIGHT + TOWER_BUFFER + (0.02*SCREEN_HEIGHT) + e_mscb_height/2 + 15

############-- GAME DIAGNOSTICS BOX --##################
rx_width = WINDOW_WIDTH * 0.3
rx_height = SCREEN_HEIGHT * 0.5
rx_xposn = WINDOW_WIDTH * 0.22
rx_yposn = SCREEN_HEIGHT * 0.5

################################################################################
# Define Tetris colors
colors = [
          (0,   0,   0  ),
          (160, 1, 240),
          (68, 240, 0),
          (240, 9, 0),
          (38, 3, 242),
          (239, 160, 1),
          (79, 240, 241),
          (240, 240, 0),
          (102, 102, 102)
          ]

# Define the shapes of the single parts
tetris_shapes = [
    [[0, 1, 0],
     [1, 1, 1]],

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
