# Buckeye ~~Tetris~~ TETROMINOES
Tetris @ The Ohio State University

## TO-DO
Adam = Game Views  
.... = User Pop-Up for Information before playing
.... = User Game over Screen  
.... = File Saving Structure(?)  
.... = Countdown Clock until HACK OHI/O Signups End & Actual Event
.... = Game Play cutoff time out for player(?)  
Kelly= Hard Drop Feature  
.... = Resolve Error Thrown when piece comes to edge of screen

Dan  = User input method and game to screen connection  

All  = Prizes  
.... = Trophys for top places?  

### STRUCTURE THEORY (ACB)  
- 3 Main views.........key to Switch View  
1. "MenuView"  ........F1  
2. "LeaderBoardView"...F2  
3. "GameView"  ........F3  

Initial Boot will create window and load "MenuView".  
....Two Options: "Start Game"    --> "GameView"  
....             "Leader Board"  --> "LeaderBoardView"  

IN GAME VIEW:  
....System waits for user input of any kind.. then begins playing  
....  
....  
....  

### File Saving Structure (ACB)  
1. Game should pull from external txt/dat file for current leaderboard.  
2. Game should save to external txt/dat file for leaderboard progression.  
3. Leaderboard file updated after completion of each game  




### "Arcade" Library
[http://arcade.academy/]  
Python library for 2D games.   
Arcade is built on top of Pyglet and OpenGL.  

> pip install arcade

Longer Official Install Instructions  
> [http://arcade.academy/installation.html#installation-instructions]



### SCREEN REQ's
Tower Screen:     342 x 1080 px  
Game Should be:   342 x 1008  
** there is a 72 px buffer on the bottom of the screen  
** QUESTION: Do we build game such that there is a 72 pixel buffer shown on game, but not on screen? or build to 1008 height?  

### SUB-SECTION WORK
X-BOX CONTROLLER:  
https://www.howtogeek.com/404214/how-to-remap-any-controller-to-keyboard-keys-on-windows-and-macos/




-----------------------------------------------  
### Markdown Cheatsheet
https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet
