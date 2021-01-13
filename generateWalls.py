from logger import Logger

from pymclevel import MCSchematic
from pymclevel.box import Vector

name = 'generateWalls'
logger = Logger(name)

def calc_wall_sections(box):
    try:
        # TODO: calculate and return:
        # - x_left
        # - x_right
        # - z_left
        # - z_right
        # - gate
        # 8 Blocks each side for the corners
        # remaining blocks between 6-9 inclusive for gate
        pass
    except Exception as e:
        logger.error(e)

def place_wall_sections(level, box):
    try:
        # TODO: place wall sections
            # +z:
            # |-********-|
            # |          |
            # |          |
            # |          |
            # |          |
            # |__________|

            # -z:
            # |----------|
            # |          |
            # |          |
            # |          |
            # |          |
            # |_********_|

            # +x:
            # |----------|
            # |          |
            # |          *
            # |          *
            # |          |
            # |__________|

            # -x:
            # |----------|
            # |          |
            # *          |
            # *          |
            # |          |
            # |__________|
        pass
    except Exception as e:
        logger.error(e)

def place_wall_corners(level, box):
    try:
        # TODO: place wall corners
            # -x +z:
            # **---------|
            # *          |
            # |          |
            # |          |
            # |          |
            # |__________|

            # +x +z:
            # |---------**
            # |          *
            # |          |
            # |          |
            # |          |
            # |__________|

            # -x -z:
            # |----------|
            # |          |
            # |          |
            # |          |
            # *          |
            # **_________|

            # +x -z:
            # |----------|
            # |          |
            # |          |
            # |          |
            # |          *
            # |_________**
        pass
    except Exception as e:
        logger.error(e)

def place_gates(level, box):
    try:
        # TODO: place gates based on gate size
        pass
    except Exception as e:
        logger.error(e)

def place_walls(level, box):
    try:
        # TODO: place walls together
        pass
    except Exception as e:
        logger.error(e)