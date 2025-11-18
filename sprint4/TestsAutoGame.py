'''
Ryan Phillips 
UMKC CS 449 Sprint 4 Tests
TestsAutoGame.py

Tests for the AutoGame game subclass
'''
import unittest

from AutoGame import *


class TestAutoGame(unittest.TestCase):
    def setUp(self):
       self.game = AutoGame(5, 5, PlayerType.Red, True, False)
    def tearDown(self):
        self.game = None # allow gc to clean up