'''
Ryan Phillips 
UMKC CS 449 Sprint 5 Tests
TestsGeneralGame.py

Tests for the GeneralGame sub class
'''
import unittest

from GeneralGame import *

class TestGeneralGame(unittest.TestCase):
    def setUp(self):
        self.game = GeneralGame(5, 5, PlayerType.Red)
    def tearDown(self):
        self.game = None # allow gc to clean up

    # AC 2.1 Game mode config
    def test_game_mode_configs(self):
        self.assertEqual(self.game.get_game_type(), GameType.General)
        self.assertEqual(isinstance(self.game, GeneralGame), True)

    # AC 3.1 Board dims, game mode, strting player turn, empty board
    def test_full_config(self):
          self.game.reset(10, 15, PlayerType.Red)
          self.assertEqual(self.game.get_board_size_x(), 10)
          self.assertEqual(self.game.get_board_size_y(), 15)
          self.assertEqual(self.game.get_game_type(), GameType.General)
          self.assertEqual(isinstance(self.game, GeneralGame), True)
          self.assertEqual(self.game.get_turn(), PlayerType.Red)

          for row in range(self.game.get_board_size_x()):
            for col in range(self.game.get_board_size_y()):
                self.assertEqual(self.game.get_slot_type_for_spot(row, col), BoardSlotType.Empty)

    # AC 6.1 test making and move and swithing turn - general game
    def test_general_game_valid_moves(self):
        self.game.reset(10, 15, PlayerType.Red)

        self.game.make_move(BoardSlotType.S, 1, 1)
        self.assertEqual(self.game.get_slot_type_for_spot(1, 1), BoardSlotType.S)
        self.assertEqual(self.game.get_turn(), PlayerType.Blue)

        self.game.make_move(BoardSlotType.O, 1, 2)
        self.assertEqual(self.game.get_slot_type_for_spot(1, 2), BoardSlotType.O)
        self.assertEqual(self.game.get_turn(), PlayerType.Red)

    # AC 6.2 test invalid move - spot already taken - general game
    def test_general_game_invalid_move_spot_taken(self):
        self.game.reset(10, 15, PlayerType.Red)

        self.game.make_move(BoardSlotType.S, 1, 1)
        self.assertEqual(self.game.get_slot_type_for_spot(1, 1), BoardSlotType.S)
        self.assertEqual(self.game.get_turn(), PlayerType.Blue)

        # try to move on spot already taken
        self.assertEqual(self.game.make_move(BoardSlotType.O, 1, 1).type, MovefunctionReturnType.SpotAlreadyTaken)
        self.assertEqual(self.game.get_slot_type_for_spot(1, 1), BoardSlotType.S)
        self.assertEqual(self.game.get_turn(), PlayerType.Blue)

    # AC 6.3 test invalid move - invalid row index - general game
    def test_general_game_invalid_move_row(self):
        self.game.reset(10, 15, PlayerType.Red)

        # try to move on invalid row
        self.assertEqual(self.game.make_move(BoardSlotType.O, 20, 1).type, MovefunctionReturnType.InvalidSpot)
        self.assertEqual(self.game.get_turn(), PlayerType.Red)

    # AC 6.4 test invalid move - invalid column index - general game
    def test_general_game_invalid_move_column(self):
        self.game.reset(10, 15, PlayerType.Red)

        # try to move on invalid row
        self.assertEqual(self.game.make_move(BoardSlotType.O, 5, 100).type, MovefunctionReturnType.InvalidSpot)
        self.assertEqual(self.game.get_turn(), PlayerType.Red)

    # AC 7.1 - game does not end until board is full - not a first sos
    def test_game_ongoing_when_first_sos_made(self):
        self.game.reset(5, 5, PlayerType.Red)

        self.game.make_move(BoardSlotType.S, 0, 0)
        self.game.make_move(BoardSlotType.O, 0, 1)
        self.game.make_move(BoardSlotType.S, 0, 2)

        self.assertEqual(self.game.game_state, GameStateType.Ongoing)

    # AC 7.1 - game is one by plater with most soses on board full
    def test_game_win_on_board_full_blue_had_most_soses(self):
        self.game.reset(3, 3, PlayerType.Blue)

        self.game.make_move(BoardSlotType.S, 0, 0)
        self.game.make_move(BoardSlotType.O, 0, 1)
        self.game.make_move(BoardSlotType.S, 0, 2)

        self.game.make_move(BoardSlotType.S, 1, 0)
        self.game.make_move(BoardSlotType.O, 1, 1)
        self.game.make_move(BoardSlotType.S, 1, 2)

        self.game.make_move(BoardSlotType.S, 2, 0)
        self.game.make_move(BoardSlotType.O, 2, 1)
        self.game.make_move(BoardSlotType.S, 2, 2)

        self.assertEqual(self.game.game_state, GameStateType.Blue_Win)

    # AC 7.1 - game is one by plater with most soses on board full
    def test_game_win_on_board_full_Red_had_most_soses(self):
        self.game.reset(3, 3, PlayerType.Red)

        self.game.make_move(BoardSlotType.S, 0, 0)
        self.game.make_move(BoardSlotType.O, 0, 1)
        self.game.make_move(BoardSlotType.S, 0, 2)

        self.game.make_move(BoardSlotType.S, 1, 0)
        self.game.make_move(BoardSlotType.O, 1, 1)
        self.game.make_move(BoardSlotType.S, 1, 2)

        self.game.make_move(BoardSlotType.S, 2, 0)
        self.game.make_move(BoardSlotType.O, 2, 1)
        self.game.make_move(BoardSlotType.S, 2, 2)

        self.assertEqual(self.game.game_state, GameStateType.Red_Win)

    # AC 7.2 - Game is a draw on board full and equal soses by both players
    def test_game_draw_on_board_full_equal_soses(self):
        self.game.reset(5, 5, PlayerType.Blue)

        for row in range(5):
            for col in range(5):
                self.game.make_move(BoardSlotType.S, row, col)

        self.assertEqual(self.game.game_state, GameStateType.Draw)

if __name__ == "__main__":
    unittest.main()