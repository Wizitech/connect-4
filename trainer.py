# generate 50 random states
# store them in a file
# use neural network classifier to predict
# make sure at least 20% are positive cases
# look for a way to not approximate



import random
from four import *

file = open("games.txt", "a")

for i in range(180):
    board = initial_state()
    while not terminal(board):
        moves = actions(board)
        move = random.choice(moves)
        board = result(board, move)
    for line in board:
        for val in line:
            file.write(str(int(val)))
        file.write("\n")
file.close()
print("done")


