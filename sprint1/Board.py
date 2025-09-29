'''
Ryan Phillips 
UMKC CS 449 Sprint 1
Board.py
'''

from enum import Enum

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
    
class GameBoard(object):
    def __init__(self, game_type: GameType, board_size: int) -> None:
        assert(board_size > 2)
        self.game_type = game_type
        self.size = board_size
        self.state = [
            [BoardSlotType.Empty for  _ in range(board_size)]  
                for _ in range(board_size)
            ]

    def make_move(self, slot_type: BoardSlotType, row: int, col: int) -> str:
        if row >= len(self.state):
            return "Invalid spot on board."
        if col >= len(self.state):
            return "Invalid spot on board."
        if (self.state[row][col] != BoardSlotType.Empty):
            return "Board spot has already been taken."
        
        self.state[row][col] = slot_type
        #self.check_for_sos(slot_type, row, col)

    def check_for_sos(self, slot_type: BoardSlotType, row: int, col: int) -> tuple:
        SOS_indexes = tuple()
        

        '''
        # check all rows for sos
        check_count = 0
        for current_row in range(self.size):
            check_count = 0
            for current_col in range(self.size):
                needs_s = check_count == 0 or check_count == 2
                if needs_s and self.state[current_row][current_col] == BoardSlotType.S:
                    check_count += 1
                elif not needs_s and self.state[current_row][current_col] == BoardSlotType.O:
                    check_count += 1
                else:
                    check_count = 0
                
                # so we have an SOS, we now it was eneded on current_col and went two cols back
                # we also can set check count to 1 because this could be the start of a new sos
                if check_count == 3:
                    current_SOS_tuple = ((current_row, current_col - 2), (current_row, current_col - 1), (current_row, current_col))
                    SOS_indexes += (current_SOS_tuple,)
                    check_count = 1
        '''

        return SOS_indexes
    
    # check on horizontal, vertical, and dignoal axis's for an sos gicen the current game move
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
    g = GameBoard(GameType.General, 8)

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
            #if (len(current_state) > 0):
            #    print(True, end=" , ")
            #else:
            #    print(False, end=", ")
        print("\n", end="")

    print(state)
    # have to divide by 3 because the moves are pre-set 
    # before checking the sos conditioins; in in real game they are checkedon the spot thats why its tripeled here
    print(f" Total SOS's = {int(len(state) / 3)}")