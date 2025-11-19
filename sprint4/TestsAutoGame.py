'''
Ryan Phillips 
UMKC CS 449 Sprint 4 Tests
TestsAutoGame.py

Tests for the AutoGame game subclass
'''
import unittest

from AutoGame import *

# AC 8.* -9.*
class TestAutoGame(unittest.TestCase):
    def setUp(self):
       self.game = AutoGame(5, 5, PlayerType.Red, True, False)
    def tearDown(self):
        self.game = None # allow gc to clean up

  # AC 8.1 - red can be a computer
    def test_computer_red_player_type(self):
        self.game = AutoGame(5, 5, PlayerType.Red, True, False)
        self.assertEqual(self.game.is_red_computer(), True)
        self.assertEqual(self.game.is_blue_computer(), False)

    # AC 8.2 - blue can be a compuet 
    def test_computer_blue_player_type(self):
          self.game = AutoGame(5, 5, PlayerType.Red, True, False)
          self.assertEqual(self.game.is_red_computer(), True)
          self.assertEqual(self.game.is_blue_computer(), False)

    # AC 9.1 - move with most soses
    def test_autoplay_make_best_move(self):
          self.game = AutoGame(5, 5, PlayerType.Red, True, False)
          # inject state
          self.game.state[0][0] = BoardSlotType.S
          self.game.state[0][1] = BoardSlotType.O
          move_return_data = self.game.make_move(BoardSlotType.S, -1, -1)
          self.assertEqual(len(move_return_data.soses_made), 1)

     # AC 9.2 - random move when no soses can be made
    def test_autoplay_make_random_move_if_no_soses_available(self):
          self.game = AutoGame(5, 5, PlayerType.Red, True, False)
          move_return_data = self.game.make_move(BoardSlotType.S, -1, -1)
          self.assertEqual(
               move_return_data.slot_type, 
               self.game.get_slot_type_for_spot(move_return_data.row, move_return_data.col))
          
if __name__ == '__main__':
    unittest.main()