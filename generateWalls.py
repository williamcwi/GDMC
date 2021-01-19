from logger import Logger

from pymclevel import MCSchematic
from pymclevel.box import Vector

import os.path

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
        progress = 0

        # +x -z:
        filename = os.path.join(os.path.dirname(__file__), 'schematics', 'wall', 'wall_{}.schematic'.format(wall_type))
        wall_corner = MCSchematic(shape=(8,12,8), filename=filename)
        ground = heightmap[len(heightmap)-1][0]
        level.copyBlocksFrom(wall_corner, wall_corner.bounds, Vector(box.maxx-8, ground, box.minz))
        progress += 1
        logger.info('Placing {}s... ({}/4)'.format(building, progress))

        # -x -z:
        wall_corner.rotateLeft()
        ground = heightmap[0][0]
        level.copyBlocksFrom(wall_corner, wall_corner.bounds, Vector(box.minx, ground, box.minz))
        progress += 1
        logger.info('Placing {}s... ({}/4)'.format(building, progress))

        # -x +z:
        wall_corner.rotateLeft()
        ground = heightmap[0][len(heightmap[0])-1]
        level.copyBlocksFrom(wall_corner, wall_corner.bounds, Vector(box.minx, ground, box.maxz-8))
        progress += 1
        logger.info('Placing {}s... ({}/4)'.format(building, progress))
        
        # +x +z:
        wall_corner.rotateLeft()
        ground = heightmap[len(heightmap)-1][len(heightmap[len(heightmap)-1])-1]
        level.copyBlocksFrom(wall_corner, wall_corner.bounds, Vector(box.maxx-8, ground, box.maxz-8))
        progress += 1
        logger.info('Placing {}s... ({}/4)'.format(building, progress))

        pass
    except Exception as e:
        logger.error(e)

def place_wall_sections(level, box, heightmap, x_left, x_right, z_left, z_right):
    try:
        building = 'wall section'
        progress = 0

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

        # TODO: Rotate wall_base 180 deg

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
                    if sections is not x_left - 1:
                        ground = heightmap[len(heightmap)-8-i][1]
                        level.copyBlocksFrom(wall_right, wall_right.bounds, Vector(box.maxx-8-i, ground, box.minz+1))
                        i += 1
                elif wt == 3: # pillar
                    if sections is not x_left - 1:
                        ground = heightmap[len(heightmap)-8-i][1]
                        level.copyBlocksFrom(wall_pillar, wall_pillar.bounds, Vector(box.maxx-8-i, ground, box.minz))
                        i += 1
            # TODO: Generate wall_base

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
                    if sections is not x_right - 1:
                        ground = heightmap[8+i][1]
                        level.copyBlocksFrom(wall_left, wall_left.bounds, Vector(box.minx+7+i, ground, box.minz+1))
                        i += 1
                    else: 
                        gate_pos_1 = Vector(box.minx+7+i, ground, box.minz)
                elif wt == 3: # pillar
                    if sections is not x_right - 1:
                        ground = heightmap[8+i][1]
                        level.copyBlocksFrom(wall_pillar, wall_pillar.bounds, Vector(box.minx+7+i, ground, box.minz))
                        i += 1
            # TODO: Generate wall_base
        progress += 1

        logger.info('Placing {}s... ({}/4)'.format(building, progress))

        wall_pillar.rotateLeft()
        wall_left.rotateLeft()
        wall_middle.rotateLeft()
        wall_right.rotateLeft()
        wall_base.rotateLeft()

        # -x:
        # left: 
        i = 1
        for sections in range(z_left):
            for wt in range(4): # wall type
                if wt == 0: #left
                    ground = heightmap[1][8+i]
                    level.copyBlocksFrom(wall_left, wall_left.bounds, Vector(box.minx+1, ground, box.minz+7+i))
                    i += 1
                elif wt == 1: # middle
                    ground = heightmap[1][8+i]
                    level.copyBlocksFrom(wall_middle, wall_middle.bounds, Vector(box.minx+1, ground, box.minz+7+i))
                    i += 1
                elif wt == 2: # right
                    if sections is not z_left - 1:
                        ground = heightmap[1][8+i]
                        level.copyBlocksFrom(wall_right, wall_right.bounds, Vector(box.minx+1, ground, box.minz+7+i))
                        i += 1
                    else: 
                        gate_pos_2 = Vector(box.minx, ground, box.minz+7+i)
                elif wt == 3: # pillar
                    if sections is not z_left - 1:
                        ground = heightmap[1][8+i]
                        level.copyBlocksFrom(wall_pillar, wall_pillar.bounds, Vector(box.minx, ground, box.minz+7+i))
                        i += 1
            # TODO: Generate wall_base

        # right: 
        i = 1
        for sections in range(z_right):
            for wt in range(4): # wall type
                if wt == 0: # right
                    ground = heightmap[1][len(heightmap[1])-8-i]
                    level.copyBlocksFrom(wall_right, wall_right.bounds, Vector(box.minx+1, ground, box.maxz-8-i))
                    i += 1
                elif wt == 1: # middle
                    ground = heightmap[1][len(heightmap[1])-8-i]
                    level.copyBlocksFrom(wall_middle, wall_middle.bounds, Vector(box.minx+1, ground, box.maxz-8-i))
                    i += 1
                elif wt == 2: #left
                    if sections is not z_right - 1:
                        ground = heightmap[1][len(heightmap[1])-8-i]
                        level.copyBlocksFrom(wall_left, wall_left.bounds, Vector(box.minx+1, ground, box.maxz-8-i))
                        i += 1
                elif wt == 3: # pillar
                    if sections is not z_right - 1:
                        ground = heightmap[1][len(heightmap[1])-8-i]
                        level.copyBlocksFrom(wall_pillar, wall_pillar.bounds, Vector(box.minx, ground, box.maxz-8-i))
                        i += 1
            # TODO: Generate wall_base
        progress += 1

        logger.info('Placing {}s... ({}/4)'.format(building, progress))

        wall_pillar.rotateLeft()
        wall_left.rotateLeft()
        wall_middle.rotateLeft()
        wall_right.rotateLeft()
        wall_base.rotateLeft()

        # +z:
        # left: 
        i = 1
        for sections in range(x_left):
            for wt in range(4): # wall type
                if wt == 0: #left
                    ground = heightmap[len(heightmap)-8-i][len(heightmap[len(heightmap)-8-i])-2]
                    level.copyBlocksFrom(wall_right, wall_right.bounds, Vector(box.maxx-8-i, ground, box.maxz-9))
                    i += 1
                elif wt == 1: # middle
                    ground = heightmap[len(heightmap)-8-i][len(heightmap[len(heightmap)-8-i])-2]
                    level.copyBlocksFrom(wall_middle, wall_middle.bounds, Vector(box.maxx-8-i, ground, box.maxz-9))
                    i += 1
                elif wt == 2: # right
                    if sections is not x_left - 1:
                        ground = heightmap[len(heightmap)-8-i][len(heightmap[len(heightmap)-8-i])-2]
                        level.copyBlocksFrom(wall_left, wall_left.bounds, Vector(box.maxx-8-i, ground, box.maxz-9))
                        i += 1
                elif wt == 3: # pillar
                    if sections is not x_left - 1:
                        ground = heightmap[len(heightmap)-8-i][len(heightmap[len(heightmap)-8-i])-2]
                        level.copyBlocksFrom(wall_pillar, wall_pillar.bounds, Vector(box.maxx-8-i, ground, box.maxz-9))
                        i += 1
            # TODO: Generate wall_base

        # right: 
        i = 1
        for sections in range(x_right):
            for wt in range(4): # wall type
                if wt == 0: # right
                    ground = heightmap[8+i][len(heightmap[8+i])-2]
                    level.copyBlocksFrom(wall_left, wall_left.bounds, Vector(box.minx+7+i, ground, box.maxz-9))
                    i += 1
                elif wt == 1: # middle
                    ground = heightmap[8+i][len(heightmap[8+i])-2]
                    level.copyBlocksFrom(wall_middle, wall_middle.bounds, Vector(box.minx+7+i, ground, box.maxz-9))
                    i += 1
                elif wt == 2: #left
                    if sections is not x_right - 1:
                        ground = heightmap[8+i][len(heightmap[8+i])-2]
                        level.copyBlocksFrom(wall_right, wall_right.bounds, Vector(box.minx+7+i, ground, box.maxz-9))
                        i += 1
                    else: 
                        gate_pos_3 = Vector(box.minx+7+i, ground, box.maxz-9)
                elif wt == 3: # pillar
                    if sections is not x_right - 1:
                        ground = heightmap[8+i][len(heightmap[8+i])-2]
                        level.copyBlocksFrom(wall_pillar, wall_pillar.bounds, Vector(box.minx+7+i, ground, box.maxz-9))
                        i += 1
            # TODO: Generate wall_base
        progress += 1

        logger.info('Placing {}s... ({}/4)'.format(building, progress))

        wall_pillar.rotateLeft()
        wall_left.rotateLeft()
        wall_middle.rotateLeft()
        wall_right.rotateLeft()
        wall_base.rotateLeft()

        # -x:
        # left: 
        i = 1
        for sections in range(z_left):
            for wt in range(4): # wall type
                if wt == 0: #left
                    ground = heightmap[len(heightmap)-2][8+i]
                    level.copyBlocksFrom(wall_right, wall_right.bounds, Vector(box.maxx-9, ground, box.minz+7+i))
                    i += 1
                elif wt == 1: # middle
                    ground = heightmap[len(heightmap)-2][8+i]
                    level.copyBlocksFrom(wall_middle, wall_middle.bounds, Vector(box.maxx-9, ground, box.minz+7+i))
                    i += 1
                elif wt == 2: # right
                    if sections is not z_left - 1:
                        ground = heightmap[len(heightmap)-2][8+i]
                        level.copyBlocksFrom(wall_left, wall_left.bounds, Vector(box.maxx-9, ground, box.minz+7+i))
                        i += 1
                    else: 
                        gate_pos_4 = Vector(box.maxx-9, ground, box.minz+7+i)
                elif wt == 3: # pillar
                    if sections is not z_left - 1:
                        ground = heightmap[len(heightmap)-2][8+i]
                        level.copyBlocksFrom(wall_pillar, wall_pillar.bounds, Vector(box.maxx-9, ground, box.minz+7+i))
                        i += 1
            # TODO: Generate wall_base

        # right: 
        i = 1
        for sections in range(z_right):
            for wt in range(4): # wall type
                if wt == 0: # right
                    ground = heightmap[len(heightmap)-2][len(heightmap[len(heightmap)-2])-8-i]
                    level.copyBlocksFrom(wall_left, wall_left.bounds, Vector(box.maxx-9, ground, box.maxz-8-i))
                    i += 1
                elif wt == 1: # middle
                    ground = heightmap[len(heightmap)-2][len(heightmap[len(heightmap)-2])-8-i]
                    level.copyBlocksFrom(wall_middle, wall_middle.bounds, Vector(box.maxx-9, ground, box.maxz-8-i))
                    i += 1
                elif wt == 2: #left
                    if sections is not z_right - 1:
                        ground = heightmap[len(heightmap)-2][len(heightmap[len(heightmap)-2])-8-i]
                        level.copyBlocksFrom(wall_right, wall_right.bounds, Vector(box.maxx-9, ground, box.maxz-8-i))
                        i += 1
                elif wt == 3: # pillar
                    if sections is not z_right - 1:
                        ground = heightmap[len(heightmap)-2][len(heightmap[len(heightmap)-2])-8-i]
                        level.copyBlocksFrom(wall_pillar, wall_pillar.bounds, Vector(box.maxx-9, ground, box.maxz-8-i))
                        i += 1
            # TODO: Generate wall_base
        progress += 1

        logger.info('Placing {}s... ({}/4)'.format(building, progress))

        return gate_pos_1, gate_pos_2, gate_pos_3, gate_pos_4

    except Exception as e:
        logger.error(e)

def get_gate_schem(width):
    try:
        if width == 6:
            filename = os.path.join(os.path.dirname(__file__), 'schematics', 'wall', 'gate', 'gate_6.schematic')
            return MCSchematic(shape=(10,12,9), filename=filename)
        elif width == 7:
            filename = os.path.join(os.path.dirname(__file__), 'schematics', 'wall', 'gate', 'gate_7.schematic')
            return MCSchematic(shape=(11,12,9), filename=filename)
        elif width == 8:
            filename = os.path.join(os.path.dirname(__file__), 'schematics', 'wall', 'gate', 'gate_8.schematic')
            return MCSchematic(shape=(12,12,9), filename=filename)
        elif width == 9:
            filename = os.path.join(os.path.dirname(__file__), 'schematics', 'wall', 'gate', 'gate_9.schematic')
            return MCSchematic(shape=(13,12,9), filename=filename)
    except Exception as e:
        logger.error(e)

def place_gates(level, box, heightmap, gate_pos_1, gate_pos_2, gate_pos_3, gate_pos_4, x_gate, z_gate):
    try:
        # TODO: place gates based on gate size
        gate_x = get_gate_schem(x_gate)
        gate_z = get_gate_schem(z_gate)
        gate_z.rotateLeft()

        # -z:
        level.copyBlocksFrom(gate_x, gate_x.bounds, gate_pos_1)
        # -x:
        level.copyBlocksFrom(gate_z, gate_z.bounds, gate_pos_2)

        # Rotate both walls by 180 deg
        gate_x.rotateLeft()
        gate_x.rotateLeft()
        gate_z.rotateLeft()
        gate_z.rotateLeft()

        # -z:
        level.copyBlocksFrom(gate_x, gate_x.bounds, gate_pos_3)
        # -x:
        level.copyBlocksFrom(gate_z, gate_z.bounds, gate_pos_4)


    except Exception as e:
        logger.error(e)

def place_gates_controls(level, box, position, gate_size):
    try:
        # TODO: Add gate controls 
        pass
    except Exception as e:
        logger.error(e)

def place_walls(level, box, heightmap):
    try:
        # TODO: place walls together
        x_left, x_right, x_gate, z_left, z_right, z_gate = calc_wall_sections(box) # calculate wall sections and gate sizes
        
        place_wall_corners(level, box, heightmap)
        gate_pos_1, gate_pos_2, gate_pos_3, gate_pos_4 = place_wall_sections(level, box, heightmap, x_left, x_right, z_left, z_right)
        place_gates(level, box, heightmap, gate_pos_1, gate_pos_2, gate_pos_3, gate_pos_4, x_gate, z_gate)

    except Exception as e:
        logger.error(e)