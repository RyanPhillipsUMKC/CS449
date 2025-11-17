'''
Ryan Phillips 
UMKC CS 449 Sprint 4
GeneralGame.py
Implements General Game backend
'''

from Game import *

class GeneralGame(Game):
    # general game wins on all spots full and winner has most sos's, draw on eaul sos's
    # if game still ongoing swicth turns to other player iff no sos was made by current player
    # check for game over and who won
    def _update_game_state(self):
        if self.are_all_spots_full():
            num_of_sos_for_red = len(self.soses_by_player[PlayerType.Red])
            num_of_sos_for_blue = len(self.soses_by_player[PlayerType.Blue])
            if num_of_sos_for_blue == num_of_sos_for_red:
                self.game_state = GameStateType.Draw
            elif num_of_sos_for_blue > num_of_sos_for_red:
                self.game_state = GameStateType.Blue_Win
            else:
                self.game_state = GameStateType.Red_Win
        else: # game still going
            # in general game player turn only swaps if there was no sos made
            if len(self.soses_this_turn) == 0:
                self.turn = PlayerType.Red if self.turn == PlayerType.Blue else PlayerType.Blue

    def get_game_type(self):
        return GameType.General