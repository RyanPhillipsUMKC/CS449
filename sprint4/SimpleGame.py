'''
Ryan Phillips 
UMKC CS 449 Sprint 4
SimpleGame.py
Implements Simple Game backend
'''
from Game import *

class SimpleGame(Game):
    # simple game wins on first sos or else turn goes to other player
    def _update_game_state(self):
        # draw on board full and no sos made
        if len(self.soses_this_turn) > 0:
            self.game_state = GameStateType.Red_Win if self.turn == PlayerType.Red else GameStateType.Blue_Win
        elif self.are_all_spots_full():
            self.game_state = GameStateType.Draw
        else:
            self.turn = PlayerType.Red if self.turn == PlayerType.Blue else PlayerType.Blue

    def get_game_type(self):
        return GameType.Simple