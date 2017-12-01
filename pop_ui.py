from math import sin, cos, pi, sqrt
import pygame
from pop import *

SIDE = 70
THETA = pi / 3.0
h_THETA = pi / 6.0
ROWS = 6
COLUMNS = 6
IMAGE_HEIGHT = int(SIDE * (ROWS + 1 + (ROWS - 1) * cos (THETA)) + 0.5)
IMAGE_WIDTH = int(SIDE * sin (THETA) * (2 * COLUMNS + 1) + 0.5)

colours = {0: (192, 192, 192), 1: (0, 255, 0), 2: (255, 165, 0), 3: (0, 0, 255), 4: (255, 0, 0)}
gameQuit = False

pygame.init()
gameDisplay = pygame.display.set_mode((IMAGE_WIDTH, IMAGE_HEIGHT))
pygame.display.set_caption('Protect Our Planet')
clock = pygame.time.Clock()


def hex_centres():
    '''Provides the centres for the hex cells'''
    for row in range (ROWS):
        for column in range (COLUMNS):
            x = SIDE * ((2 * column + 1 + row % 2) * sin (THETA))
            y = SIDE * ((row + 1) + row * cos (THETA))
            yield x, y

def hex_points(x, y):
    '''Provides the co-ordinates of the vertices of a hex cell given centre'''
    for ver_num in range(6):
        angle =  h_THETA + THETA * ver_num
        yield (x + SIDE * (cos(angle))), (y + SIDE * (sin(angle)))
def pygame_colours():
    while True:
        yield 255, 0, 0 # red
        yield 255, 255, 0 # yellow
        yield 0, 0, 255 # blue
        yield 0, 255, 0 # green
def pygame_hex():
    '''Requires PyGame 1.8 or better to save as PNG'''
    pygame.init()
    screen = pygame.display.set_mode((IMAGE_WIDTH, IMAGE_HEIGHT))
    colours = pygame_colours()
    for x,y in hex_centres():
        print x,y
        pygame.draw.polygon(screen, colours.next(), list(hex_points(x,y)))
        pygame.draw.polygon(screen, (0,0,0), list(hex_points(x,y)), 5)
    pygame.image.save(screen, 'pygame_hexes.png')

def draw_canvas(board):
    index = 0
    myfont = pygame.font.SysFont("monospace", 20)
    #gameDisplay.fill((0, 0, 0))
    for x, y in hex_centres():
        col = colours [board [0][index / ROWS][index % COLUMNS]['idx']]
        pygame.draw.polygon(gameDisplay, col, list(hex_points(x,y)))
        pygame.draw.polygon(gameDisplay, (0,0,0), list(hex_points(x,y)), 5)
        label = myfont.render(str(board [0][index / ROWS][index % COLUMNS]['health']), 1, (255, 255, 255))
        gameDisplay.blit(label, (x-5, y-5))
        index += 1
    pygame.display.update()

def get_cell_no(coord):
    coord = list(coord)
    row = int(coord[1] / (SIDE * (1 + cos(THETA))))
    if row % 2 == 1:
        coord[0] -= SIDE * sin(THETA)
    column = int(coord[0] / (2 * SIDE * sin(THETA)))
    return list((row, column))

def get_user_move(gameQuit):
    stposGiven = False
    flposGiven = False
    startPos = 0
    finishPos = 0
    while not (gameQuit or flposGiven):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameQuit = True
            elif stposGiven and event.type == pygame.MOUSEBUTTONDOWN:
                finishPos = get_cell_no(pygame.mouse.get_pos())
                print "Final Position given"
                flposGiven = True
                return startPos, finishPos
            elif event.type == pygame.MOUSEBUTTONDOWN:
                startPos = get_cell_no(pygame.mouse.get_pos())
                print "Starting Position Given"
                stposGiven = True
    return startPos, finishPos

def uigame():
    turn = 0
    illegal = 0
    board = init()
    draw_canvas(board)
    while turn < n["Turn"]:
        if (illegal > 10):
            print "Too many illegal moves! Aborting game"
            return
        startPos, finishPos = get_user_move(gameQuit)
        r = getReach2Cells(board[0], startPos[0], startPos[1])
        if (board[0][startPos[0]][startPos[1]]["idx"] != 3):
            print ("\nNot your piece! Illegal move! Please try again\n\n")
            illegal += 1
            continue
        for u in r:
            if (u[0:2] == finishPos):
                finishPos = copy.deepcopy(u)
                break
        newBoard, success = checkMove(board, "Native", startPos, finishPos)
        if (not success):
            print ("\nIllegal move for some reason! Please try again\n\n")
            illegal += 1
            continue
        draw_canvas (newBoard)
        board = copy.deepcopy(newBoard)
        print "Natives, Poachers = ", board[1:]
        print "\n\n $--> Computer's move\n\n"
        ret_Board, ret_move = MaxValuePoacher(board, 0)
        draw_canvas (ret_Board)
        print "\n\n $--> Computer made move :\n\n %r -> [%d, %d]\n" % (ret_move[3], ret_move[0], ret_move[1])
        board = copy.deepcopy(ret_Board)
        print "Natives, Poachers = ", board[1:]
        if (tothealth(board[0]) < safelevel):
            print "You lose!!!"
            return
        turn +=1
    print "You win!!!"

    pygame.quit()
    quit()

if __name__ == '__main__':
    #uigame()
    uigame()
