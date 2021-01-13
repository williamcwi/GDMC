from logger import Logger

from pymclevel import MCSchematic
from pymclevel.box import Vector

name = 'generateWalls'
logger = Logger(name)

def calc_wall_sections(box):
    try:

        x_len = box.size[0] - 16 # remove corner blocks: 8 per side
        z_len = box.size[2] - 16 # remove corner blocks: 8 per side

        if x_len < 6 or z_len < 6:
            logger.error("Box Selection too small")
            
        else:
            # x-axis
            if x_len <= 9:
                x_left = 0
                x_right = 0
                x_gate = x_len
            else:
                section_num = 0
                while x_len > 9:
                    x_len -= 4
                    section_num += 1
                if section_num % 2 == 0:
                    x_left = section_num / 2
                    x_right = section_num / 2
                    x_gate = x_len
                else:
                    x_left = (section_num - 1) / 2
                    x_right = ((section_num - 1) / 2) + 1
                    x_gate = x_len

            # z-axis
            if z_len <= 9:
                z_left = 0
                z_right = 0
                z_gate = z_len
            else:
                section_num = 0
                while z_len > 9:
                    z_len -= 4
                    section_num += 1
                if section_num % 2 == 0:
                    z_left = section_num / 2
                    z_right = section_num / 2
                    z_gate = z_len
                else:
                    z_left = (section_num - 1) / 2
                    z_right = ((section_num - 1) / 2) + 1
                    z_gate = z_len

            return x_left, x_right, x_gate, z_left, z_right, z_gate

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
        x_left, x_right, x_gate, z_left, z_right, z_gate = calc_wall_sections(box)
        print(x_left, x_right, x_gate, z_left, z_right, z_gate)
    except Exception as e:
        logger.error(e)