# Owner: Hai Hoang
# Revision Date: December 03, 2022
# Leader comments: Looks good

import unittest
import Tetris
from unittest.mock import Mock
import pygame

class TestHai(unittest.TestCase):
    def test_combo(self):
        game = Tetris.Game()
        self.assertEqual(game.combo,-1)
        self.assertEqual(game.combo_score_computation(4),24)
        self.assertEqual(game.combo_score_computation(4),40)
        self.assertEqual(game.combo,7)
        self.assertEqual(game.combo_score_computation(0),0)
        self.assertEqual(game.combo_score_computation(4),24)
    def test_sound(self):
        sound = Tetris.Sound(1)
        sound.load_sound = Mock()
        sound.highscore()
        sound.load_sound.assert_called_with('ode_to_joy_snip.mp3')
        sound.hitmarker()
        sound.load_sound.assert_called_with('hitmarker_2.mp3')
        sound.not_highscore()
        sound.load_sound.assert_called_with('spongebob-boowomp.mp3')

if __name__ == "__main__":
    unittest.main()