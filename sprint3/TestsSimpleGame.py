'''
Ryan Phillips 
UMKC CS 449 Sprint 3 Tests
TestsSimpleGame.py

Tests for the SimpleGame sub class
'''
import unittest

from SimpleGame import *

class TestSimpleGame(unittest.TestCase):
    def setUp(self):
       self.game = SimpleGame(GameType.Simple, 5, 5, PlayerType.Red)
    def tearDown(self):
        self.game = None # allow gc to clean up

    def test_game_win_on_first_sos_made_by_red(self):
        self.game.reset(GameType.Simple, 5, 5, PlayerType.Red)

        self.game.make_move(BoardSlotType.S, 0, 0)
        self.game.make_move(BoardSlotType.O, 0, 1)
        self.game.make_move(BoardSlotType.S, 0, 2)

        self.assertEqual(self.game.game_state, GameStateType.Red_Win)

    def test_game_win_on_first_sos_made_by_blue(self):
        self.game.reset(GameType.Simple, 5, 5, PlayerType.Blue)

        self.game.make_move(BoardSlotType.S, 0, 0)
        self.game.make_move(BoardSlotType.O, 0, 1)
        self.game.make_move(BoardSlotType.S, 0, 2)

        self.assertEqual(self.game.game_state, GameStateType.Blue_Win)

    def test_game_draw_on_board_full(self):
        self.game.reset(GameType.Simple, 5, 5, PlayerType.Blue)

        for row in range(5):
            for col in range(5):
                self.game.make_move(BoardSlotType.S, row, col)

        self.assertEqual(self.game.game_state, GameStateType.Draw)

if __name__ == "__main__":
    unittest.main()