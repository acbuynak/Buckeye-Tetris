# BlockOHI/O :video_game:
Tetrominoes @ The Ohio State University

---

### DEPENDENCIES  
These programs are necessary to run program.

**Python3**  
Arcade Library requires `Python 3.6` or newer.  
Runs on Windows, Mac OS X, and Linux.

**"Arcade" Library**  
GUI Library and Game Support Structure  
Python library for 2D games.   
Arcade is built on top of Pyglet and OpenGL.  
http://arcade.academy/  


**AntiMicro**  
Gamepad Input Converted to Keystrokes for Teamviewer.  
Required only when using the physical arcade console. Configuration file is provided in `/support` directory for the game console.
https://github.com/AntiMicro/antimicro/releases  

---

### REQUIREMENTS

**Output Screen**  

|Screen           | Pixels (px)|
|-----------------|------------|
|Tower            |342 x 1080  |  
|Game Area        |342 x 1008  |
|Program Display  |1920 x 1080 |
* There is a 72 px buffer on the bottom of the Tower screen  


**Game Speed & System Hardware**  
The structure of the game relies on a small number of sprite tiles (ie the falling blocks). Their location is updated every loop progression of the script and thus puts a greater draw on the system. See some discussion at the below link.  
[Arcade Performance/Moving-Sprites](https://arcade.academy/arcade_vs_pygame_performance.html#moving-sprites)

---

### STRUCTURE THEORY  

| 4 Main views    | Key to Switch View |  
|-----------------|--------------------|
|"MenuView"       |`F1`|
|"LeaderBoardView"|`F2`|
|"NewPlayer"      |`F3`|
|"GameView"       | *Natural progression from* "NewPlayer"|


**Leaderboard/Score Saving Structure**    
1. Game should pull from external txt/dat file for current leaderboard.  
2. Game should save to external txt/dat file for leaderboard progression.  
3. Leaderboard file updated after completion of each game  
4. File must be saved in `src` file and named: `tetris_scores.csv`


