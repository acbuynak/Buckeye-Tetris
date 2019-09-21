"""
This module contains very useful variables for the game.
"""

import os
import arcade

# Image of the base background
BACKGROUNDS = ["assets" + os.sep + "bg_scarletleaf.png","assets" + os.sep + "bg_mainmenu.png", "assets" + os.sep + "bg_leaderboard.png"]
LOGO_TITLE = "assets" + os.sep +  "title_buckeyetetris.png"
#LOGO_HACKOHIO =

# Button Textures
BUTTONS = [ "assets" + os.sep + "button_play.png",
            "assets" + os.sep + "button_leaderboard.png",
            "assets" + os.sep + "button_menu.png",
            "assets" + os.sep + "button_exit.png" ]

# Game over text
GAME_OVER = "assets" + os.sep +  "gameover.png"







############-- MISC GLOBAL VARIABLES --##################

# GAME SPEED
# Use this to control how fast the game starts at and increments faster from
# value = update every (n) frames
INITIAL_GAME_SPEED = 10

#- TETRIS BOARD SIZE
ROW_COUNT = 20
COLUMN_COUNT = 10

#- Stone Components
WIDTH = 30      # brick & cell WIDTH
HEIGHT = 30     # brick & cell HEIGHT
MARGIN = 2   # This sets the margin between each cell

# TETRIS BOARD dimensions
TETRIS_WIDTH = (WIDTH + MARGIN) * COLUMN_COUNT + MARGIN
TETRIS_HEIGHT = (HEIGHT + MARGIN) * ROW_COUNT + MARGIN

# WINDOW DIMENSIONS

SCREEN_WIDTH  = 342
SCREEN_HEIGHT = 1008
SCREEN_TITLE  = "Tetris"

HIDE_BOTTOM   = HEIGHT+MARGIN
SCREEN_MARGIN = (1/2) * (SCREEN_WIDTH - COLUMN_COUNT*( WIDTH+MARGIN ))

############-- GAME VIEW ITEM PLACEMENT --##################

e_mscb_height = 60
e_mscb_width = SCREEN_WIDTH - (2*SCREEN_MARGIN)
e_mscb_xposn  = SCREEN_WIDTH / 2
e_mscb_yposn  = TETRIS_HEIGHT + 20 + e_mscb_height/2

################################################################################

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

# Define the shapes of the single parts
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
