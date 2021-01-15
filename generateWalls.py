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

def place_wall_corners(level, box, heightmap):
    try:
        wall_type = 'corner'
        building = 'wall {}'.format(wall_type)

        # +x -z:
        # |----------|
        # |          |
        # |          |
        # |          |
        # |          *
        # |_________**
        
        filename = os.path.join(os.path.dirname(__file__), 'schematics', 'wall', 'wall_{}.schematic'.format(wall_type))
        schematic = MCSchematic(shape=(8,12,8), filename=filename)
        ground = heightmap[len(heightmap)-1][0]
        level.copyBlocksFrom(schematic, schematic.bounds, Vector(box.maxx-8, ground, box.minz))

        # -x -z:
        # |----------|
        # |          |
        # |          |
        # |          |
        # *          |
        # **_________|

        schematic.rotateLeft()
        ground = heightmap[0][0]
        level.copyBlocksFrom(schematic, schematic.bounds, Vector(box.minx, ground, box.minz))

        # -x +z:
        # **---------|
        # *          |
        # |          |
        # |          |
        # |          |
        # |__________|

        schematic.rotateLeft()
        ground = heightmap[0][len(heightmap[0])-1]
        level.copyBlocksFrom(schematic, schematic.bounds, Vector(box.minx, ground, box.maxz-8))
        
        # +x +z:
        # |---------**
        # |          *
        # |          |
        # |          |
        # |          |
        # |__________|

        schematic.rotateLeft()
        ground = heightmap[len(heightmap)-1][len(heightmap[len(heightmap)-1])-1]
        level.copyBlocksFrom(schematic, schematic.bounds, Vector(box.maxx-8, ground, box.maxz-8))

        pass
    except Exception as e:
        logger.error(e)

def place_wall_sections(level, box, heightmap):
    try:
        # TODO: place wall sections
        # wall_pillar (1x12x9)
        # wall_left (1x11x8)
        # wall_middle (1x11x8)
        # wall_right (1x11x8)
        # wall_base (3x6x7)
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

def place_gates(level, box, heightmap):
    try:
        # TODO: place gates based on gate size
        pass
    except Exception as e:
        logger.error(e)

def place_walls(level, box, heightmap):
    try:
        # TODO: place walls together
        x_left, x_right, x_gate, z_left, z_right, z_gate = calc_wall_sections(box) # calculate wall sections and gate sizes
        
        place_wall_corners(level, box, heightmap)
        place_wall_sections(level, box, heightmap)
        place_gates(level, box, heightmap)

    except Exception as e:
        logger.error(e)