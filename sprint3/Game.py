'''
Ryan Phillips 
UMKC CS 449 Sprint 3
Game.py
Implements the game and board backend
'''
from enum import Enum
from collections import defaultdict

# States that a single slot on the game board can be in
class BoardSlotType(Enum):
    Empty = 0
    S = 1
    O = 2

class GameType(Enum):
    Simple = 0
    General = 1

class PlayerType(Enum):
    Red = 1
    Blue = 2

class GameStateType(Enum):
    Ongoing = 1
    Red_Win = 2
    Blue_Win = 3
    Draw = 4

# just use theese so ui can have context depenant reaction to trying to make a move thats invalid
class MovefunctionReturnType(Enum):
    InvalidSpot = 0
    SpotAlreadyTaken = 1
    GameIsAlreadyOver = 2
    ValidMove = 3

class Game(object):
    def __init__(self, board_size_x: int, board_size_y: int, starting_player_turn: PlayerType) -> None:
        self.reset(board_size_x, board_size_y, starting_player_turn)

    def reset(self, board_size_x: int, board_size_y: int, starting_player_turn: PlayerType) -> None:
        # keep board in a valid size (sos can be made in either direction so >= 3)
        self.size_x = board_size_x if board_size_x >= 3 else 3
        self.size_y = board_size_y if board_size_y >= 3 else 3
        self.turn = starting_player_turn
        self.state = [
            [BoardSlotType.Empty for _ in range(board_size_y)]  
                for _ in range(board_size_x)
            ]
        self.soses_this_turn = tuple()
        self.soses_by_player = defaultdict(tuple)
        self.game_state = GameStateType.Ongoing

    def make_move(self, slot_type: BoardSlotType, row: int, col: int) -> MovefunctionReturnType:
        if row >= self.size_x:
            return MovefunctionReturnType.InvalidSpot
        if col >= self.size_y:
            return MovefunctionReturnType.InvalidSpot
        if self.state[row][col] != BoardSlotType.Empty:
            return MovefunctionReturnType.SpotAlreadyTaken
        if self.game_state != GameStateType.Ongoing:
            return MovefunctionReturnType.GameIsAlreadyOver
        
        # make move
        self.state[row][col] = slot_type

        # check for sos's and then cache them so ui know wheres to draw
        sos_indexes_from_move = self.check_for_sos_from_move(slot_type, row, col)
        self.soses_this_turn = sos_indexes_from_move
        self.soses_by_player[self.turn] += sos_indexes_from_move

        # check for win conditons and updates turns + game state
        self._update_game_state()
                    
        return MovefunctionReturnType.ValidMove
    
    # virtual funtions for sub classes to override
    def _update_game_state(self):
        pass
    def get_game_type(self):
        pass
    
    def are_all_spots_full(self):
        for row in self.state:
            for col in row:
                if col == BoardSlotType.Empty:
                    return False
        return True

    # check on horizontal, vertical, and dignoal axis's for an sos gicen the current game move
    # this returns a tuple of tuples of all the indexes invloved in the sos's made from the move
    # e.g. (((0,0), (0,1), (0,2)), ...)
    def check_for_sos_from_move(self, slot_type: BoardSlotType, row: int, col: int) -> tuple:
        SOS_indexes = tuple()

        # check for sos from a O move
        if slot_type == BoardSlotType.O:
            # check for horizontal sos from an O move
            # if O we know it cant be a horizontal win if in the first or last col
            if (not ((col == 0) or (col == (self.size_y - 1)))):
                # O has S to the left and right
                if (self.state[row][col - 1] == BoardSlotType.S and self.state[row][col + 1] == BoardSlotType.S):
                    SOS_indexes += (((row, col - 1), (row, col), (row, col + 1)),)
            
            # check for vertical sos from an O move
            # if O we know it cant be a vertical sos if in the first or last row
            if (not ((row == 0) or (row == (self.size_x - 1)))):
                # O has S to the left and right
                if (self.state[row - 1][col] == BoardSlotType.S and self.state[row + 1][col] == BoardSlotType.S):
                    SOS_indexes += (((row - 1, col), (row, col), (row + 1, col)),)

            # check for diagnoal sos from O move
            # if O we know it cant be a diagnol sos if in the first or last row or in the first or last col
            if (not ((col == 0) or (col == (self.size_y - 1)))) and (not ((row == 0) or (row == (self.size_x - 1)))):
                # O has S to the left, down spot and right, up slot
                if (self.state[row - 1][col - 1] == BoardSlotType.S and self.state[row + 1][col + 1] == BoardSlotType.S):
                    SOS_indexes += (((row - 1, col - 1), (row, col), (row + 1, col + 1)),)
                # O has S to the right, down spot and left, up slot
                if (self.state[row - 1][col + 1] == BoardSlotType.S and self.state[row + 1][col - 1] == BoardSlotType.S):
                    SOS_indexes += (((row - 1, col + 1), (row, col), (row + 1, col - 1)),)

        # check for sos on S moves
        elif slot_type == BoardSlotType.S:
            # check for horizontal sos from an S Move
            # check left two slots of us
            if (col >= 2) and self.state[row][col - 1] == BoardSlotType.O and self.state[row][col - 2] == BoardSlotType.S:
                SOS_indexes += (((row, col), (row, col - 1), (row, col - 2)),)
            # check right two slots of us
            if (col <= self.size_y - 3) and self.state[row][col + 1] == BoardSlotType.O and self.state[row][col + 2] == BoardSlotType.S:
                SOS_indexes += (((row, col), (row, col + 1), (row, col + 2)),)

            # check for vertical sos from an S Move
            # check down two slots of us
            if (row >= 2) and self.state[row - 1][col] == BoardSlotType.O and self.state[row - 2][col] == BoardSlotType.S:
                SOS_indexes += (((row, col), (row - 1, col), (row - 2, col)),)
            # check up two slots of us
            if (row <= self.size_x - 3) and self.state[row + 1][col] == BoardSlotType.O and self.state[row + 2][col] == BoardSlotType.S:
                SOS_indexes += (((row, col), (row + 1, col), (row + 2, col)),)

            # check for diagnol sos from an S Move
            # check up and left two slots of us
            if (row >= 2) and (col >= 2) and self.state[row - 1][col - 1] == BoardSlotType.O and self.state[row - 2][col - 2] == BoardSlotType.S:
                SOS_indexes += (((row, col), (row - 1, col - 1), (row - 2, col - 2)),)
            # check up and right two slots of us
            if (row >= 2) and (col <= self.size_y - 3) and self.state[row - 1][col + 1] == BoardSlotType.O and self.state[row - 2][col + 2] == BoardSlotType.S:
                SOS_indexes += (((row, col), (row - 1, col + 1), (row - 2, col + 2)),)
            # check down and left two slots of us
            if (row <= self.size_x - 3) and (col >= 2) and self.state[row + 1][col - 1] == BoardSlotType.O and self.state[row + 2][col - 2] == BoardSlotType.S:
                SOS_indexes += (((row, col), (row + 1, col - 1), (row + 2, col - 2)),)
            # check down and right two slots of us
            if (row <= self.size_x - 3) and (col <= self.size_y - 3) and self.state[row + 1][col + 1] == BoardSlotType.O and self.state[row + 2][col + 2] == BoardSlotType.S:
                SOS_indexes += (((row, col), (row + 1, col + 1), (row + 2, col + 2)),)
            
        return SOS_indexes
    
    # Getters

    def get_slot_type_for_spot(self, row, col):
        if row >= 0 and row < self.size_x and col >= 0 and col < self.size_y:
            return self.state[row][col]
        else:
            return BoardSlotType.Empty
        
    def get_turn(self):
        return self.turn
    def get_board_size_x(self):
        return self.size_x
    def get_board_size_y(self):
        return self.size_y
    def get_game_state(self):
        return self.game_state
    def get_soses_this_turn(self):
        return self.soses_this_turn
    def get_soses_by_player(self):
        return self.soses_by_player