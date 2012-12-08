'''
AI for the 'Osetinska dama'

generates all moves for given position
implements the AI by the minimax algorithm
provides the best move to the computer player, and also a hint for the human player
'''

'''
How the positions on playboard are evaluated:
(as viewed from WHITE player)

 ---------------------------
|10 | 5 | 5 | 5 | 5 | 5 |10 | 7
|---|---|---|---|---|---|--- 
| 5 |   |   |   |   |   | 5 | 6
|---|---|---|---|---|---|--- 
| 5 |   |   |   |   |   | 5 | 5
|---|---|---|---|---|---|--- 
| 5 |   |   |   |   |   | 5 | 4
|---|---|---|---|---|---|--- 
| 5 |   |   |   |   |   | 5 | 3
|---|---|---|---|---|---|--- 
| 5 |   |   |   |   |   | 5 | 2
|---|---|---|---|---|---|--- 
|10 | 5 | 5 | 5 | 5 | 5 |10 | 1
|---|---|---|---|---|---|--- 
  a   b   c   d   e   f   g  
'''

from globalconstants import *
from copy import deepcopy
from threading import *
from random import shuffle

class Thinker(object):

    '''
    Implements the AI for the game
    '''

    def __init__(self):
        pass


    def generateMoves(self, board, x, y):

        '''
        Generate all simple moves from given position.
        Returns empty list if no move possible.
        '''

        moves = []
        delta = (0, 1, -1)

        playerCell = board.getPlayer(x, y)

        if playerCell == EMPTY:
            return moves

        for i in delta:
            newX = x + i
            if playerCell == WHITE:
                newY = y + 1
            if playerCell == BLACK:
                newY = y - 1
            nextCell = board.getPlayer(newX, newY)
            if ((playerCell == WHITE and nextCell == EMPTY)
                or (playerCell == BLACK and nextCell == EMPTY)):
                move = [x, y, playerCell, EMPTY, newX, newY, EMPTY, playerCell]
                move.insert(0, len(move)) # add length of the move at the beginning
                moves.append(move)
        shuffle(moves) # add more entropy for the AI player
        return moves
                

    def generateSkips(self, board, x, y):

        'Generates all availabe skips from given position - limited length'

        skips = []
        delta = (0, 2, -2)

        currentCell = board.getPlayer(x, y)

        for i in delta:
            for j in delta:
                newX = x + i
                newY = y + j
                skipX = x + i/2
                skipY = y + j/2
                newCell = board.getPlayer(newX, newY)
                skippedCell = board.getPlayer(skipX, skipY)
                if ((currentCell == WHITE and newCell == EMPTY and skippedCell == BLACK)
                    or
                    (currentCell == BLACK and newCell == EMPTY and skippedCell == WHITE)):
                    skip = [x, y, currentCell, newCell, skipX, skipY, skippedCell, EMPTY, newX, newY, newCell, currentCell]
                    skip.insert(0, len(skip))
                    skips.append(skip)
                
        shuffle(skips) # add more entropy to the skips - AI
        return  skips
    

    def genAllSkips(self, board, x, y):

        skips = self.generateSkips(board, x, y)

        if not skips == None:
            for skip in skips:
                copyBoard = board.copyBoard()
                endPos = copyBoard.doMove(skip)
                endX = endPos[0]
                endY = endPos[1]
                length = skip.pop(0) #remove the lenght from the beginning
                skip.extend(self.genAllSkips(copyBoard, endX, endY))    
        
        return skips

            

    def narrow(self, skip):

        ''' Help function to remove nested lists from a move.

            returns (n-1)level copy of (n)level list.
            Returns empty list if given single-level list.
            Returns argument if len 1 argument given.
            Returns black-hole if argument given is multi-level list,
            with nested list in the middle - like: [1, 2, [8], 4, 5]
        '''
        
        result = []
        copySkip = deepcopy(skip)
        copySkip.reverse()
        
        for item in copySkip:
            if type(item).__name__ == 'list':
                result.append(item)

        length = len(result)
        sliced = copySkip[length:]

        for it in result:
            it.reverse()
            it.extend(sliced)
            it.reverse()

        return result

    

    def narrowSkips(self, skips):

        result = []
        print 'start result', result

        for item in skips:
            re = self.narrow(item)
            print 're inside for', re
            print 'item inside for', item
            if re == []:
                result.append(item)
                print 'result2', result
                print 'skip at the end'
                print item
            else:
                self.narrowSkips(re)

        return result

    def moveGenerator(self, board, x, y):
        '''
        Generates all moves available for given position.
        Returns all skips if a skip exists, returns normal
        move if there's no skip available or returns empty list in case
        the piece cannot perform any valid move.
        '''

        skips = self.generateSkips(board, x, y)
        # revork to return all the available skips, not only the len12 ones

        if skips != []:
            return skips
        else:
            return self.generateMoves(board, x, y)



    def genAvailableMovesOnTurn(self, board):
        '''
        Gets all available moves the player on turn can perform.
        The function is used as a move generator for the minimax.
        '''
        player = board.getPlayerOnTurn()

        moves = []

        for i in xrange(0, BOARDDIAMETER):
            for j in xrange(0, BOARDDIAMETER):
                playerTest = board.getPlayer(i, j)
                if player == playerTest:
                    moves.extend(self.moveGenerator(board, i, j))

        return moves
        
        

    def enumBoard(self, board):
        '''
        Enumerates the given position of a piece on board.
        Returns number that falls into <-MANY, MANY>
        '''

        # Enumeration of the material - count of pieces, value(piece) = 1
            
        countWhite = board.getCountOfPieces(WHITE)
        countBlack = board.getCountOfPieces(BLACK)

        # Enumeration of the position - bonuses for position
        # Position at the edge = +5
        # Position in a corner = +10 (the piece will hit the rule for adding edge bonus twice)
    
        bonusWhite = 0
        bonusBlack = 0
        
        for i in xrange(0, BOARDDIAMETER):
            for j in xrange(0, BOARDDIAMETER):
                player = board.getPlayer(i, j)
                if (i == 0 or i == BOARDDIAMETER-1):
                    if player == WHITE:
                        bonusWhite += EDGE
                    if player == BLACK:
                        bonusBlack += EDGE
                if (j == 0 or j == BOARDDIAMETER-1):
                    if player == WHITE:
                        bonusWhite += EDGE
                    if player == BLACK:
                        bonusBlack += EDGE
                
                
        result = (countWhite + bonusWhite) - (countBlack + bonusBlack)
        
        return result

    

    def isEnd(self, board):

        moves = []

        for i in xrange(0, BOARDDIAMETER):
            for j in xrange(0, BOARDDIAMETER):
                moves.extend(self.moveGenerator(board, i, j))

        if moves == []:
            return True
        else:
            return False
        

    def minimax(self, board, depth = 4):
        if (self.isEnd(board) or depth == 0):
            return self.enumBoard(board)
        else:
            moves = self.genAvailableMovesOnTurn(board)
            enum = -MAX

            for move in moves:
                copyBoard = board.copyBoard()
                copyBoard.doMove(move)
                enum = max(enum, self.minimax(copyBoard, depth-1))

            if enum > MANY:
                enum -= enum

            if enum < -MANY:
                enum += enum

            return enum

    def getBestMove(self, board, depth):

        moves = self.genAvailableMovesOnTurn(board)
        maxEnum = -MAX
        bestMove = []

        for move in moves:
            copyBoard = board.copyBoard()
            copyBoard.doMove(move)
            enum = -self.minimax(copyBoard, depth-1)

            if enum > maxEnum:
                maxEnum = enum
                bestMove = move

        return bestMove
            
                
    

    
