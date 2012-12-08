'''
Implements the textual representation of the playboard.

Also, allows the human player entering a move. Shows the history of recent moves,
and implements textual menu for setting up the game properties.

'''



from globalconstants import WHITE, BLACK, EMPTY, BOARDDIAMETER, AI, HUMAN
from validator import *

class BoardToConsole(object):

    '''
    Console interpretation of the playboard
    Some basis UI items - menu, status messages, options to load, save, replay the game

    '''
    
    def __init__(self):
        return None


    def drawPlayboard(self, board):
        # upper border
        print ''
        print '', '---' * 9

        
        # content of the board
        for i in xrange(BOARDDIAMETER-1, -1, -1):
            for j in xrange(0, BOARDDIAMETER):

                cell_value = board.getPlayer(j, i)
           
                if cell_value == EMPTY:
                    print '|  ',
                elif cell_value == WHITE:
                    print '| 0',
                elif cell_value == BLACK:
                    print '| X',

                # lower border of the board
                if j == 6:
                    print'|', i+1
                    print'|---' * 7,
                    print''

        print u' ', # just to add a free space at the bottom right corner

        for item in 'abcdefg': # print column names of the playboard
            print item, ' ',

    def mainMenu(self):
        # 22 lines
        print '#'*78
        print '\n'*3
        print "\t\t\t Welcome in 'Osetinska dama'!"
        print "\t\t\t Make your selection below:"
        print "\n\t\t\t\t Start game - enter 1"
        print "\t\t\t\t Option 2"
        print "\t\t\t\t Option 3"
        print "\n" *11
        selection = int(raw_input('Your choice:'))
        

        return selection

    def promptForPlayer(self):
        '''
        ASCII menu for player selection
        '''
        selectedTypes = []
        
        for i in xrange(1, 3):
            print '#'*78
            print '\n'*3
            print "\t\t\t Osetinska dama"
            print "\n\tSelect type of player%i:" % i
            print "\t\t(1)Human"
            print "\t\t(2)Computer"
            print "\n" *12
            selection = int(raw_input('Your choice:'))
            if selection not in (1, 2):
                print '#'*78
                print '\n'*3
                print "\t\t\t SORRY, THE ENTERED VALUE IS NOT CORRECT!"
                print "\n\tPress return key to retry."
                print "\n" *14
                raw_input()
                self.promptForPlayer()
            if selection == AI:
                print '#'*78
                print '\n'*3
                print "\t\t\t Select the level of the AI player."
                print "\n\tAllowed values are 1, 2, 3, or 4"
                print "\n" *14
                level = int(raw_input('Your choice:'))
                if level not in (1, 2, 3, 4):
                    print '#'*78
                    print '\n'*3
                    print "\t\t\t SORRY, THE ENTERED VALUE IS NOT CORRECT!"
                    print "\n\tPress return key to retry."
                    print "\n" *14
                    raw_input()
                    self.promptForPlayer()
                
            else:
                selectedTypes.append(selection)
                

            
        
        return selectedTypes
        

    def getMove(self):
        '''
        Gets the desired move coordinates from human player.
        '''

        xcoordinates = ['a','b','c','d','e','f', 'g']

        xcordStart = raw_input('Zadejte X souradnici pocatku tahu (a-f):')
        
        if xcordStart not in xcoordinates:
            print 'Souradnice musi byt pismeno v intervalu <a-f>!\n'
            self.getMove()

        ycordStart = int(raw_input('Zadejte Y souradnici pocatku tahu (1-7):'))

        if ycordStart not in xrange(1, 8):
            print 'Hodnota musi byt v intervalu <1, 7>!\n'
            self.getMove()

        xcordEnd = raw_input('Zadejte X souradnici konce tahu (a-f):')

        if xcordEnd not in xcoordinates:
            print 'Souradnice musi byt pismeno v intervalu <a-f>!\n'
            self.getMove()
        
        ycordEnd = int(raw_input('Zadejte Y souradnici konce tahu (1-7):'))

        if ycordEnd not in xrange(1, 8):
            print 'Hodnota musi byt v intervalu <1, 7>!\n'
            self.getMove()

        xcordStart = xcoordinates.index(xcordStart)
        xcordEnd = xcoordinates.index(xcordEnd)
        ycordStart = ycordStart-1
        ycordEnd = ycordEnd-1
        

        result = [xcordStart, ycordStart, xcordEnd, ycordEnd]

        return result
        
        
        

    def getUserInput(self):
        pass


    def announceGameEnd(self, status):
        '''
        Announcement on the end of the game
        '''
        if status == 0:
            print '\n\nThe game is over - split score! Your skils are obviously the same..\n'
        if status == WHITE:
            print '\n\nWHITE wins the game!\n'
        if status == BLACK:
            print '\n\nBLACK wins the game!\n'
        return
