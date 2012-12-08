'''
Validates move entered by the human player.

Also, implements the rules of the game - that includes control of player, who is
actually on move, giving the right to perform a move to the other player etc.

Builds a list of all available moves for a player and all his pieces currently
present on the board.

'''

from globalconstants import WHITE, BLACK, EMPTY
from think import *

class Validator(object):

    '''
    Implements the rules of the game

    A move:

    (LENGTH, startx, starty, playerOld, playerNew, endx, endy, playerOld, playerNew)

    example:

    (4, 0, 0, WHITE, EMPTY, 1, 1, BLACK, EMPTY, 2, 2, EMPTY, WHITE)


    '''

    def __init__(self):
        return
        

    def setPlayerOnTurn(self, board, player):
        if ((not board.getPlayerOnTurn() == player) and (not self.isEndPosition(board) and player != EMPTY)):
            if self.canMove(board, player):
                board.setPlayerOnTurn(player)
        else:
            return
            

    def getPlayerOnTurn(self, board):
        return board.getPlayerOnTurn()


    def getMovesOfPlayer(self, board, player):
        '''
        Returns all available moves for the player.
        Returns empty list in case the player cannot perform any move.
        '''

        think = Thinker()

        moves = []

        for i in xrange(0, BOARDDIAMETER):
            for j in xrange(0, BOARDDIAMETER):
                playerTest = board.getPlayer(i, j)
                if player == playerTest:
                    moves.extend(think.moveGenerator(board, i, j))

        return moves


    def getMoveFromUI(self, board, ui):
        '''
        Obtains start and end coordinates of the move form the ui.
        '''
        coordinates = ui.getMove()

        if coordinates:
            startX = coordinates[0]
            startY = coordinates[1]
            endX = coordinates[2]
            endY = coordinates[3]

        move = self.validateMove(board, startX, startY, endX, endY)
        return move
                


    def canMove(self, board, player):
        '''
        Returns True if the player can perform a move.
        '''
        if self.getMovesOfPlayer(board, player) != []:
            return True

        return False



    def validateMove(self, board, startX, startY, endX, endY):

        '''
        Based on the given start and end coordinates examines if the move is valid by
        comparing the given move with move generated by the AI.
        If valid coordinates given, returns the move.
        If the coordinates are not valid, returns empty list.
        '''
        think = Thinker()

        availableMoves = think.moveGenerator(board, startX, startY)

        if availableMoves == []:
            return availableMoves

        for item in availableMoves:
            print '###'
            length = len(item)
            testStartX = item[1]
            testStartY = item[2]
            testEndX = item[-4]
            testEndY = item[-3]
            if ((startX == testStartX)
                and (startY == testStartY)
                and (endX == testEndX)
                and (endY == testEndY)):
                return item

        return []

                

    def isEndPosition(self, board):
        '''
        Returns True if the given position is the end position.
        '''

        whiteMoves = self.getMovesOfPlayer(board, WHITE)
        blackMoves = self.getMovesOfPlayer(board, BLACK)

        if whiteMoves == [] and blackMoves == []:
            return True

        return False

    def isWinPosition(self, board, player):
        '''
        Returns True if the player won the game
        '''

        if player == WHITE:
            opponent = BLACK
        if player == BLACK:
            opponent = WHITE

        playerPieces = board.getCountOfPieces(player)
        opponentPieces = board.getCountOfPieces(opponent)

        if opponentPieces == 0:
            return True

        if self.isEndPosition(board):
            if playerPieces > opponentPieces:
                return True
            if playerPieces <= opponentPieces:
                return False

                


    
class Observer(object):

    '''
    Provides the observer - game authority
    Controls the player on move, initializates the game, resets the board
    
    '''

    def __init__(self):
        return




    def isValidHumanMove(self, board, validator, ui):
        '''
        Returns False if entered move is not valid.
        Else, returns True
        '''

        if self.getMoveFromUI == []:
            return False

        else:
            return True
            
        

    def initGame(self, board, ui):
        '''
        Starts the game.
        Initializes the initial position of the pieces on the board.
        '''
        selection = ui.mainMenu()
        return selection
 
    def gameLoop(self, board, thinker, validator, ui):
        '''
        Main game loop
        '''
        selection = ui.mainMenu()

        # prompt user for players and types
        # init players (human-human, human-AI, AI-AI)
        # if player == AI:
        # get the 'level' of the AI player

       # if selection == 1:
            #playerTypes = ui.promptForPlayer()
            #if playerTypes[0] == HUMAN:
             #   player1 = HumanPlayer(WHITE)
            #if playerTypes[0] == AI:
            #    player1 = AIPlayer(WHITE)
           # if playerTypes[1] == HUMAN:
          #      player2 = HumanPlayer(BLACK)
         #   if playerTypes[1] == AI:
        #        player2 = AIPlayer(BLACK)
       #     board.setInitPosition()
    
                
        board.setInitPosition()
        ui.drawPlayboard(board)
    


        player1 = AIPlayer(BLACK, 5)
        player2 = AIPlayer(WHITE, 4)

        validator.setPlayerOnTurn(board, WHITE)


        while 1:

            playerTurns = validator.getPlayerOnTurn(board)

            if playerTurns == WHITE:
                playerOpp = BLACK
            if playerTurns == BLACK:
                playerOpp = WHITE

            if playerTurns == player1.getColour():
                player = player1
            else:
                player = player2
            
            move = player.selectMove(board, validator, thinker, ui)
            board.doMove(move)

            # save move to undo
            board.saveMoveToUndo(move)
            print board.undo
            
            ui.drawPlayboard(board)

            
            # tests of possible end of the game
            if validator.isEndPosition(board):
                if validator.isWinPosition(board, playerTurns):
                    ui.announceGameEnd(playerTurns)
                    return
                if validator.isWinPosition(board, playerOpp):
                    ui.announceGameEnd(playerOpp)
                    return
                else:
                    ui.announceGameEnd(0)
                    return

            # switching the player on turn
            if validator.canMove(board, playerOpp):
                print 'setting the other P as on turn'
                validator.setPlayerOnTurn(board, playerOpp)
            else:
                print 'the other cannot turn, leaving the same player on turn'
                validator.setPlayerOnTurn(board, playerTurns)
            # check for user input (return if end/stop/save is selected)
                
            

    def saveMoveUndo(self, board):
        pass



class Player(object):

    def __init__(self, colour):
        self.colour = colour

    def getColour(self):
        return self.colour

class AIPlayer(Player):

    def __init__(self, colour, level=3):
        Player.__init__(self, colour)
        self.level = level

    def selectMove(self, board, validator, think, ui):
        move = think.getBestMove(board, self.level)
        return move


class HumanPlayer(Player):

    def __init__(self, colour):
        Player.__init__(self, colour)

    def selectMove(self, board, validator, think, ui):
        move = validator.getMoveFromUI(board, ui)
        return move
        

    
        

    

    
