'''
Ryan Phillips 
UMKC CS 449 Sprint 3 Tests
TestsGame.py

Tests for the Game base class
'''
import unittest

from Game import *


# Test if board dims, game mode, and starting player turn can be configured, and initialized properly with empty board
# AC 1.* - 3.*
class TestGameInit(unittest.TestCase):
    def setUp(self):
       self.game = Game(GameType.Simple, 5, 5, PlayerType.Red)
    def tearDown(self):
        self.game = None # allow gc to clean up

    # AC 1.1 Test inits to an empty board
    def test_all_empty(self):
      self.game.reset(GameType.Simple, 5, 5, PlayerType.Red)
      for row in range(self.game.get_board_size_x()):
          for col in range(self.game.get_board_size_y()):
              self.assertEqual(self.game.get_slot_type_for_spot(row, col), BoardSlotType.Empty)

    # AC 1.1 Board dimensions config
    def test_valid_board_sizes_config(self):
        self.game.reset(GameType.Simple, 5, 5, PlayerType.Red)
        self.assertEqual(self.game.get_board_size_x(), 5)
        self.assertEqual(self.game.get_board_size_y(), 5)

        self.game.reset(GameType.Simple, 10, 15, PlayerType.Red)
        self.assertEqual(self.game.get_board_size_x(), 10)
        self.assertEqual(self.game.get_board_size_y(), 15)

    # AC 1.2 Invalid board dimensions (must be able to make sos on both dims so >= 3)
    def test_invalid_board_size_config(self):
        self.game.reset(GameType.Simple, 5, 1, PlayerType.Red)
        self.assertEqual(self.game.get_board_size_x(), 5)
        self.assertEqual(self.game.get_board_size_y(), 3)

        self.game.reset(GameType.Simple, 2, 4, PlayerType.Red)
        self.assertEqual(self.game.get_board_size_x(), 3)
        self.assertEqual(self.game.get_board_size_y(), 4)

        self.game.reset(GameType.Simple, 1, 1, PlayerType.Red)
        self.assertEqual(self.game.get_board_size_x(), 3)
        self.assertEqual(self.game.get_board_size_y(), 3)

    # AC 2.1 Game mode config
    def test_game_mode_configs(self):
        self.game.reset(GameType.Simple, 5, 5, PlayerType.Red)
        self.assertEqual(self.game.get_game_type(), GameType.Simple)

        self.game.reset(GameType.General, 5, 5, PlayerType.Red)
        self.assertEqual(self.game.get_game_type(), GameType.General)

    # AC Other starting player turn config
    def test_starting_player_turn_configs(self):
          self.game.reset(GameType.Simple, 5, 5, PlayerType.Red)
          self.assertEqual(self.game.get_turn(), PlayerType.Red)

          self.game.reset(GameType.General, 5, 5, PlayerType.Blue)
          self.assertEqual(self.game.get_turn(), PlayerType.Blue)

    # AC 3.1 Board dims, game mode, strting player turn, empty board
    def test_full_config(self):
          self.game.reset(GameType.Simple, 10, 15, PlayerType.Red)
          self.assertEqual(self.game.get_board_size_x(), 10)
          self.assertEqual(self.game.get_board_size_y(), 15)
          self.assertEqual(self.game.get_game_type(), GameType.Simple)
          self.assertEqual(self.game.get_turn(), PlayerType.Red)

          for row in range(self.game.get_board_size_x()):
            for col in range(self.game.get_board_size_y()):
                self.assertEqual(self.game.get_slot_type_for_spot(row, col), BoardSlotType.Empty)


# Test if S and O moves can be made in a simple game
# AC 4.1 - 4.*, AC 6.1 - 6.*
class TestGameMoves(unittest.TestCase):
    def setUp(self):
       self.game = Game(GameType.Simple, 5, 5, PlayerType.Red)
    def tearDown(self):
        self.game = None # allow gc to clean up
    
    # AC 4.1 test making and move and swithing turn - simple game
    def test_simple_game_valid_moves(self):
        self.game.reset(GameType.Simple, 10, 15, PlayerType.Red)

        self.game.make_move(BoardSlotType.S, 1, 1)
        self.assertEqual(self.game.get_slot_type_for_spot(1, 1), BoardSlotType.S)
        self.assertEqual(self.game.get_turn(), PlayerType.Blue)

        self.game.make_move(BoardSlotType.O, 1, 2)
        self.assertEqual(self.game.get_slot_type_for_spot(1, 2), BoardSlotType.O)
        self.assertEqual(self.game.get_turn(), PlayerType.Red)

    # AC 4.2 test invalid move - spot already taken - simple game
    def test_simple_game_invalid_move_spot_taken(self):
        self.game.reset(GameType.Simple, 10, 15, PlayerType.Red)

        self.game.make_move(BoardSlotType.S, 1, 1)
        self.assertEqual(self.game.get_slot_type_for_spot(1, 1), BoardSlotType.S)
        self.assertEqual(self.game.get_turn(), PlayerType.Blue)

        # try to move on spot already taken
        self.assertEqual(self.game.make_move(BoardSlotType.O, 1, 1), MovefunctionReturnType.SpotAlreadyTaken)
        self.assertEqual(self.game.get_slot_type_for_spot(1, 1), BoardSlotType.S)
        self.assertEqual(self.game.get_turn(), PlayerType.Blue)

    # AC 4.3 test invalid move - invalid row index - simple game
    def test_simple_game_invalid_move_row(self):
        self.game.reset(GameType.Simple, 10, 15, PlayerType.Red)

        # try to move on invalid row
        self.assertEqual(self.game.make_move(BoardSlotType.O, 20, 1), MovefunctionReturnType.InvalidSpot)
        self.assertEqual(self.game.get_turn(), PlayerType.Red)

    # AC 4.4 test invalid move - invalid column index - simple game
    def test_simple_game_invalid_move_column(self):
        self.game.reset(GameType.Simple, 10, 15, PlayerType.Red)

        # try to move on invalid row
        self.assertEqual(self.game.make_move(BoardSlotType.O, 5, 100), MovefunctionReturnType.InvalidSpot)
        self.assertEqual(self.game.get_turn(), PlayerType.Red)

    # AC 6.1 test making and move and swithing turn - general game
    def test_general_game_valid_moves(self):
        self.game.reset(GameType.General, 10, 15, PlayerType.Red)

        self.game.make_move(BoardSlotType.S, 1, 1)
        self.assertEqual(self.game.get_slot_type_for_spot(1, 1), BoardSlotType.S)
        self.assertEqual(self.game.get_turn(), PlayerType.Blue)

        self.game.make_move(BoardSlotType.O, 1, 2)
        self.assertEqual(self.game.get_slot_type_for_spot(1, 2), BoardSlotType.O)
        self.assertEqual(self.game.get_turn(), PlayerType.Red)

    # AC 6.2 test invalid move - spot already taken - general game
    def test_general_game_invalid_move_spot_taken(self):
        self.game.reset(GameType.General, 10, 15, PlayerType.Red)

        self.game.make_move(BoardSlotType.S, 1, 1)
        self.assertEqual(self.game.get_slot_type_for_spot(1, 1), BoardSlotType.S)
        self.assertEqual(self.game.get_turn(), PlayerType.Blue)

        # try to move on spot already taken
        self.assertEqual(self.game.make_move(BoardSlotType.O, 1, 1), MovefunctionReturnType.SpotAlreadyTaken)
        self.assertEqual(self.game.get_slot_type_for_spot(1, 1), BoardSlotType.S)
        self.assertEqual(self.game.get_turn(), PlayerType.Blue)

    # AC 6.3 test invalid move - invalid row index - general game
    def test_general_game_invalid_move_row(self):
        self.game.reset(GameType.General, 10, 15, PlayerType.Red)

        # try to move on invalid row
        self.assertEqual(self.game.make_move(BoardSlotType.O, 20, 1), MovefunctionReturnType.InvalidSpot)
        self.assertEqual(self.game.get_turn(), PlayerType.Red)

    # AC 6.4 test invalid move - invalid column index - general game
    def test_general_game_invalid_move_column(self):
        self.game.reset(GameType.General, 10, 15, PlayerType.Red)

        # try to move on invalid row
        self.assertEqual(self.game.make_move(BoardSlotType.O, 5, 100), MovefunctionReturnType.InvalidSpot)
        self.assertEqual(self.game.get_turn(), PlayerType.Red)

if __name__ == '__main__':
    unittest.main()