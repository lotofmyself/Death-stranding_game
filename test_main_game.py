import pygame.event
import pytest
from main_game import generate_level, load_level, Tile, Camera, player_group


def test_update_player():
    """Проверка изменения положения персонажа на игровом поле"""
    playa, x, y = generate_level(['.....', '...@...', '....'])
    first_pos_y = playa.rect.y
    e1 = pygame.event.Event(pygame.K_DOWN, key=pygame.K_DOWN)
    player_group.update(e1, playa)
    assert (first_pos_y - playa.rect.y) == -10
    first_pos_y = playa.rect.y
    e1 = pygame.event.Event(pygame.K_DOWN, key=pygame.K_UP)
    player_group.update(e1, playa)
    assert (first_pos_y - playa.rect.y) == 10
    first_pos_x = playa.rect.x
    e1 = pygame.event.Event(pygame.K_DOWN, key=pygame.K_RIGHT)
    player_group.update(e1, playa)
    assert (first_pos_x - playa.rect.x) == -10
    first_pos_x = playa.rect.x
    e1 = pygame.event.Event(pygame.K_DOWN, key=pygame.K_LEFT)
    player_group.update(e1, playa)
    assert (first_pos_x - playa.rect.x) == 10


def test_load_level():
    """Проверка заполнения уровня"""
    as_result = ['.....................................................', '.....................................................', '.....................................................', '.....................................................', '...........###############################...........', '...........#@.............#............-##...........', '...........#.....#####....####.........###...........', '...........#..##########...#...###########...........', '...........##.###.......#####.######.....#...........', '...........#......##########...########.##...........', '...........#....######...###...####....###...........', '...........####...%###..................##...........', '...........###..##################.#######...........', '...........#...#.....#.............####..#...........', '...........###.##############......####..#...........', '...........#....##############....#####..#...........', '...........####...##.....######...#####.##...........', '...........###...#...#.....######..#######...........', '...........#.......#######..............##...........', '...........###############################...........', '.....................................................', '.....................................................', '.....................................................', '.....................................................']
    assert load_level('1lvl.txt') == as_result


def test_generate_level():
    """Проверка определения координат игрока и присвоения ему размеров"""
    playa, x, y = generate_level('...@...')
    assert playa.x == 0 and playa.y == 3 and playa.rect == (15, 155, 40, 40)
    playa, x, y = generate_level('......')
    assert playa is None


def test_update_camera():
    """Проверка изменения координат камеры"""
    level = load_level('1lvl.txt')
    playa, x, y = generate_level(level)
    camera = Camera((x, y))
    e1 = pygame.event.Event(pygame.K_DOWN, key=pygame.K_DOWN)
    player_group.update(e1, playa)
    n_pos_x = camera.dx
    n_pos_y = camera.dy
    camera.update(playa)
    assert camera.dx != n_pos_x and camera.dy != n_pos_y
