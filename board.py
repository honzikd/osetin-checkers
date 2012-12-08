'''
Playboard implementation

Two dimensional array

Also, holds two stacks of moves - for 'undo' and 'redo'

'''

from globalconstants import *


class Playboard(object):
    '''
    Holds the actual state of the game

    '''
    
    board = []
    playerOnTurn = None
    
    undo = [] # using Python list methods pop() and append(), implemented as a stack
    redo = [] #
    
    def __init__ (self):
        self.board = []
        for i in xrange(0, BOARDDIAMETER):
            self.board.append([EMPTY])
        for item in self.board:
            for i in xrange(0, BOARDDIAMETER-1):
                item.append(EMPTY)

    def copyBoard(self):
        ''' Creates and returns carbon-copy of actual board'''
        cpboard = Playboard()
        for i in xrange(0, BOARDDIAMETER):
            for j in xrange(0, BOARDDIAMETER):
                cpboard.board[i][j] = self.board[i][j]
        return cpboard

    def test(self, x, y):
        ''' Test if given coordinates fits inside the board'''
        if (x >= BOARDDIAMETER or
            x < 0 or
            y >= BOARDDIAMETER or
            y < 0):
            return False
        return True

    def getPlayer(self, x, y):
        ''' Returns value of cell at given position '''
        if not self.test(x, y):
            return 'Trying to obtain player outside the board'
        else:
            return self.board[BOARDDIAMETER - y - 1][x]
        
    def setPlayer(self, x, y, player):
        if not self.test(x, y):
            return 'Trying to set player outside the board'
        else:
            self.board[BOARDDIAMETER - y - 1][x] = player

    def getPlayerOnTurn(self):
        return self.playerOnTurn

    def setPlayerOnTurn(self, player):
        self.playerOnTurn = player
       

    def setInitPosition(self):
        '''Sets the initial position on the gameboard'''
        self.board = [] #empty the board
        self.__init__()
        for i in xrange(BOARDDIAMETER - 1, 3, -1):
            for j in xrange(0, BOARDDIAMETER):
                self.setPlayer(j, i, BLACK)
        for i in xrange(0, 3):
            for j in xrange(0, BOARDDIAMETER):
                self.setPlayer(j, i, WHITE)

    def getCountOfPieces(self, player):
        '''Updates the count of black/white pieces currently present on the board'''
        count = 0
        for i in range(0, BOARDDIAMETER):
            for j in range(0, BOARDDIAMETER):
                p = self.getPlayer(j, i)
                if p == player:
                    count += 1
        return count
        

    def doMove(self, move, inverse=False):
        ''' Performs a move, no matter if it's valid or not.

        A move:

        (LENGTH, startx, starty, playerOld, playerNew, endx, endy, playerOld, playerNew)

        example:

        (12, 0, 0, WHITE, EMPTY, 0, 1, BLACK, EMPTY, 0, 2, EMPTY, WHITE)
        '''

        length = move[0]
        parts = length / 4 # the move is divided to 'parts' groups with 4 members 
        endPosition = []
        for i in xrange(0, parts):
            shift = 0 + 4*i
            x = move[1+shift]
            y = move[2+shift]
            playerOld = move[3+shift]
            playerNew = move[4+shift]
            self.setPlayer(x, y, playerNew)
            endPosition = [x, y]

        return endPosition

    def resetUndo(self):
        self.undo = []

    def saveMoveToUndo(self, move):
        self.undo.append(move)


