'''
Ryan Phillips 
UMKC CS 449 Sprint 5
Game.py
Implements the game and board backend base class
'''
from enum import Enum
from collections import defaultdict
from time import sleep


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

class MoveFunctionReturnData():
    def __init__(self):
        self.type = MovefunctionReturnType.InvalidSpot
        self.row = -1
        self.col = -1
        self.slot_type = BoardSlotType.Empty
        self.soses_made = tuple()

# Sprint 5 Abstract Cache Writer
# This class is injected into the game by the client so they can chose hwo they cache the game and replay
# e.g. to a file or to a database ... etc
class GameCache(object):
  # virtual function to reset the cache in file database or whatever caching technique
  def reset(self) -> None:
      pass
  # virtual function to write game config headers
  def write_game_config(self, board_size_x: int, board_size_y: int) -> None:
      pass
  # virtual function to get the serialized game config
  def get_game_config(self) -> tuple:
      pass
  # virtual function to write move in a sos game
  def write_move(self, turn: PlayerType, slot_type: BoardSlotType, row: int, col: int) -> None:
      pass
  # virtual function to read the next sos move
  def get_next_move(self) -> tuple:
    pass

# Writer that is filed based
# fileformat =
# board_size_x, board_size_y, game_mode
# turn,slot_type,row,col
# turn,slot_type,row,col
# ... 
# eof
class GameCache_FileBased(object):
    def __init__(self, file_name="game_cache.txt"):
        self._reader = None
        self.file_name= file_name

    def reset(self):
        self._reader = None
        open(self.file_name, 'w').close()

    def write_game_config(self, board_size_x, board_size_y, game_type):
        with open(self.file_name, "a") as f:
            game_mode_str = "S" if game_type == GameType.Simple else "G"
            f.write(f"{board_size_x},{board_size_y},{game_mode_str}\n")

    # read first line headers for game config settings
    def get_game_config(self):
        try:
            with open(self.file_name, "r") as f:
                config_header = f.readline()
                if not config_header:
                    return None
                size_x, size_y, game_mode_str = config_header.strip().split(",")
                game_mode = GameType.Simple if game_mode_str == "S" else GameType.General
                return int(size_x), int(size_y), game_mode
        except FileNotFoundError:
            return None  # no cache yet
  
    def write_move(self, turn, slot_type, row, col):
        turn_str = "R" if turn == PlayerType.Red else "B"
        slot_type_str = "S" if slot_type == BoardSlotType.S else "O"
        with open(self.file_name, "a") as f:
            f.write(f"{turn_str},{slot_type_str},{row},{col}\n")

    # read move by move with a cached file pointer this is what supplys the generator fro replay functionality
    def get_next_move(self):
        # cache an iterator for sequential reading
        if self._reader is None:
            try:
                self._reader = open(self.file_name, "r")
                self._reader.readline() # skip the game config headers
            except FileNotFoundError:
                return None  # no cache yet

        line = self._reader.readline()
        if not line:
            return None  # no more moves

        turn_str, slot_type_str, row_str, col_str = line.strip().split(",")

        turn = PlayerType.Red if turn_str == "R" else PlayerType.Blue
        slot_type = BoardSlotType.S if slot_type_str == "S" else BoardSlotType.O
        row = int(row_str)
        col = int(col_str)

        return turn, slot_type, row, col
  

class Game(object):
    def __init__(self, board_size_x: int, board_size_y: int, starting_player_turn: PlayerType, cache_writer: GameCache, record: bool) -> None:
        self.reset(board_size_x, board_size_y, starting_player_turn, cache_writer, record)

    def reset(self, board_size_x: int, board_size_y: int, starting_player_turn: PlayerType, cache_writer: GameCache, record: bool) -> None:
        self.cache_writer = cache_writer
        self.record = self.cache_writer is not None and record
        if self.record:
            self.cache_writer.reset()
        self.reset_game_state(board_size_x, board_size_y, starting_player_turn)
    
    def reset_game_state(self, board_size_x: int, board_size_y: int, starting_player_turn: PlayerType, should_record_override: bool=True):
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

        if self.cache_writer is not None and self.record and should_record_override:
            self.cache_writer.write_game_config(board_size_x, board_size_y, self.get_game_type())

    # virtual function for overriding (e.g. auto game)
    def make_move(self, slot_type: BoardSlotType, row: int, col: int, should_record_override: bool=True, is_replay=False) -> MoveFunctionReturnData:
        return_data = MoveFunctionReturnData()
        return_data.type = MovefunctionReturnType.ValidMove
        return_data.row = row
        return_data.col = col
        return_data.slot_type = slot_type

        if row >= self.size_x:
            return_data.type = MovefunctionReturnType.InvalidSpot
            return return_data
        if col >= self.size_y:
            return_data.type = MovefunctionReturnType.InvalidSpot
            return return_data
        if self.state[row][col] != BoardSlotType.Empty:
            return_data.type = MovefunctionReturnType.SpotAlreadyTaken
            return return_data
        if self.game_state != GameStateType.Ongoing:
            return_data.type = MovefunctionReturnType.GameIsAlreadyOver
            return return_data
        
        # make move
        self.state[row][col] = slot_type

        # check for sos's and then cache them so ui know wheres to draw
        sos_indexes_from_move = self.check_for_sos_from_move(slot_type, row, col)
        return_data.soses_made = sos_indexes_from_move
        self.soses_by_player[self.turn] += sos_indexes_from_move

        # Sprint 5 write to file
        if self.cache_writer is not None and self.record and should_record_override:
            self.cache_writer.write_move(self.get_turn(), slot_type, row, col)

        # check for win conditons and updates turns + game state
        self._update_game_state(return_data)
                    
        return return_data
    
    def get_game_config_from_cache_writer(self):
        if not self.cache_writer:
            return None
        return self.cache_writer.get_game_config()
    
    # Generator to sequentially yield moves from a cache writer
    def replay_move_from_cache_writer(self):
        if not self.cache_writer:
            return None
        move = self.cache_writer.get_next_move()
        while move:
            yield move
            move = self.cache_writer.get_next_move()

    # is board full?
    def are_all_spots_full(self):
        for row in self.state:
            for col in row:
                if col == BoardSlotType.Empty:
                    return False
        return True
    
    # virtual funtions for sub classes to override
    def _update_game_state(self, move_function_return_data):
        pass
    # virtual function for testing only
    def get_game_type(self):
        pass

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
        # WAITING TO REFACTOR THIS TO BE MORE MODULAR IN SPRINT 5
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
    def get_soses_by_player(self):
        return self.soses_by_player