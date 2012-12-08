from board import *
from UIconsole import BoardToConsole
from think import Thinker
from validator import *

play = Playboard()
brain = Thinker()
btc = BoardToConsole()
val = Validator()
obs = Observer()


#play.setPlayer(0, 5, WHITE)
#play.setPlayer(1, 3, BLACK)
#play.setPlayer(1, 1, BLACK)


obs.gameLoop(play, brain, val, btc)
