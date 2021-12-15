import pytest
from main_game import generate_level, load_level, Tile, Camera

def test_generate_level():
    new_player, x, y = None, None, None
    playa, x, y = generate_level('...@...')
    assert playa != None and x == 0 and y == 6

def test_update_camera():
    level = load_level('1lvl.txt')
    playa, x, y = generate_level(level)
    camera = Camera((x, y))
    assert camera.update(playa) != (0,0)