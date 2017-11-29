
# coding: utf-8

# In[7]:

import traceback
import random
import math
import copy

boost = 5
#depminimax = 5
n = {"Tree": 7, "Animal": 3, "Native": 2, "Poacher": 2, "Blank": 22, "Tot": 14, "Row": 6, "Turn": 20, "depMiniMax": 3}
idx = {"Tree": 1, "Animal": 2, "Native": 3, "Poacher": 4, "Blank": 0}
idxrev = { 1:"Tree", 2:"Animal", 3:"Native", 4:"Poacher", 0:"Blank"}
health = {"Tree": 30, "Animal": 45, "Native": 50, "Poacher": 100, "Blank": 0}
hit = {"Animal": {"Native": 25, "Poacher": 50}, "Native": {"Poacher": 10, "Tree": 30, "Animal": 50}, "Poacher": {"Native": 5, "Tree": 10, "Animal": 15}}
blank = {"idx": 0, "health": 0}
safelevel = 200

# In[8]:
def printBoard (board):
    for row in board[0]:
        print "%r, %r" % ([x["idx"] for x in row], [x["health"] for x in row])
    m = tothealth(board[0])
    print ("\nCurrent Health: %d\n\n" %m)

def getNeighbor(board, i, j):
    cell=[]
    new_cell=[]
    cell.extend(([i-1,j], [i+1,j], [i,j-1], [i,j+1]))
    if(i%2==1):
        cell.extend(([i-1,j+1],[i+1,j+1]))
    else:
        cell.extend(([i-1,j-1],[i+1,j-1]))
    for x in range(len(cell)):
        if(cell[x][0]>=0 and cell[x][0] < len(board) and cell[x][1]>=0 and cell[x][1] < len(board[0])):
            new_cell.append(cell[x])
    return new_cell


# In[9]:


def getReach2Cells(board, i, j):
    temp1 = getNeighbor(board,i,j)
    temp2=[]
    for each_elem in temp1:
        temp = getNeighbor(board,each_elem[0], each_elem[1])
        for e in temp:
            temp2.append(e)
    cells=[]
    temp1.append([i,j])
    for each in temp2:
        if ((each not in cells) and (each not in temp1)):
            cells.append(each)
    temp1.remove([i,j])
    for each in temp1:
        cells.append(each)
    for x in range(len(cells)):
        if cells[x] in temp1:
            cells[x].append(1)
        else:
            cells[x].append(2)
    return cells

def tothealth(board):
    hlth = 0
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j]["idx"] != idx["Poacher"]:
                hlth += board[i][j]["health"]
            else:
                hlth += (5 * (100 - board[i][j]["health"]))
    return hlth


def evaluate(board, isplayer):
    try:
        hlth = tothealth(board)
        if(isplayer):
            #print "Native's turn"
            score = 0
            for i in range(len(board)):
                for j in range(len(board[0])):
                    if(board[i][j]["idx"] == 3): #native identified
                        #print "Cell %d, %d" % (i, j)
                        cells = getReach2Cells(board, i, j)
                        profit = [0]
                        for cell in cells:
                            if(board[cell[0]][cell[1]]["idx"] == idx["Tree"] and cell[2] == 1): #tree at level 1
                                score += boost
                                #print "Score boost due to tree at %d, %d" % (cell[0], cell[1])
                            elif(board[cell[0]][cell[1]]["idx"] == idx["Poacher"]): #poacher at any level
                                score -= hit["Poacher"]["Native"]
                                #print "Score decreased by %d due to poacher at %d, %d" % (hit["Poacher"]["Native"], cell[0], cell[1])
                                temp = board[cell[0]][cell[1]]["health"]/hit["Native"]["Poacher"] #strikes remaining
                                profit.append(health["Poacher"]/temp)
                                #print "Score might be increased by %d due to poacher there" % (health["Poacher"]/temp)
                            elif(board[cell[0]][cell[1]]["idx"]== idx["Animal"] and cell[2]==1): #animal at level 1
                                score -= hit["Animal"]["Native"]
                                #print "cell = %r" % cell
                                #print "Score might be decreased by %d due to animal at %d, %d" % (hit["Animal"]["Native"], cell[0], cell[1])
                        temp = max(profit)
                        #print "Max profit = %d" % temp
                        score += (temp + hlth)
                        #print "Score = %d" % score

        else:
            #print "Poacher's turn"
            score = 0
            for i in range(len(board)):
                for j in range(len(board[0])):
                    if board[i][j]["idx"] == idx["Poacher"]:
                        cells = getReach2Cells(board, i, j)
                        profit=[0]
                        for cell in cells:
                            if(board[cell[0]][cell[1]]["idx"]== idx["Tree"] and cell[2]==1): #tree at level 1
                                temp = board[cell[0]][cell[1]]["health"]/hit["Poacher"]["Tree"] #strikes remaining
                                profit.append(100 * health["Tree"]/temp)
                                #print "Score might be increased by %d due to attack on plant at %d, %d" % (health["Tree"]/temp, cell[0], cell[1])
                            elif(board[cell[0]][cell[1]]["idx"]== 2 and cell[2]==2): #animal at level 2
                                temp = board[cell[0]][cell[1]]["health"]/hit["Poacher"]["Animal"] #strikes remaining
                                profit.append(100 * health["Animal"]/temp)
                                #print "Score might be increased by %d due to attack on animal at %d, %d" % (health["Animal"]/temp, cell[0], cell[1])
                            elif(board[cell[0]][cell[1]]["idx"]== 2 and cell[2]==1): #animal at level 1
                                score -= hit["Animal"]["Poacher"]
                                #print "Score decreased by %d due to animal at %d, %d" % (hit["Animal"]["Poacher"], cell[0], cell[1])
                            elif(board[cell[0]][cell[1]]["idx"]== 3): #native at any level
                                score -= hit["Native"]["Poacher"]
                                #print "Score decreased by %d due to native at %d, %d" % (hit["Native"]["Poacher"], cell[0], cell[1])
                                temp = board[cell[0]][cell[1]]["health"]/hit["Poacher"]["Native"] #strikes remaining
                                profit.append(100 * health["Native"]/temp)
                                #print "Score might be increased by %d due to native there" % (health["Native"]/temp)
                        temp = max(profit)
                        #print "Max profit = %d" % temp
                        score += temp
                        score -= hlth
                        #print "Score = %d" % score

    except Exception as e:
        print e
        traceback.print_exc()
        print type(board[cell[0]][cell[1]]), board[cell[0]][cell[1]]
        print type(board[cell[0]][cell[1]]["health"]), board[cell[0]][cell[1]]["health"]
        exit()

    return(score)

# In[11]:


def checkMove(oldBoard, idxUser, startPos, finishPos, plantTree = 0):
    try:

        deg = copy.deepcopy(finishPos)
        #print "Deg is %r" % deg
        board = copy.deepcopy(oldBoard)
        neighbors = getReach2Cells(board[0], startPos[0], startPos[1])
        #print "Neighbors are %r" % neighbors
        u = copy.deepcopy(finishPos)[0:2]
        #print(board[0][startPos[0]][startPos[1]]["idx"],board[0][finishPos[0]][finishPos[1]]["idx"] , idxUser)
        #print "u is %r" % u
        if (board[0][startPos[0]][startPos[1]]["idx"] == board[0][finishPos[0]][finishPos[1]]["idx"]):
            #print "board index matched"
            #print(board[0][startPos[0]][startPos[1]]["idx"],board[0][finishPos[0]][finishPos[1]]["idx"] , idxUser)
            #if (idxUser == "Native"):
                #print "Hitting one's own kin!"
            return (oldBoard, False)
        if deg in neighbors:
            #print "deg is in neighbors"
            if deg[2] == 1:
                #if (idxUser == "Native"):
                    #print "deg[2] is 1"
                if (board[0][finishPos[0]][finishPos[1]]["idx"] == idx["Blank"]):
                    #print "board pos is blank"
                    board[0][finishPos[0]][finishPos[1]] = copy.deepcopy(board[0][startPos[0]][startPos[1]])
                    board[0][startPos[0]][startPos[1]] = copy.deepcopy(blank)
                    board[idx[idxUser]-2].remove(startPos)
                    board[idx[idxUser]-2].append(u)
                    return (board, True)
                #print("Error case")
                #print(board[0][startPos[0]][startPos[1]]["idx"],board[0][finishPos[0]][finishPos[1]]["idx"] , idxUser)
                board[0][finishPos[0]][finishPos[1]]["health"] -= hit[idxUser][idxrev[board[0][finishPos[0]][finishPos[1]]["idx"]]]
                if (board[0][finishPos[0]][finishPos[1]]["health"] <= 0):
                    #board[0][finishPos[0]][finishPos[1]]["health"] = 0
                    #print "cell ltez"
                    if board[0][u[0]][u[1]]["idx"] == 3 or board[0][u[0]][u[1]]["idx"] == 4:
                        if u in board[1]:
                            board[1].remove(u)
                        if u in board[2]:
                            board[2].remove(u)
                    board[0][finishPos[0]][finishPos[1]] = copy.deepcopy(board[0][startPos[0]][startPos[1]])
                    board[0][startPos[0]][startPos[1]] = copy.deepcopy(blank)
                    #print("u: " , idxUser)
                    #print(board[idx[idxUser]-2])
                    #print(startPos)
                    board[idx[idxUser]-2].remove(startPos)
                    board[idx[idxUser]-2].append(u)

                return (board, True)
            else:
                #print "deg[2] is not 1"
                if (board[0][finishPos[0]][finishPos[1]]["idx"] == idx["Blank"]):
                    #if (idxUser == "Native"):
                        #print ("Hitting far off empty\n")
                    return (oldBoard, False)
                #print "pos is not blank"
                board[0][finishPos[0]][finishPos[1]]["health"] -= hit[idxUser][idxrev[board[0][finishPos[0]][finishPos[1]]["idx"]]]
                #print "idxrev", idxrev[board[0][finishPos[0]][finishPos[1]]["idx"]]
                if (board[0][finishPos[0]][finishPos[1]]["health"] <= 0):
                    board[0][finishPos[0]][finishPos[1]] = copy.deepcopy(blank)
                    if board[0][u[0]][u[1]]["idx"] == 3 or board[0][u[0]][u[1]]["idx"] == 4:
                        if u in board[1]:
                            board[1].remove(u)
                        if u in board[2]:
                            board[2].remove(u)
                return (board, True)
    except Exception as e:
        print e
        traceback.print_exc()
        print "lbool", board[0][startPos[0]][startPos[1]]["idx"]
        print "rbool", board[0][finishPos[0]][finishPos[1]]["idx"]
        print "startpos", startPos
        print "finPos ", finishPos
        print "nohealth", board[0][finishPos[0]][finishPos[1]]
        print "lhs ", board[0][finishPos[0]][finishPos[1]]["health"]
        print "hit of user ", hit[idxUser]
        print "user ", idxUser
        print "banda ", idxrev[board[0][finishPos[0]][finishPos[1]]["idx"]]
        for row in board[0]:
            print [x["idx"] for x in row]
        for row in board[0]:
            print [x["health"] for x in row]
        exit()
    #if (idxUser == "Native"):
        #print "Don't know why"
    return (oldBoard, False)

# In[12]:


def init():
    board = []
    native = []
    poacher = []
    for nRow in range(n["Row"]):
        row = []
        for nCol in range(n["Row"]):
            row.append({"idx": 0, "health": 0})
        board.append(row)
    pos = random.sample(range(36), n["Tot"])
    for iter in pos[:n["Tree"]]:
        board [iter / n["Row"]][iter % n["Row"]]["idx"] = idx["Tree"]
        board [iter / n["Row"]][iter % n["Row"]]["health"] = health["Tree"]
    for iter in pos[n["Tree"]:n["Tree"]+n["Animal"]]:
        board [iter / n["Row"]][iter % n["Row"]]["idx"] = idx["Animal"]
        board [iter / n["Row"]][iter % n["Row"]]["health"] = health["Animal"]
    for iter in pos[n["Tree"]+n["Animal"]:n["Tree"]+n["Animal"]+n["Native"]]:
        board [iter / n["Row"]][iter % n["Row"]]["idx"] = idx["Native"]
        board [iter / n["Row"]][iter % n["Row"]]["health"] = health["Native"]
        native.append([iter / n["Row"], iter % n["Row"]])
    for iter in pos[n["Tree"]+n["Animal"]+n["Native"]:n["Tot"]]:
        board [iter / n["Row"]][iter % n["Row"]]["idx"] = idx["Poacher"]
        board [iter / n["Row"]][iter % n["Row"]]["health"] = health["Poacher"]
        poacher.append([iter / n["Row"], iter % n["Row"]])
    board = [board, native, poacher]
    return board


# In[14]:

def MaxValuePoacher (board, depth):
    #print "MaxValuePoacher"
    #for row in board[0]:
    #    print ([(x["idx"], x["health"]) for x in row])
    #print board[1:3]
    if depth > n["depMiniMax"]:
        return (evaluate(board[0], True), evaluate(board[0], False))
    maxim = float("-inf")
    corrOppScore = maxim
    for h in board[2]:
        #print("tmc1: ", h)
        for move in getReach2Cells (board[0], h[0], h[1]):
            #for row in board[0]:
                #print ([(x["idx"], x["health"]) for x in row])
            #print("Natives: ", board[1])
            #print("Poachers: ", board[2])
            #print("tc1: ", h, h[0], h[1], board[0][h[0]][h[1]]["idx"])
            newBoard, success = checkMove(board, "Poacher", [h[0], h[1]], move)
            if (success):
                #print "Move made %r %r" %( h, move)
                plScore, poScore = MaxValuePlayer (newBoard, depth + 1)
                #print "lala"
                if (poScore > maxim):
                    if depth == 0:
                        nextBoard = copy.deepcopy(newBoard)
                        hc = copy.deepcopy(h)
                        bestmove = copy.deepcopy(move)
                        bestmove.append(hc)
                    maxim = poScore
                    corrOppScore = plScore
    if depth == 0:
        return (nextBoard, bestmove)
    return (maxim, corrOppScore)

def MaxValuePlayer (board, depth):
    #print "MaxValuePlayer"

        #print "%r, %r" % ([x["idx"] for x in row], [x["health"] for x in row])
        #print ([(x["idx"], x["health"]) for x in row])
    #print board[1:3]
    maxim = float("-inf")
    corrOppScore = maxim
    for h in board[1]:
        #print("tmc2: ", h)
        for move in getReach2Cells (board[0], h[0], h[1]):
            #for row in board[0]:
                #print ([(x["idx"], x["health"]) for x in row])
            #print("Natives: ", board[1])
            #print("Poachers: ", board[2])
            #print("tc2: ",h,  h[0], h[1], board[0][h[0]][h[1]]["idx"])
            newBoard, success = checkMove(board, "Native", [h[0], h[1]], move)
            if (success):
                #print "Move made %r %r"%( h, move)
                poScore, plScore = MaxValuePoacher (newBoard, depth + 1)
                #print "mama"
                if (plScore > maxim):
                    maxim = plScore
                    corrOppScore = poScore
    return (maxim, corrOppScore)

def main():
    board = init()
    print " $--> Initial board position\n\n"
    printBoard (board)
    for turn in range(n["Turn"]):
        print "\n @@@ Your move @@@\n"
        startPos = [int(x.strip()) for x in raw_input(" $--> Moving piece : ").split(",")]
        finishPos = [int(x.strip()) for x in raw_input(" $--> Target position : ").split(",")]
        if (board[0][startPos[0]][startPos[1]]["idx"] != 3):
            print ("\n!!! Illegal move ... not your piece!  Please try again\n\n", board[0])
            continue
        print "\n\n"
        r = getReach2Cells(board, startPos[0], startPos[1])
        for u in r:
            if (u[0:2] == finishPos):
                finishPos = copy.deepcopy(u)
                #print finishPos
                break
        #plantTree = int(raw_input())
        #print finishPos
        newBoard, success = checkMove(board, "Native", startPos, finishPos)
        if (not success):
            print ("\n!!! Illegal move ! Please try again\n\n")
            continue
        printBoard(newBoard)
        board = copy.deepcopy(newBoard)
        print "\n\n $--> Computer's move\n\n"
        ret_Board, ret_move = MaxValuePoacher(board, 0)
        printBoard (ret_Board)
        print "\n\n $--> Computer made move :\n\n %r -> [%d, %d]\n" % (ret_move[3], ret_move[0], ret_move[1])
        board = copy.deepcopy(ret_Board)
        if (tothealth(board[0]) < safelevel):
            print "You lose!!!"
            return
    print "You win!!!"

if __name__ == '__main__':
    main()
