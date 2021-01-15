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
        filename = os.path.join(os.path.dirname(__file__), 'schematics', 'wall', 'wall_{}.schematic'.format(wall_type))
        wall_corner = MCSchematic(shape=(8,12,8), filename=filename)
        ground = heightmap[len(heightmap)-1][0]
        level.copyBlocksFrom(wall_corner, wall_corner.bounds, Vector(box.maxx-8, ground, box.minz))
        logger.info('Placing {}s... (1/4)'.format(building))

        # -x -z:
        wall_corner.rotateLeft()
        ground = heightmap[0][0]
        level.copyBlocksFrom(wall_corner, wall_corner.bounds, Vector(box.minx, ground, box.minz))
        logger.info('Placing {}s... (2/4)'.format(building))

        # -x +z:
        wall_corner.rotateLeft()
        ground = heightmap[0][len(heightmap[0])-1]
        level.copyBlocksFrom(wall_corner, wall_corner.bounds, Vector(box.minx, ground, box.maxz-8))
        logger.info('Placing {}s... (3/4)'.format(building))
        
        # +x +z:
        wall_corner.rotateLeft()
        ground = heightmap[len(heightmap)-1][len(heightmap[len(heightmap)-1])-1]
        level.copyBlocksFrom(wall_corner, wall_corner.bounds, Vector(box.maxx-8, ground, box.maxz-8))
        logger.info('Placing {}s... (4/4)'.format(building))

        pass
    except Exception as e:
        logger.error(e)

def place_wall_sections(level, box, heightmap, x_left, x_right, z_left, z_right):
    try:
        # TODO: place wall sections

        wall_type = 'pillar' # wall_pillar (1x12x9)
        filename = os.path.join(os.path.dirname(__file__), 'schematics', 'wall', 'wall_{}.schematic'.format(wall_type))
        wall_pillar = MCSchematic(shape=(1,12,9), filename=filename)
        
        wall_type = 'left' # wall_left (1x11x8)
        filename = os.path.join(os.path.dirname(__file__), 'schematics', 'wall', 'wall_{}.schematic'.format(wall_type))
        wall_left = MCSchematic(shape=(1,11,8), filename=filename)

        wall_type = 'middle' # wall_middle (1x11x8)
        filename = os.path.join(os.path.dirname(__file__), 'schematics', 'wall', 'wall_{}.schematic'.format(wall_type))
        wall_middle = MCSchematic(shape=(1,11,8), filename=filename)

        wall_type = 'right' # wall_right (1x11x8)
        filename = os.path.join(os.path.dirname(__file__), 'schematics', 'wall', 'wall_{}.schematic'.format(wall_type))
        wall_right = MCSchematic(shape=(1,11,8), filename=filename)

        wall_type = 'base' # wall_base (3x6x7)
        filename = os.path.join(os.path.dirname(__file__), 'schematics', 'wall', 'wall_{}.schematic'.format(wall_type))
        wall_base = MCSchematic(shape=(3,6,7), filename=filename)

        # -z:
        # left: 
        i = 1
        for sections in range(x_left):
            for wt in range(4): # wall type
                if wt == 0: #left
                    ground = heightmap[len(heightmap)-8-i][1]
                    level.copyBlocksFrom(wall_left, wall_left.bounds, Vector(box.maxx-8-i, ground, box.minz+1))
                    i += 1
                elif wt == 1: # middle
                    ground = heightmap[len(heightmap)-8-i][1]
                    level.copyBlocksFrom(wall_middle, wall_middle.bounds, Vector(box.maxx-8-i, ground, box.minz+1))
                    i += 1
                elif wt == 2: # right
                    ground = heightmap[len(heightmap)-8-i][1]
                    level.copyBlocksFrom(wall_right, wall_right.bounds, Vector(box.maxx-8-i, ground, box.minz+1))
                    i += 1
                elif wt == 3: # pillar
                    ground = heightmap[len(heightmap)-8-i][1]
                    level.copyBlocksFrom(wall_pillar, wall_pillar.bounds, Vector(box.maxx-8-i, ground, box.minz))
                    i += 1

        # right: 
        i = 1
        for sections in range(x_right):
            for wt in range(4): # wall type
                if wt == 0: # right
                    ground = heightmap[8+i][1]
                    level.copyBlocksFrom(wall_right, wall_right.bounds, Vector(box.minx+7+i, ground, box.minz+1))
                    i += 1
                elif wt == 1: # middle
                    ground = heightmap[8+i][1]
                    level.copyBlocksFrom(wall_middle, wall_middle.bounds, Vector(box.minx+7+i, ground, box.minz+1))
                    i += 1
                elif wt == 2: #left
                    ground = heightmap[8+i][1]
                    level.copyBlocksFrom(wall_left, wall_left.bounds, Vector(box.minx+7+i, ground, box.minz+1))
                    i += 1
                elif wt == 3: # pillar
                    ground = heightmap[8+i][1]
                    level.copyBlocksFrom(wall_pillar, wall_pillar.bounds, Vector(box.minx+7+i, ground, box.minz))
                    i += 1

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

def place_gates(level, box, heightmap, x_gate, z_gate):
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
        place_wall_sections(level, box, heightmap, x_left, x_right, z_left, z_right)
        place_gates(level, box, heightmap, x_gate, z_gate)

    except Exception as e:
        logger.error(e)