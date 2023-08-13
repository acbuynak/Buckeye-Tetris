"""
This module contains the back-end of the scoring system for the game.

SCORE SAVE FILE STRUCTURED AS csv...
SCORE NAME LEVEL


"""

import csv
import os
import pathlib


def importScores():
    ALL_SCORES = []
    full_path = os.path.join(pathlib.Path(__file__).parent.resolve(), 'tetris_scores.csv')
    with open(full_path, newline='') as csvfile:
        currentLine = csv.reader(csvfile, delimiter=',')
        i=0
        for row in currentLine:
            ALL_SCORES.append([ int(row[0]), str(row[1]), int(row[2]) ])
            i+=1
    return ALL_SCORES




def saveScores(SCORES):
    with open('tetris_scores.csv', 'w', newline='') as csvfile:
        currentLine = csv.writer(csvfile, delimiter=',')
        i=0
        for row in SCORES:
            currentLine.writerow( [ row[0], row[1], row[2] ] )
