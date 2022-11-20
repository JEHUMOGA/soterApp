WIDTH = 1440
HEIGHT = 720
GRID_SIZE = 6
CELL_COUNT = GRID_SIZE ** 2
MINES_COUNT = (GRID_SIZE ** 2) // 4


def height_prct(porcentage):
    return (HEIGHT / 100) * porcentage


def width_prct(porcentage):
    return (WIDTH / 100) * porcentage
