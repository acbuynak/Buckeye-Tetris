# Buckeye ~~Tetris~~ TETROMINOES
Tetris @ The Ohio State University


## DEPENDENCIES
These programs are necessary to run program.

###### AntiMicro
Gamepad Input Converted to Keystrokes for Teamviewer  
https://github.com/AntiMicro/antimicro/releases  

###### "Arcade" Library
GUI Library and Game Support Structure  
[http://arcade.academy/]  
Python library for 2D games.   
Arcade is built on top of Pyglet and OpenGL.  


### STRUCTURE THEORY  
- 3 Main views.........key to Switch View  
1. "MenuView"  ........F1  
2. "LeaderBoardView"...F2  
3. "GameView"  ........F3  


## TO-DO
Adam - Countdown Clock until HACK OHI/O Signups End & Actual Event
Adam - Only increase game level and therefore game speed after a collision
   
Unassigned - Show 'next' piece on top of screen  
Unassigned - Scoring Rules need decided  

Idea - Game Play cutoff time out for player(?)  
Idea - User Game over Screen (?)  
Idea - ReOrder F1,F2,F3,F4 keys (?)  


#### File Saving Structure (ACB)  
1. Game should pull from external txt/dat file for current leaderboard.  
2. Game should save to external txt/dat file for leaderboard progression.  
3. Leaderboard file updated after completion of each game  


### SCREEN REQ's
Tower Screen:     342 x 1080 px  
Game Should be:   342 x 1008  
** there is a 72 px buffer on the bottom of the screen  
** QUESTION: Do we build game such that there is a 72 pixel buffer shown on game, but not on screen? or build to 1008 height?  


-----------------------------------------------  
### Markdown Cheatsheet
https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet
