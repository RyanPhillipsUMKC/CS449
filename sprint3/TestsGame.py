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
       self.game = Game(5, 5, PlayerType.Red)
    def tearDown(self):
        self.game = None # allow gc to clean up

    # AC 1.1 Test inits to an empty board
    def test_all_empty(self):
      self.game.reset(5, 5, PlayerType.Red)
      for row in range(self.game.get_board_size_x()):
          for col in range(self.game.get_board_size_y()):
              self.assertEqual(self.game.get_slot_type_for_spot(row, col), BoardSlotType.Empty)

    # AC 1.1 Board dimensions config
    def test_valid_board_sizes_config(self):
        self.game.reset(5, 5, PlayerType.Red)
        self.assertEqual(self.game.get_board_size_x(), 5)
        self.assertEqual(self.game.get_board_size_y(), 5)

        self.game.reset(10, 15, PlayerType.Red)
        self.assertEqual(self.game.get_board_size_x(), 10)
        self.assertEqual(self.game.get_board_size_y(), 15)

    # AC 1.2 Invalid board dimensions (must be able to make sos on both dims so >= 3)
    def test_invalid_board_size_config(self):
        self.game.reset(5, 1, PlayerType.Red)
        self.assertEqual(self.game.get_board_size_x(), 5)
        self.assertEqual(self.game.get_board_size_y(), 3)

        self.game.reset(2, 4, PlayerType.Red)
        self.assertEqual(self.game.get_board_size_x(), 3)
        self.assertEqual(self.game.get_board_size_y(), 4)

        self.game.reset(1, 1, PlayerType.Red)
        self.assertEqual(self.game.get_board_size_x(), 3)
        self.assertEqual(self.game.get_board_size_y(), 3)
    
    # AC 2.1 Game mode config
    def test_game_mode_configs(self):
        self.assertEqual(self.game.get_game_type(), None)
        self.assertEqual(isinstance(self.game, Game), True)

    # AC Other starting player turn config
    def test_starting_player_turn_configs(self):
          self.game.reset(5, 5, PlayerType.Red)
          self.assertEqual(self.game.get_turn(), PlayerType.Red)

          self.game.reset(5, 5, PlayerType.Blue)
          self.assertEqual(self.game.get_turn(), PlayerType.Blue)

    # AC 3.1 Board dims, game mode, strting player turn, empty board
    def test_full_config(self):
          self.game.reset(10, 15, PlayerType.Red)
          self.assertEqual(self.game.get_board_size_x(), 10)
          self.assertEqual(self.game.get_board_size_y(), 15)
          self.assertEqual(self.game.get_game_type(), None)
          self.assertEqual(self.game.get_turn(), PlayerType.Red)

          for row in range(self.game.get_board_size_x()):
            for col in range(self.game.get_board_size_y()):
                self.assertEqual(self.game.get_slot_type_for_spot(row, col), BoardSlotType.Empty)


# Test if SOS's are made when moves are made
# These applt to AC 5.1, 5.1, 7.1, 7.2 - a simple game is over, and a general game is over
class TestGameSOSMadeConditions(unittest.TestCase):
    def setUp(self):
       self.game = Game(5, 5, PlayerType.Red)
    def tearDown(self):
        self.game = None # allow gc to clean up

    def test_vertical_up_sos_made(self):
        self.game.reset(3, 3, PlayerType.Red)

        self.game.make_move(BoardSlotType.S, 0, 0)
        self.game.make_move(BoardSlotType.O, 1, 0)
        self.game.make_move(BoardSlotType.S, 2, 0)

        self.assertEqual(len(self.game.get_soses_this_turn()), 1)
        self.assertEqual(self.game.get_soses_this_turn()[0], ((2, 0), (1, 0), (0, 0)))

    def test_vertical_down_sos_made(self):
        self.game.reset(3, 3, PlayerType.Red)

        self.game.make_move(BoardSlotType.S, 2, 1)
        self.game.make_move(BoardSlotType.O, 1, 1)
        self.game.make_move(BoardSlotType.S, 0, 1)

        self.assertEqual(len(self.game.get_soses_this_turn()), 1)
        self.assertEqual(self.game.get_soses_this_turn()[0], ((0, 1), (1, 1), (2, 1)))

    def test_horizontal_left_sos_made(self):
        self.game.reset(3, 3, PlayerType.Red)

        self.game.make_move(BoardSlotType.S, 0, 0)
        self.game.make_move(BoardSlotType.O, 0, 1)
        self.game.make_move(BoardSlotType.S, 0, 2)

        self.assertEqual(len(self.game.get_soses_this_turn()), 1)
        self.assertEqual(self.game.get_soses_this_turn()[0], ((0, 2), (0, 1), (0, 0)))
    
    def test_horizontal_right_sos_made(self):
        self.game.reset(3, 3, PlayerType.Red)

        self.game.make_move(BoardSlotType.S, 1, 0)
        self.game.make_move(BoardSlotType.O, 1, 1)
        self.game.make_move(BoardSlotType.S, 1, 2)

        self.assertEqual(len(self.game.get_soses_this_turn()), 1)
        self.assertEqual(self.game.get_soses_this_turn()[0], ((1, 2), (1, 1), (1, 0)))

    def test_diagonal_up_and_left_sos_made(self):
        self.game.reset(3, 3, PlayerType.Red)

        self.game.make_move(BoardSlotType.S, 0, 0)
        self.game.make_move(BoardSlotType.O, 1, 1)
        self.game.make_move(BoardSlotType.S, 2, 2)

        self.assertEqual(len(self.game.get_soses_this_turn()), 1)
        self.assertEqual(self.game.get_soses_this_turn()[0], ((2, 2), (1, 1), (0, 0)))

    def test_diagonal_up_and_right_sos_made(self):
        self.game.reset(3, 3, PlayerType.Red)

        self.game.make_move(BoardSlotType.S, 0, 2)
        self.game.make_move(BoardSlotType.O, 1, 1)
        self.game.make_move(BoardSlotType.S, 2, 0)

        self.assertEqual(len(self.game.get_soses_this_turn()), 1)
        self.assertEqual(self.game.get_soses_this_turn()[0], ((2, 0), (1, 1), (0, 2)))

    def test_diagonal_down_and_right_sos_made(self):
        self.game.reset(3, 3, PlayerType.Red)

        self.game.make_move(BoardSlotType.S, 2, 2)
        self.game.make_move(BoardSlotType.O, 1, 1)
        self.game.make_move(BoardSlotType.S, 0, 0)

        self.assertEqual(len(self.game.get_soses_this_turn()), 1)
        self.assertEqual(self.game.get_soses_this_turn()[0], ((0, 0), (1, 1), (2, 2)))

    def test_diagonal_down_and_left_sos_made(self):
        self.game.reset(3, 3, PlayerType.Red)

        self.game.make_move(BoardSlotType.S, 0, 2)
        self.game.make_move(BoardSlotType.O, 1, 1)
        self.game.make_move(BoardSlotType.S, 2, 0)

        self.assertEqual(len(self.game.get_soses_this_turn()), 1)
        self.assertEqual(self.game.get_soses_this_turn()[0], ((2, 0), (1, 1), (0, 2)))

if __name__ == '__main__':
    unittest.main()