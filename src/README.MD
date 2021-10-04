# Developer Notes


## Key Map per program screens

### Screen: Main Menu
Class: `MenuView`

| Key | Key ID | Function |
| --- | ------ | -------- |
| F1  | 65470  | Reload Main Menu |
| F2  | 65471  | Leaderboard |
| F5  | 65474  | Leaderboard |
| F3  | 65472  | New Player |


### Screen: Leaderboard
Class: `LBView`

| Key | Key ID | Function |
| --- | ------ | -------- |
| F1  | 65470  | Switch to Main Menu Screen|
| F2  | 65471  | Reload Leaderboard |
| F5  | 65474  | Reload Leaderboard |
| F3  | 65472  | Switch to New Player Screen |


### Screen: New Player, Name Entry
Class: `PNameView`

| Key | Key ID | Function |
| --- | ------ | -------- |
| F1  | 65470  | Switch to Main Menu Screen|
| F2  | 65471  | Switch to Leaderboard |
| F3  | 65472  | Reload New Player Screen |
| Enter (alphabet board) | 65293 | Signal, Ready to Play |
| Enter (numpad) | 65421 | Signal, Ready to Play |
| Directional Keys (left,right,up,down) | 65361, 65362, 65363, 65364 | If `READY_TO_PLAY=True` then Launch Game |
| Enter (numpad) | 65421 | If `READY_TO_PLAY=True` then Launch Game |
| Spacebar  | 32 | If `READY_TO_PLAY=True` then Launch Game |


Before `READY_TO_PLAY` signal is sent, may enter player name. Allowed entries..
* all lower case letters
* all numbers
* dash (alphabet pad)
* numpad minus symbol
* period
* backspace (works as expected)

Includes warning for empty name. Warning prompted to terminal, not game view screen.


### Screen: Game
Class: `GameView`

