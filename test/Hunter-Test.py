# Owner: Hunter Giordullo
# Revision Date: December 03, 2022
# Leader comments: Looks good

import unittest
import Tetris
from unittest.mock import Mock
import pygame

class TestHunter(unittest.TestCase):
    def test_dark_mode(self):
        visuals = Tetris.Visuals()
        visuals.set_dark_mode() # dark mode on
        visuals.set_dark_mode() # dark mode off
        visuals.set_dark_mode() # dark mode on
        visuals.set_dark_mode() # dark mode off     
    def test_scoreboard(self):
        scoreboard = Tetris.Scoreboard()
        scoreboard.add_score(1)
        scoreboard.add_score(2)
        scoreboard.add_score(3)
        scoreboard.add_score(4)
        scoreboard.add_score(5)
        scoreboard.add_score(6)
        scoreboard.add_score(7)
        scoreboard.add_score(8)
        scoreboard.add_score(9)
        scoreboard.add_score(10) # Will write to 10 the overwrite after
        scoreboard.add_score(11) # Make sure the score of 1 is overwritten
    def test_hold_piece(self):
        game = Tetris.Game()
        game.hold_piece() # hold current piece
        game.hold_piece() # hold next piece

if __name__ == "__main__":
    unittest.main()