import pytest
from main_game import generate_level, load_level


def test_generate_level():
    new_player, x = None, None
    y = None
    load_level('1lvl')
    level = load_level('3lvl')
    generate_level(level)
    assert (new_player, x != None, None) and y != None
