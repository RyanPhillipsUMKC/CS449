'''
Ryan Phillips 
UMKC CS 449 Sprint 5 Tests
TestsSimpleGame.py

Tests for the SimpleGame sub class
'''
import unittest

from SimpleGame import *

class TestSimpleGame(unittest.TestCase):
    def setUp(self):
       self.game = SimpleGame(5, 5, PlayerType.Red)
    def tearDown(self):
        self.game = None # allow gc to clean up

    # AC 2.1 Game mode config
    def test_game_mode_configs(self):
        self.assertEqual(self.game.get_game_type(), GameType.Simple)
        self.assertEqual(isinstance(self.game, SimpleGame), True)

    # AC 3.1 Board dims, game mode, strting player turn, empty board
    def test_full_config(self):
          self.game.reset(10, 15, PlayerType.Red)
          self.assertEqual(self.game.get_board_size_x(), 10)
          self.assertEqual(self.game.get_board_size_y(), 15)
          self.assertEqual(self.game.get_game_type(), GameType.Simple)
          self.assertEqual(isinstance(self.game, SimpleGame), True)
          self.assertEqual(self.game.get_turn(), PlayerType.Red)

          for row in range(self.game.get_board_size_x()):
            for col in range(self.game.get_board_size_y()):
                self.assertEqual(self.game.get_slot_type_for_spot(row, col), BoardSlotType.Empty)

    # AC 4.1 test making and move and swithing turn - simple game
    def test_simple_game_valid_moves(self):
        self.game.reset(10, 15, PlayerType.Red)

        self.game.make_move(BoardSlotType.S, 1, 1)
        self.assertEqual(self.game.get_slot_type_for_spot(1, 1), BoardSlotType.S)
        self.assertEqual(self.game.get_turn(), PlayerType.Blue)

        self.game.make_move(BoardSlotType.O, 1, 2)
        self.assertEqual(self.game.get_slot_type_for_spot(1, 2), BoardSlotType.O)
        self.assertEqual(self.game.get_turn(), PlayerType.Red)

    # AC 4.2 test invalid move - spot already taken - simple game
    def test_simple_game_invalid_move_spot_taken(self):
        self.game.reset(10, 15, PlayerType.Red)

        self.game.make_move(BoardSlotType.S, 1, 1)
        self.assertEqual(self.game.get_slot_type_for_spot(1, 1), BoardSlotType.S)
        self.assertEqual(self.game.get_turn(), PlayerType.Blue)

        # try to move on spot already taken
        self.assertEqual(self.game.make_move(BoardSlotType.O, 1, 1).type, MovefunctionReturnType.SpotAlreadyTaken)
        self.assertEqual(self.game.get_slot_type_for_spot(1, 1), BoardSlotType.S)
        self.assertEqual(self.game.get_turn(), PlayerType.Blue)

    # AC 4.3 test invalid move - invalid row index - simple game
    def test_simple_game_invalid_move_row(self):
        self.game.reset(10, 15, PlayerType.Red)

        # try to move on invalid row
        self.assertEqual(self.game.make_move(BoardSlotType.O, 20, 1).type, MovefunctionReturnType.InvalidSpot)
        self.assertEqual(self.game.get_turn(), PlayerType.Red)

    # AC 4.4 test invalid move - invalid column index - simple game
    def test_simple_game_invalid_move_column(self):
        self.game.reset(10, 15, PlayerType.Red)

        # try to move on invalid row
        self.assertEqual(self.game.make_move(BoardSlotType.O, 5, 100).type, MovefunctionReturnType.InvalidSpot)
        self.assertEqual(self.game.get_turn(), PlayerType.Red)

    # AC 5.1 test game won on first sos - red player
    def test_game_win_on_first_sos_made_by_red(self):
        self.game.reset(5, 5, PlayerType.Red)

        self.game.make_move(BoardSlotType.S, 0, 0)
        self.game.make_move(BoardSlotType.O, 0, 1)
        self.game.make_move(BoardSlotType.S, 0, 2)

        self.assertEqual(self.game.game_state, GameStateType.Red_Win)

    # AC 5.1 test game won on first sos - blue player
    def test_game_win_on_first_sos_made_by_blue(self):
        self.game.reset(5, 5, PlayerType.Blue)

        self.game.make_move(BoardSlotType.S, 0, 0)
        self.game.make_move(BoardSlotType.O, 0, 1)
        self.game.make_move(BoardSlotType.S, 0, 2)

        self.assertEqual(self.game.game_state, GameStateType.Blue_Win)

    # AC 5.2 test game draw on board full
    def test_game_draw_on_board_full(self):
        self.game.reset(5, 5, PlayerType.Blue)

        for row in range(5):
            for col in range(5):
                self.game.make_move(BoardSlotType.S, row, col)

        self.assertEqual(self.game.game_state, GameStateType.Draw)

if __name__ == "__main__":
    unittest.main()