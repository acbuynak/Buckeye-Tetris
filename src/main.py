# ADAM BUYNAK
# SEPTEMBER 2019

###############################################################################
# Announcements
print("\n\n - BUCKEYE TETRIS - ")
print("  Title: buckeye-tetris.py\n Author: Adam Buynak\n       : Developed for & in partnership with OHI/O\n")
print(" ----> PLEASE WAIT FOR ALL DEPENDENCIES TO LOAD")
print(" ----> USER WILL BE PROMPTED WHEN PROGRAM IS READY\n\n")

###############################################################################
# IMPORT ELEMENTS FROM PACKAGES
import arcade

# examples
#from otherScript import function
#import pandas as pd                                                             # Import 'pandas' for dataframe creation and handling #shorten call name to 'pd'

###############################################################################
# FUNCTIONS


###############################################################################
# MASTER BLOCK


#- Global Constants
SCREEN_WIDTH = 342
SCREEN_HEIGHT = 1008
SCREEN_TITLE = "BUCKEYE TETRIS"

#- Main Application Class
class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """
        pass

    def on_draw(self):
        """ Render the screen. """

        arcade.start_render()
        # Code to draw the screen goes here


#- Game Structure
def main():
    """ Main method """
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
