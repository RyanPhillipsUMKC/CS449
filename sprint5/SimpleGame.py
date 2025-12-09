'''
Ryan Phillips 
UMKC CS 449 Sprint 5
SimpleGame.py
Implements Simple Game backend
'''
from AutoGame import *

class SimpleGame(AutoGame):
    # simple game wins on first sos or else turn goes to other player
    def _update_game_state(self, move_function_return_data):
        # draw on board full and no sos made
        if len(move_function_return_data.soses_made) > 0:
            self.game_state = GameStateType.Red_Win if self.turn == PlayerType.Red else GameStateType.Blue_Win
        elif self.are_all_spots_full():
            self.game_state = GameStateType.Draw
        else:
            self.turn = PlayerType.Red if self.turn == PlayerType.Blue else PlayerType.Blue

    def get_game_type(self):
        return GameType.Simple