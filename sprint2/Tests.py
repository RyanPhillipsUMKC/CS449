'''
Ryan Phillips 
UMKC CS 449 Sprint 2 Tests
Language: Python
GUI Framework: TKinter
Tests.py
'''
import unittest

from Board import *

# Test if board is intialized to all empty slots
class TestEmptyBoard(unittest.TestCase):
    def setUp(self):
       self.game = GameBoard(GameType.Simple, 5, 5, PlayerType.Red)
    def tearDown(self):
        self.game = None # allow gc to clean up
    
    def test_all_empty(self):
        for row in range(self.game.get_board_size_x()):
            for col in range(self.game.get_board_size_y()):
                self.assertEqual(self.game.get_slot_type_for_spot(row, col), BoardSlotType.Empty)

# Test if board size can be configured
class TestEmptyBoard(unittest.TestCase):
    def setUp(self):
       self.game = GameBoard(GameType.Simple, 5, 5, PlayerType.Red)
    def tearDown(self):
        self.game = None # allow gc to clean up

    def test_different_board_sizes(self):
        self.assertEqual(self.game.get_board_size_x(), 5)
        self.assertEqual(self.game.get_board_size_y(), 5)
        self.test_all_empty()

        self.game.reset(GameType.Simple, 10, 15, PlayerType.Red)
        self.assertEqual(self.game.get_board_size_x(), 10)
        self.assertEqual(self.game.get_board_size_y(), 15)
        self.test_all_empty()

    def test_all_empty(self):
        for row in range(self.game.get_board_size_x()):
            for col in range(self.game.get_board_size_y()):
                self.assertEqual(self.game.get_slot_type_for_spot(row, col), BoardSlotType.Empty)

# Test if S and O moves can be made in a simple game
class TestSimpleGameMoves(unittest.TestCase):
    def setUp(self):
       self.game = GameBoard(GameType.Simple, 5, 5, PlayerType.Red)
    def tearDown(self):
        self.game = None # allow gc to clean up
    
    def test_single_moves(self):
        self.game.make_move(BoardSlotType.S, 1, 1)
        self.assertEqual(self.game.get_slot_type_for_spot(1, 1), BoardSlotType.S)
        self.assertEqual(self.game.get_turn(), PlayerType.Blue)

        self.game.make_move(BoardSlotType.O, 1, 2)
        self.assertEqual(self.game.get_slot_type_for_spot(1, 2), BoardSlotType.O)
        self.assertEqual(self.game.get_turn(), PlayerType.Red)

        self.assertEqual(self.game.get_slot_type_for_spot(0, 0), BoardSlotType.Empty)

if __name__ == '__main__':
    unittest.main()