'''
Ryan Phillips 
UMKC CS 449 Sprint 4
AutoGame.py
Subclass of game to allow for computer play
'''

from random import randint

from Game import *


class AutoGame(Game):
    def __init__(self, board_size_x, board_size_y, starting_player_turn, red_computer=False, blue_computer=False):
        super().__init__(board_size_x, board_size_y, starting_player_turn)
        self.red_is_computer = red_computer
        self.blue_is_computer = blue_computer

    def is_red_computer(self):
        return self.red_is_computer
    def is_blue_computer(self):
        return self.blue_is_computer
    
    def is_computers_turn(self):
        turn = self.get_turn()
        if (turn == PlayerType.Red and self.is_red_computer()):
            return True
        if (turn == PlayerType.Blue and self.is_blue_computer()):
            return True
        return False
    
    def make_move(self, slot_type, row, col):
        if self.is_computers_turn():
            auto_row, auto_col, auto_slot_type = self.get_auto_move()
            return super().make_move(auto_slot_type, auto_row, auto_col)
        return super().make_move(slot_type, row, col)
  
    def get_auto_move(self):
        empty_spots = tuple()

        selection_with_most_soses = tuple()
        most_soses = -1

        # try to find spot that would make the most soses
        for row in range(self.get_board_size_x()):
            for col in range (self.get_board_size_y()):
                if (self.state[row][col] == BoardSlotType.Empty):
                    empty_spots += ((row, col), )

                    s_move_soses_made = len(self.check_for_sos_from_move(BoardSlotType.S, row, col))
                    if (s_move_soses_made > 0 and s_move_soses_made > most_soses):
                        selection_with_most_soses = (row, col, BoardSlotType.S)
                        most_soses = s_move_soses_made

                    o_move_soses_made = len(self.check_for_sos_from_move(BoardSlotType.O, row, col))
                    if (o_move_soses_made > 0 and o_move_soses_made > most_soses):
                        selection_with_most_soses = (row, col, BoardSlotType.O)
                        most_soses = o_move_soses_made
        
        if most_soses != -1:
            return selection_with_most_soses

        # cant make an sos anywhere so choose random empty spot with S
        row, col = empty_spots[randint(0, len(empty_spots) - 1)]
        return (row, col, BoardSlotType.S if bool(randint(0, 1)) else BoardSlotType.O)