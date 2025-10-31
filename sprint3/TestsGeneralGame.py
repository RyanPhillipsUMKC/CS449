'''
Ryan Phillips 
UMKC CS 449 Sprint 3 Tests
TestsGeneralGame.py

Tests for the GeneralGame sub class
'''
import unittest

from GeneralGame import *

class TestSimpleGame(unittest.TestCase):
    def setUp(self):
        self.game = GeneralGame(GameType.General, 5, 5, PlayerType.Red)
    def tearDown(self):
        self.game = None # allow gc to clean up

    # AC 7.1 - game does not end until board is full - not a first sos
    def test_game_ongoing_when_first_sos_made(self):
        self.game.reset(GameType.General, 5, 5, PlayerType.Red)

        self.game.make_move(BoardSlotType.S, 0, 0)
        self.game.make_move(BoardSlotType.O, 0, 1)
        self.game.make_move(BoardSlotType.S, 0, 2)

        self.assertEqual(self.game.game_state, GameStateType.Ongoing)

    # AC 7.1 - game is one by plater with most soses on board full
    def test_game_win_on_board_full_blue_had_most_soses(self):
        self.game.reset(GameType.General, 3, 3, PlayerType.Blue)

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
    def test_game_win_on_board_full_blue_had_most_soses(self):
        self.game.reset(GameType.General, 3, 3, PlayerType.Red)

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
        self.game.reset(GameType.General, 5, 5, PlayerType.Blue)

        for row in range(5):
            for col in range(5):
                self.game.make_move(BoardSlotType.S, row, col)

        self.assertEqual(self.game.game_state, GameStateType.Draw)

if __name__ == "__main__":
    unittest.main()