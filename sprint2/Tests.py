'''
Ryan Phillips 
UMKC CS 449 Sprint 2 Tests
Tests.py
'''
import unittest

from Game import *
        

# Test if board dims, game mode, and starting player turn can be configured, and initialized properly with empty board
class TestGameInit(unittest.TestCase):
    def setUp(self):
       self.game = GameBoard(GameType.Simple, 5, 5, PlayerType.Red)
    def tearDown(self):
        self.game = None # allow gc to clean up

    # Test inits to an empty board
    def test_all_empty(self):
      self.game.reset(GameType.Simple, 5, 5, PlayerType.Red)
      for row in range(self.game.get_board_size_x()):
          for col in range(self.game.get_board_size_y()):
              self.assertEqual(self.game.get_slot_type_for_spot(row, col), BoardSlotType.Empty)

    # Board dimensions config
    def test_board_sizes_config(self):
        self.game.reset(GameType.Simple, 5, 5, PlayerType.Red)
        self.assertEqual(self.game.get_board_size_x(), 5)
        self.assertEqual(self.game.get_board_size_y(), 5)

        self.game.reset(GameType.Simple, 10, 15, PlayerType.Red)
        self.assertEqual(self.game.get_board_size_x(), 10)
        self.assertEqual(self.game.get_board_size_y(), 15)

    # Game mode config
    def test_game_mode_configs(self):
        self.game.reset(GameType.Simple, 5, 5, PlayerType.Red)
        self.assertEqual(self.game.get_game_type(), GameType.Simple)

        self.game.reset(GameType.General, 5, 5, PlayerType.Red)
        self.assertEqual(self.game.get_game_type(), GameType.General)

    # strting player turn config
    def test_starting_player_turn_configs(self):
          self.game.reset(GameType.Simple, 5, 5, PlayerType.Red)
          self.assertEqual(self.game.get_turn(), PlayerType.Red)

          self.game.reset(GameType.General, 5, 5, PlayerType.Blue)
          self.assertEqual(self.game.get_turn(), PlayerType.Blue)

    # Board dims, game mode, strting player turn, empty board
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
class TestGameMoves(unittest.TestCase):
    def setUp(self):
       self.game = GameBoard(GameType.Simple, 5, 5, PlayerType.Red)
    def tearDown(self):
        self.game = None # allow gc to clean up
    
    # test making and move and swithing turn
    def test_simple_game_moves(self):
        self.game.reset(GameType.Simple, 10, 15, PlayerType.Red)

        self.game.make_move(BoardSlotType.S, 1, 1)
        self.assertEqual(self.game.get_slot_type_for_spot(1, 1), BoardSlotType.S)
        self.assertEqual(self.game.get_turn(), PlayerType.Blue)

        self.game.make_move(BoardSlotType.O, 1, 2)
        self.assertEqual(self.game.get_slot_type_for_spot(1, 2), BoardSlotType.O)
        self.assertEqual(self.game.get_turn(), PlayerType.Red)

    # test making and move and swithing turn 
    # this test does not check iff tun stays same player when an sos is made because its not part of this sprint
    def test_genral_game_moves(self):
        self.game.reset(GameType.General, 10, 15, PlayerType.Red)

        self.game.make_move(BoardSlotType.S, 1, 1)
        self.assertEqual(self.game.get_slot_type_for_spot(1, 1), BoardSlotType.S)
        self.assertEqual(self.game.get_turn(), PlayerType.Blue)

        self.game.make_move(BoardSlotType.O, 1, 2)
        self.assertEqual(self.game.get_slot_type_for_spot(1, 2), BoardSlotType.O)
        self.assertEqual(self.game.get_turn(), PlayerType.Red)

if __name__ == '__main__':
    unittest.main()