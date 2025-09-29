'''
Ryan Phillips 
UMKC CS 449 Sprint 1
Board.py  This should probablly just be Game.py because it handles win conditions and other stuff besides the board struct
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

class GameBoard(object):
    def __init__(self, game_type: GameType, board_size: int, starting_player_turn: PlayerType) -> None:
        self.reset(game_type, board_size, starting_player_turn)

    def reset(self, game_type: GameType, board_size: int, starting_player_turn: PlayerType) -> None:
        assert(board_size > 2)
        self.game_type = game_type
        self.size = board_size
        self.turn = starting_player_turn
        self.state = [
            [BoardSlotType.Empty for  _ in range(board_size)]  
                for _ in range(board_size)
            ]
        self.soses_by_player = defaultdict(tuple)
        self.game_state = GameStateType.Ongoing

    def make_move(self, slot_type: BoardSlotType, row: int, col: int) -> MovefunctionReturnType:
        if row >= len(self.state):
            return MovefunctionReturnType.InvalidSpot
        if col >= len(self.state):
            return MovefunctionReturnType.InvalidSpot
        if self.state[row][col] != BoardSlotType.Empty:
            return MovefunctionReturnType.SpotAlreadyTaken
        if self.game_state != GameStateType.Ongoing:
            return MovefunctionReturnType.GameIsAlreadyOver
        
        # make move
        self.state[row][col] = slot_type

        # check for sos's and then cache them so ui know wheres to draw
        sos_indexes_from_move = self.check_for_sos_from_move(slot_type, row, col)
        self.soses_by_player[self.turn] += sos_indexes_from_move

        #check for win conditons and upfates turns + game state
        # simple game wins on first sos or else turn goes to other player
        if self.game_type == GameType.Simple:
            if len(sos_indexes_from_move) > 0:
                self.game_state = GameStateType.Red_Win if self.turn == PlayerType.Red else GameStateType.Blue_Win
            else:
                self.turn = PlayerType.Red if self.turn == PlayerType.Blue else PlayerType.Blue
        
        # general game wins on all spots full and winner has most sos's
        # if game still ongoing swicth turns to other player iff no sos was made by current player
        elif self.game_type == GameType.General:
            are_all_spots_full = True
            for row in self.state:
                for col in row:
                    if col == BoardSlotType.Empty:
                        are_all_spots_full = False
                        break

            # check for game over and who won
            if are_all_spots_full:
                num_of_sos_for_red = len(self.soses_by_player[PlayerType.Red])
                num_of_sos_for_blue = len(self.soses_by_player[PlayerType.Blue])
                if num_of_sos_for_blue == num_of_sos_for_red:
                    self.game_state = GameStateType.Draw
                elif num_of_sos_for_blue > num_of_sos_for_red:
                    self.game_state = GameStateType.Red_Win
                else:
                    self.game_state = GameStateType.Blue_Win
            else: # game still going
                # in general game player turn only swaps if there was no sos made
                if len(sos_indexes_from_move) == 0:
                    self.turn = PlayerType.Red if self.turn == PlayerType.Blue else PlayerType.Blue
                    

        return MovefunctionReturnType.ValidMove

    # check on horizontal, vertical, and dignoal axis's for an sos gicen the current game move
    # this returns a tuple of tuples of all the indexes invloved in the sos's made from the move
    # e.g. (((0,0), (0,1), (0,2)), ...)
    def check_for_sos_from_move(self, slot_type: BoardSlotType, row: int, col: int) -> tuple:
        SOS_indexes = tuple()

        # check for sos from a O move
        if slot_type == BoardSlotType.O:
            # check for horizontal sos from an O move
            # if O we know it cant be a horizontal win if in the first or last col
            if (not ((col == 0) or (col == (self.size - 1)))):
                # O has S to the left and right
                if (self.state[row][col - 1] == BoardSlotType.S and self.state[row][col + 1] == BoardSlotType.S):
                    SOS_indexes += (((row, col - 1), (row, col), (row, col + 1)),)
            
            # check for vertical sos from an O move
            # if O we know it cant be a vertical sos if in the first or last row
            if (not ((row == 0) or (row == (self.size - 1)))):
                # O has S to the left and right
                if (self.state[row - 1][col] == BoardSlotType.S and self.state[row + 1][col] == BoardSlotType.S):
                    SOS_indexes += (((row - 1, col), (row, col), (row + 1, col)),)

            # check for diagnoal sos from O move
            # if O we know it cant be a diagnol sos if in the first or last row or in the first or last col
            if (not ((col == 0) or (col == (self.size - 1)))) and (not ((row == 0) or (row == (self.size - 1)))):
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
            if (col <= self.size - 3) and self.state[row][col + 1] == BoardSlotType.O and self.state[row][col + 2] == BoardSlotType.S:
                SOS_indexes += (((row, col), (row, col + 1), (row, col + 2)),)

            # check for vertical sos from an S Move
            # check down two slots of us
            if (row >= 2) and self.state[row - 1][col] == BoardSlotType.O and self.state[row - 2][col] == BoardSlotType.S:
                SOS_indexes += (((row, col), (row - 1, col), (row - 2, col)),)
            # check up two slots of us
            if (row <= self.size - 3) and self.state[row + 1][col] == BoardSlotType.O and self.state[row + 2][col] == BoardSlotType.S:
                SOS_indexes += (((row, col), (row + 1, col), (row + 2, col)),)

            # check for diagnol sos from an S Move
            # check up and left two slots of us
            if (row >= 2) and (col >= 2) and self.state[row - 1][col - 1] == BoardSlotType.O and self.state[row - 2][col - 2] == BoardSlotType.S:
                SOS_indexes += (((row, col), (row - 1, col - 1), (row - 2, col - 2)),)
            # check up and right two slots of us
            if (row >= 2) and (col <= self.size - 3) and self.state[row - 1][col + 1] == BoardSlotType.O and self.state[row - 2][col + 2] == BoardSlotType.S:
                SOS_indexes += (((row, col), (row - 1, col + 1), (row - 2, col + 2)),)
            # check down and left two slots of us
            if (row <= self.size - 3) and (col >= 2) and self.state[row + 1][col - 1] == BoardSlotType.O and self.state[row + 2][col - 2] == BoardSlotType.S:
                SOS_indexes += (((row, col), (row - 1, col + 1), (row - 2, col + 2)),)
            # check down and right two slots of us
            if (row <= self.size - 3) and (col <= self.size - 3) and self.state[row + 1][col + 1] == BoardSlotType.O and self.state[row + 2][col + 2] == BoardSlotType.S:
                SOS_indexes += (((row, col), (row + 1, col + 1), (row + 2, col + 2)),)
            
        return SOS_indexes


if __name__ == "__main__":
    g = GameBoard(GameType.Simple, 8, PlayerType.Blue)
    
    g.make_move(BoardSlotType.S, 1, 1)
    g.make_move(BoardSlotType.O, 1, 2)
    g.make_move(BoardSlotType.S, 1, 3)
    g.make_move(BoardSlotType.O, 1, 4)
    g.make_move(BoardSlotType.S, 1, 5)

    g.make_move(BoardSlotType.S, 2, 1)
    g.make_move(BoardSlotType.O, 2, 2)
    g.make_move(BoardSlotType.S, 2, 3)

    g.make_move(BoardSlotType.S, 4, 3)
    g.make_move(BoardSlotType.O, 4, 4)
    g.make_move(BoardSlotType.S, 4, 5)

    g.make_move(BoardSlotType.S, 0, 4)
    g.make_move(BoardSlotType.S, 2, 4)

    g.make_move(BoardSlotType.S, 7, 7)
    g.make_move(BoardSlotType.O, 6, 7)
    g.make_move(BoardSlotType.S, 5, 7)

    g.make_move(BoardSlotType.S, 0, 7)
    g.make_move(BoardSlotType.O, 1, 6)
    g.make_move(BoardSlotType.S, 2, 5)

    g.make_move(BoardSlotType.S, 0, 7)
    g.make_move(BoardSlotType.O, 1, 6)
    g.make_move(BoardSlotType.S, 2, 5)
    
    g.make_move(BoardSlotType.S, 7, 7)
    g.make_move(BoardSlotType.O, 6, 6)
    g.make_move(BoardSlotType.S, 5, 5)

    g.make_move(BoardSlotType.S, 7, 0)
    g.make_move(BoardSlotType.O, 6, 1)
    g.make_move(BoardSlotType.S, 5, 2)

    g.make_move(BoardSlotType.O, 7, 6)
    g.make_move(BoardSlotType.S, 7, 5)

    for x in g.state:
        for y in x:
            if (y == BoardSlotType.S):
                print("S    ", end=", ")
            elif y == BoardSlotType.O:
                print("O    ", end=", ")
            else:
                print("Empty", end=", ")
        print("\n", end="")

    print()

    state = tuple()
    for x in range(g.size):
        for y in range(g.size):
            current_state = g.check_for_sos_from_move(g.state[x][y], x, y)
            state += current_state
            print(len(current_state), end=", ")
        print("\n", end="")

    print(state)
    # have to divide by 3 because the moves are pre-set 
    # before checking the sos conditioins; in in real game they are checkedon the spot thats why its tripeled here
    print(f" Total SOS's = {int(len(state) / 3)}")

    print(f"Game State = {g.game_state}")
    print(f"Number of Red SOS's = {g.soses_by_player[PlayerType.Red]}")
    print(f"Number of Blue SOS's = {g.soses_by_player[PlayerType.Blue]}")