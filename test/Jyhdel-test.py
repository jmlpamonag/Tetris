# Owner: Jyhdel Mae L. Pamonag
# Revision Date: December 03, 2022
# Leader comments: test should be made for the next piece feature as well

import unittest
import Tetris
from unittest.mock import Mock
import pygame

class TestJyhdel(unittest.TestCase):
    def test_pause_continue(self):
        game = Tetris.Game()
        self.assertEqual(game.pause,True)
        self.assertEqual(game.pause,False)
        self.assertEqual(game.pause,True)

    def test_background_music(self):
        sound = Tetris.Sound(1)
        sound.in_game = Mock()
        sound.in_game()
        sound.in_game.assert_called_with('game-music.mp3')

if __name__ == "__main__":
    unittest.main()