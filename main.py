import random
nTrees = 7
nAnimals = 3
nNatives = 2
nPoachers= 2
nTot = 14
nRows = 6

idxTree = 1
idxAnimal = 2
idxNative = 3
idxPoacher = 4
idxNull = 0

hlhTree = 30
hlhAnimal = 20
hlhNative = 50
hlhPoacher = 100

def checkMove(board, idxUser, startPos, finishPos):
    if idxUser == idxNative:
        if (board[startPos[0]][startPos[1]] != idxNative):
            return False
        if (board[finishPos[0]][finishPos[1]] == idxNull):
            board[finishPos[0]][finishPos[1]] = idxNative
            board[startPos[0]][startPos[1]] = idxNull
            return True
        if (board[finishPos[0]][finishPos[1]] == idxTree):
            board[finishPos[0]][finishPos[1]] = idxNative
            board[startPos[0]][startPos[1]] = idxNull
            return True
        if (board[finishPos[0]][finishPos[1]] == 2):
            [finishPos[0]][finishPos[1]] =


def init():
    board = []
    for nRow in range(nRows):
        board += [[{"idx": 0, "health": 0}] * nRows]
    pos = random.sample(range(36), nTot)
    for iter in pos[:7]:
        board [iter / nRows][iter % nRows]["idx"] = idxTree
        board [iter / nRows][iter % nRows]["health"] = hlhTree
    for iter in pos[7:10]:
        board [iter / nRows][iter % nRows]["idx"] = idxAnimal
        board [iter / nRows][iter % nRows]["health"] = hlhAnimal
    for iter in pos[10:12]:
        board [iter / nRows][iter % nRows]["idx"] = idxNative
        board [iter / nRows][iter % nRows]["health"] = hlhNative
    for iter in pos[12:14]:
        board [iter / nRows][iter % nRows]["idx"] = idxPoacher
        board [iter / nRows][iter % nRows]["health"] = hlhPoacher
    return board

def main():
    board = init()
    for turn in range(20):
        startPos = [int(x) for strip(x) in raw_input().split(",")]
        finishPos = [int(x) for strip(x) in raw_input().split(",")]
        plantTree = int(raw_input())
        if (not checkMove(board, idxNative, startPos, finishPos, plantTree)):
            print ("Illegal move")


if __name__ == '__main__':
    main()
