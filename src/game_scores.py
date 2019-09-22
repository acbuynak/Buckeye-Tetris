"""
This module contains the back-end of the scoring system for the game.
"""

import csv

def addScore(player_name, score, level):
    ALL_SCORES.append([score, player_name, level])

def importScores():
    ALL_SCORES = [[0,"Brutus",0]]
    with open('tetris_scores.csv', newline='') as csvfile:
        currentLine = csv.reader(csvfile, delimiter=' ')
        i=0
        for row in currentLine:
            ALL_SCORES.append([ row[0], row[1], row[2] ])
            i+=1
    return ALL_SCORES
    #print(ALL_SCORES[1][1])


#SCORE SAVE FILE STRUCTURED AS csv...
# SCORE NAME LEVEL
