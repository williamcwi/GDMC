from logger import Logger

from pymclevel import MCSchematic
from pymclevel.box import Vector

from pymclevel import TAG_Compound, TAG_Int, TAG_Byte, TAG_String

import os.path

name = 'generateWalls'
logger = Logger(name)

def calc_wall_sections(box):
    try:
        # Calculates to total number of wall sections and gate sizes for each side
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

def place_wall_corners(level, box, heightmap, combinedHM):
    try:
        wall_type = 'corner'
        building = 'wall {}'.format(wall_type)
        progress = 0

        # +x -z:
        filename = os.path.join(os.path.dirname(__file__), 'schematics', 'wall', 'wall_{}.schematic'.format(wall_type))
        wall_corner = MCSchematic(shape=(8,12,8), filename=filename)
        ground = heightmap[len(heightmap)-1][0]
        if ground == -1:
            ground = combinedHM[len(heightmap)-1][0]
        level.copyBlocksFrom(wall_corner, wall_corner.bounds, Vector(box.maxx-8, ground, box.minz))
        progress += 1
        logger.info('Placing {}s... ({}/4)'.format(building, progress))

        # -x -z:
        wall_corner.rotateLeft()
        ground = heightmap[0][0]
        if ground == -1:
            ground = combinedHM[0][0]
        level.copyBlocksFrom(wall_corner, wall_corner.bounds, Vector(box.minx, ground, box.minz))
        progress += 1
        logger.info('Placing {}s... ({}/4)'.format(building, progress))

        # -x +z:
        wall_corner.rotateLeft()
        ground = heightmap[0][len(heightmap[0])-1]
        if ground == -1:
            ground = combinedHM[0][len(heightmap[0])-1]
        level.copyBlocksFrom(wall_corner, wall_corner.bounds, Vector(box.minx, ground, box.maxz-8))
        progress += 1
        logger.info('Placing {}s... ({}/4)'.format(building, progress))
        
        # +x +z:
        wall_corner.rotateLeft()
        ground = heightmap[len(heightmap)-1][len(heightmap[len(heightmap)-1])-1]
        if ground == -1:
            ground = combinedHM[len(heightmap)-1][len(heightmap[len(heightmap)-1])-1]
        level.copyBlocksFrom(wall_corner, wall_corner.bounds, Vector(box.maxx-8, ground, box.maxz-8))
        progress += 1
        logger.info('Placing {}s... ({}/4)'.format(building, progress))

        pass
    except Exception as e:
        logger.error(e)

def place_wall_sections(level, box, heightmap, combinedHM, x_left, x_right, z_left, z_right):
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

        wall_type = 'pillar' # wall_pillar (1x12x9)
        filename = os.path.join(os.path.dirname(__file__), 'schematics', 'wall', 'water_{}.schematic'.format(wall_type))
        water_pillar = MCSchematic(shape=(1,10,8), filename=filename)
        
        wall_type = 'left' # wall_left (1x11x8)
        filename = os.path.join(os.path.dirname(__file__), 'schematics', 'wall', 'water_{}.schematic'.format(wall_type))
        water_left = MCSchematic(shape=(1,9,8), filename=filename)

        wall_type = 'middle' # wall_middle (1x11x8)
        filename = os.path.join(os.path.dirname(__file__), 'schematics', 'wall', 'water_{}.schematic'.format(wall_type))
        water_middle = MCSchematic(shape=(1,9,8), filename=filename)

        wall_type = 'right' # wall_right (1x11x8)
        filename = os.path.join(os.path.dirname(__file__), 'schematics', 'wall', 'water_{}.schematic'.format(wall_type))
        water_right = MCSchematic(shape=(1,9,8), filename=filename)

        # TODO: Rotate wall_base 180 deg

        # -z:
        # left: 
        i = 1
        for sections in range(x_left):
            for wt in range(4): # wall type
                if wt == 0: #left
                    ground = heightmap[len(heightmap)-8-i][1]
                    if ground == -1:
                        ground = combinedHM[len(heightmap)-8-i][1]
                        level.copyBlocksFrom(water_left, water_left.bounds, Vector(box.maxx-8-i, ground+2, box.minz+1))
                    else: 
                        level.copyBlocksFrom(wall_left, wall_left.bounds, Vector(box.maxx-8-i, ground, box.minz+1))
                    i += 1
                elif wt == 1: # middle
                    ground = heightmap[len(heightmap)-8-i][1]
                    if ground == -1:
                        ground = combinedHM[len(heightmap)-8-i][1]
                        level.copyBlocksFrom(water_middle, water_middle.bounds, Vector(box.maxx-8-i, ground+2, box.minz+1))
                    else: 
                        level.copyBlocksFrom(wall_middle, wall_middle.bounds, Vector(box.maxx-8-i, ground, box.minz+1))
                    i += 1
                elif wt == 2: # right
                    if sections is not x_left - 1:
                        ground = heightmap[len(heightmap)-8-i][1]
                        if ground == -1:
                            ground = combinedHM[len(heightmap)-8-i][1]
                            level.copyBlocksFrom(water_right, water_right.bounds, Vector(box.maxx-8-i, ground+2, box.minz+1))
                        else: 
                            level.copyBlocksFrom(wall_right, wall_right.bounds, Vector(box.maxx-8-i, ground, box.minz+1))
                        i += 1
                elif wt == 3: # pillar
                    if sections is not x_left - 1:
                        ground = heightmap[len(heightmap)-8-i][1]
                        if ground == -1:
                            ground = combinedHM[len(heightmap)-8-i][1]
                            level.copyBlocksFrom(water_pillar, water_pillar.bounds, Vector(box.maxx-8-i, ground+2, box.minz))
                        else: 
                            level.copyBlocksFrom(wall_pillar, wall_pillar.bounds, Vector(box.maxx-8-i, ground, box.minz))
                        i += 1
            # TODO: Generate wall_base

        # right: 
        i = 1
        for sections in range(x_right):
            for wt in range(4): # wall type
                if wt == 0: # right
                    ground = heightmap[8+i][1]
                    if ground == -1:
                        ground = combinedHM[8+i][1]
                        level.copyBlocksFrom(water_right, water_right.bounds, Vector(box.minx+7+i, ground+2, box.minz+1))
                    else: 
                        level.copyBlocksFrom(wall_right, wall_right.bounds, Vector(box.minx+7+i, ground, box.minz+1))
                    i += 1
                elif wt == 1: # middle
                    ground = heightmap[8+i][1]
                    if ground == -1:
                        ground = combinedHM[8+i][1]
                        level.copyBlocksFrom(water_middle, water_middle.bounds, Vector(box.minx+7+i, ground+2, box.minz+1))
                    else: 
                        level.copyBlocksFrom(wall_middle, wall_middle.bounds, Vector(box.minx+7+i, ground, box.minz+1))
                    i += 1
                elif wt == 2: #left
                    if sections is not x_right - 1:
                        ground = heightmap[8+i][1]
                        if ground == -1:
                            ground = combinedHM[8+i][1]
                            level.copyBlocksFrom(water_left, water_left.bounds, Vector(box.minx+7+i, ground+2, box.minz+1))
                        else: 
                            level.copyBlocksFrom(wall_left, wall_left.bounds, Vector(box.minx+7+i, ground, box.minz+1))
                        i += 1
                    else: 
                        gate_pos_1 = [box.minx+7+i, ground, box.minz]
                elif wt == 3: # pillar
                    if sections is not x_right - 1:
                        ground = heightmap[8+i][1]
                        if ground == -1:
                            ground = combinedHM[8+i][1]
                            level.copyBlocksFrom(water_pillar, water_pillar.bounds, Vector(box.minx+7+i, ground+2, box.minz))
                        else: 
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
        water_pillar.rotateLeft()
        water_left.rotateLeft()
        water_middle.rotateLeft()
        water_right.rotateLeft()

        # -x:
        # left: 
        i = 1
        for sections in range(z_left):
            for wt in range(4): # wall type
                if wt == 0: #left
                    ground = heightmap[1][8+i]
                    if ground == -1:
                        ground = combinedHM[1][8+i]
                        level.copyBlocksFrom(water_left, water_left.bounds, Vector(box.minx+1, ground+2, box.minz+7+i))
                    else: 
                        level.copyBlocksFrom(wall_left, wall_left.bounds, Vector(box.minx+1, ground, box.minz+7+i))
                    i += 1
                elif wt == 1: # middle
                    ground = heightmap[1][8+i]
                    if ground == -1:
                        ground = combinedHM[1][8+i]
                        level.copyBlocksFrom(water_middle, water_middle.bounds, Vector(box.minx+1, ground+2, box.minz+7+i))
                    else: 
                        level.copyBlocksFrom(wall_middle, wall_middle.bounds, Vector(box.minx+1, ground, box.minz+7+i))
                    i += 1
                elif wt == 2: # right
                    if sections is not z_left - 1:
                        ground = heightmap[1][8+i]
                        if ground == -1:
                            ground = combinedHM[1][8+i]
                            level.copyBlocksFrom(water_right, water_right.bounds, Vector(box.minx+1, ground+2, box.minz+7+i))
                        else: 
                            level.copyBlocksFrom(wall_right, wall_right.bounds, Vector(box.minx+1, ground, box.minz+7+i))
                        i += 1
                    else: 
                        gate_pos_2 = [box.minx, ground, box.minz+7+i]
                elif wt == 3: # pillar
                    if sections is not z_left - 1:
                        ground = heightmap[1][8+i]
                        if ground == -1:
                            ground = combinedHM[1][8+i]
                            level.copyBlocksFrom(water_pillar, water_pillar.bounds, Vector(box.minx, ground+2, box.minz+7+i))
                        else: 
                            level.copyBlocksFrom(wall_pillar, wall_pillar.bounds, Vector(box.minx, ground, box.minz+7+i))
                        i += 1
            # TODO: Generate wall_base

        # right: 
        i = 1
        for sections in range(z_right):
            for wt in range(4): # wall type
                if wt == 0: # right
                    ground = heightmap[1][len(heightmap[1])-8-i]
                    if ground == -1:
                        ground = combinedHM[1][len(heightmap[1])-8-i]
                        level.copyBlocksFrom(water_right, water_right.bounds, Vector(box.minx+1, ground, box.maxz-8-i))
                    else: 
                        level.copyBlocksFrom(wall_right, wall_right.bounds, Vector(box.minx+1, ground, box.maxz-8-i))
                    i += 1
                elif wt == 1: # middle
                    ground = heightmap[1][len(heightmap[1])-8-i]
                    if ground == -1:
                        ground = combinedHM[1][len(heightmap[1])-8-i]
                        level.copyBlocksFrom(water_middle, water_middle.bounds, Vector(box.minx+1, ground, box.maxz-8-i))
                    else: 
                        level.copyBlocksFrom(wall_middle, wall_middle.bounds, Vector(box.minx+1, ground, box.maxz-8-i))
                    i += 1
                elif wt == 2: #left
                    if sections is not z_right - 1:
                        ground = heightmap[1][len(heightmap[1])-8-i]
                        if ground == -1:
                            ground = combinedHM[1][len(heightmap[1])-8-i]
                            level.copyBlocksFrom(water_left, water_left.bounds, Vector(box.minx+1, ground, box.maxz-8-i))
                        else: 
                            level.copyBlocksFrom(wall_left, wall_left.bounds, Vector(box.minx+1, ground, box.maxz-8-i))
                        i += 1
                elif wt == 3: # pillar
                    if sections is not z_right - 1:
                        ground = heightmap[1][len(heightmap[1])-8-i]
                        if ground == -1:
                            ground = combinedHM[1][len(heightmap[1])-8-i]
                            level.copyBlocksFrom(water_pillar, water_pillar.bounds, Vector(box.minx, ground, box.maxz-8-i))
                        else: 
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
        water_pillar.rotateLeft()
        water_left.rotateLeft()
        water_middle.rotateLeft()
        water_right.rotateLeft()

        # +z:
        # left: 
        i = 1
        for sections in range(x_left):
            for wt in range(4): # wall type
                if wt == 0: #left
                    ground = heightmap[len(heightmap)-8-i][len(heightmap[len(heightmap)-8-i])-2]
                    if ground == -1:
                        ground = combinedHM[len(heightmap)-8-i][len(heightmap[len(heightmap)-8-i])-2]
                        level.copyBlocksFrom(water_right, water_right.bounds, Vector(box.maxx-8-i, ground+2, box.maxz-9))
                    else: 
                        level.copyBlocksFrom(wall_right, wall_right.bounds, Vector(box.maxx-8-i, ground, box.maxz-9))
                    i += 1
                elif wt == 1: # middle
                    ground = heightmap[len(heightmap)-8-i][len(heightmap[len(heightmap)-8-i])-2]
                    if ground == -1:
                        ground = combinedHM[len(heightmap)-8-i][len(heightmap[len(heightmap)-8-i])-2]
                        level.copyBlocksFrom(water_middle, water_middle.bounds, Vector(box.maxx-8-i, ground+2, box.maxz-9))
                    else: 
                        level.copyBlocksFrom(wall_middle, wall_middle.bounds, Vector(box.maxx-8-i, ground, box.maxz-9))
                    i += 1
                elif wt == 2: # right
                    if sections is not x_left - 1:
                        ground = heightmap[len(heightmap)-8-i][len(heightmap[len(heightmap)-8-i])-2]
                        if ground == -1:
                            ground = combinedHM[len(heightmap)-8-i][len(heightmap[len(heightmap)-8-i])-2]
                            level.copyBlocksFrom(water_left, water_left.bounds, Vector(box.maxx-8-i, ground+2, box.maxz-9))
                        else: 
                            level.copyBlocksFrom(wall_left, wall_left.bounds, Vector(box.maxx-8-i, ground, box.maxz-9))
                        i += 1
                elif wt == 3: # pillar
                    if sections is not x_left - 1:
                        ground = heightmap[len(heightmap)-8-i][len(heightmap[len(heightmap)-8-i])-2]
                        if ground == -1:
                            ground = combinedHM[len(heightmap)-8-i][len(heightmap[len(heightmap)-8-i])-2]
                            level.copyBlocksFrom(water_pillar, water_pillar.bounds, Vector(box.maxx-8-i, ground+2, box.maxz-9))
                        else: 
                            level.copyBlocksFrom(wall_pillar, wall_pillar.bounds, Vector(box.maxx-8-i, ground, box.maxz-9))
                        i += 1
            # TODO: Generate wall_base

        # right: 
        i = 1
        for sections in range(x_right):
            for wt in range(4): # wall type
                if wt == 0: # right
                    ground = heightmap[8+i][len(heightmap[8+i])-2]
                    if ground == -1:
                        ground = combinedHM[8+i][len(heightmap[8+i])-2]
                        level.copyBlocksFrom(water_left, water_left.bounds, Vector(box.minx+7+i, ground+2, box.maxz-9))
                    else: 
                        level.copyBlocksFrom(wall_left, wall_left.bounds, Vector(box.minx+7+i, ground, box.maxz-9))
                    i += 1
                elif wt == 1: # middle
                    ground = heightmap[8+i][len(heightmap[8+i])-2]
                    if ground == -1:
                        ground = combinedHM[8+i][len(heightmap[8+i])-2]
                        level.copyBlocksFrom(water_middle, water_middle.bounds, Vector(box.minx+7+i, ground+2, box.maxz-9))
                    else: 
                        level.copyBlocksFrom(wall_middle, wall_middle.bounds, Vector(box.minx+7+i, ground, box.maxz-9))
                    i += 1
                elif wt == 2: #left
                    if sections is not x_right - 1:
                        ground = heightmap[8+i][len(heightmap[8+i])-2]
                        if ground == -1:
                            ground = combinedHM[8+i][len(heightmap[8+i])-2]
                            level.copyBlocksFrom(water_right, water_right.bounds, Vector(box.minx+7+i, ground+2, box.maxz-9))
                        else: 
                            level.copyBlocksFrom(wall_right, wall_right.bounds, Vector(box.minx+7+i, ground, box.maxz-9))
                        i += 1
                    else: 
                        gate_pos_3 = [box.minx+7+i, ground, box.maxz-9]
                elif wt == 3: # pillar
                    if sections is not x_right - 1:
                        ground = heightmap[8+i][len(heightmap[8+i])-2]
                        if ground == -1:
                            ground = combinedHM[8+i][len(heightmap[8+i])-2]
                            level.copyBlocksFrom(water_pillar, water_pillar.bounds, Vector(box.minx+7+i, ground+2, box.maxz-9))
                        else: 
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
        water_pillar.rotateLeft()
        water_left.rotateLeft()
        water_middle.rotateLeft()
        water_right.rotateLeft()

        # -x:
        # left: 
        i = 1
        for sections in range(z_left):
            for wt in range(4): # wall type
                if wt == 0: #left
                    ground = heightmap[len(heightmap)-2][8+i]
                    if ground == -1:
                        ground = combinedHM[len(heightmap)-2][8+i]
                        level.copyBlocksFrom(water_right, water_right.bounds, Vector(box.maxx-9, ground+2, box.minz+7+i))
                    else: 
                        level.copyBlocksFrom(wall_right, wall_right.bounds, Vector(box.maxx-9, ground, box.minz+7+i))
                    i += 1
                elif wt == 1: # middle
                    ground = heightmap[len(heightmap)-2][8+i]
                    if ground == -1:
                        ground = combinedHM[len(heightmap)-2][8+i]
                        level.copyBlocksFrom(water_middle, water_middle.bounds, Vector(box.maxx-9, ground+2, box.minz+7+i))
                    else: 
                        level.copyBlocksFrom(wall_middle, wall_middle.bounds, Vector(box.maxx-9, ground, box.minz+7+i))
                    i += 1
                elif wt == 2: # right
                    if sections is not z_left - 1:
                        ground = heightmap[len(heightmap)-2][8+i]
                        if ground == -1:
                            ground = combinedHM[len(heightmap)-2][8+i]
                            level.copyBlocksFrom(water_left, water_left.bounds, Vector(box.maxx-9, ground+2, box.minz+7+i))
                        else: 
                            level.copyBlocksFrom(wall_left, wall_left.bounds, Vector(box.maxx-9, ground, box.minz+7+i))
                        i += 1
                    else: 
                        gate_pos_4 = [box.maxx-9, ground, box.minz+7+i]
                elif wt == 3: # pillar
                    if sections is not z_left - 1:
                        ground = heightmap[len(heightmap)-2][8+i]
                        if ground == -1:
                            ground = combinedHM[len(heightmap)-2][8+i]
                            level.copyBlocksFrom(water_pillar, water_pillar.bounds, Vector(box.maxx-9, ground+2, box.minz+7+i))
                        else: 
                            level.copyBlocksFrom(wall_pillar, wall_pillar.bounds, Vector(box.maxx-9, ground, box.minz+7+i))
                        i += 1
            # TODO: Generate wall_base

        # right: 
        i = 1
        for sections in range(z_right):
            for wt in range(4): # wall type
                if wt == 0: # right
                    ground = heightmap[len(heightmap)-2][len(heightmap[len(heightmap)-2])-8-i]
                    if ground == -1:
                        ground = combinedHM[len(heightmap)-2][len(heightmap[len(heightmap)-2])-8-i]
                        level.copyBlocksFrom(water_left, water_left.bounds, Vector(box.maxx-9, ground+2, box.maxz-8-i))
                    else: 
                        level.copyBlocksFrom(wall_left, wall_left.bounds, Vector(box.maxx-9, ground, box.maxz-8-i))
                    i += 1
                elif wt == 1: # middle
                    ground = heightmap[len(heightmap)-2][len(heightmap[len(heightmap)-2])-8-i]
                    if ground == -1:
                        ground = combinedHM[len(heightmap)-2][len(heightmap[len(heightmap)-2])-8-i]
                        level.copyBlocksFrom(water_middle, water_middle.bounds, Vector(box.maxx-9, ground+2, box.maxz-8-i))
                    else: 
                        level.copyBlocksFrom(wall_middle, wall_middle.bounds, Vector(box.maxx-9, ground, box.maxz-8-i))
                    i += 1
                elif wt == 2: #left
                    if sections is not z_right - 1:
                        ground = heightmap[len(heightmap)-2][len(heightmap[len(heightmap)-2])-8-i]
                        if ground == -1:
                            ground = combinedHM[len(heightmap)-2][len(heightmap[len(heightmap)-2])-8-i]
                            level.copyBlocksFrom(water_right, water_right.bounds, Vector(box.maxx-9, ground+2, box.maxz-8-i))
                        else: 
                            level.copyBlocksFrom(wall_right, wall_right.bounds, Vector(box.maxx-9, ground, box.maxz-8-i))
                        i += 1
                elif wt == 3: # pillar
                    if sections is not z_right - 1:
                        ground = heightmap[len(heightmap)-2][len(heightmap[len(heightmap)-2])-8-i]
                        if ground == -1:
                            ground = combinedHM[len(heightmap)-2][len(heightmap[len(heightmap)-2])-8-i]
                            level.copyBlocksFrom(water_pillar, water_pillar.bounds, Vector(box.maxx-9, ground+2, box.maxz-8-i))
                        else: 
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
        building = 'gate'
        progress = 0

        gate_x = get_gate_schem(x_gate)
        gate_z = get_gate_schem(z_gate)
        gate_z.rotateLeft()

        # -z:
        level.copyBlocksFrom(gate_x, gate_x.bounds, Vector(gate_pos_1[0], gate_pos_1[1], gate_pos_1[2]))
        place_gates_controls(level, box, gate_pos_1, x_gate, 'north')
        place_gate_floor(level, box, gate_pos_1, x_gate, 'north')

        progress += 1
        logger.info('Placing {}s... ({}/4)'.format(building, progress))

        # -x:
        level.copyBlocksFrom(gate_z, gate_z.bounds, Vector(gate_pos_2[0], gate_pos_2[1], gate_pos_2[2]))
        place_gates_controls(level, box, gate_pos_2, z_gate, 'west')
        place_gate_floor(level, box, gate_pos_2, z_gate, 'west')
        
        progress += 1
        logger.info('Placing {}s... ({}/4)'.format(building, progress))
        
        # Rotate both walls by 180 deg
        gate_x.rotateLeft()
        gate_x.rotateLeft()
        gate_z.rotateLeft()
        gate_z.rotateLeft()

        # -z:
        level.copyBlocksFrom(gate_x, gate_x.bounds, Vector(gate_pos_3[0], gate_pos_3[1], gate_pos_3[2]))
        place_gates_controls(level, box, gate_pos_3, x_gate, 'south')
        place_gate_floor(level, box, gate_pos_3, x_gate, 'south')
        
        progress += 1
        logger.info('Placing {}s... ({}/4)'.format(building, progress))
        
        # -x:
        level.copyBlocksFrom(gate_z, gate_z.bounds, Vector(gate_pos_4[0], gate_pos_4[1], gate_pos_4[2]))
        place_gates_controls(level, box, gate_pos_4, z_gate, 'east')
        place_gate_floor(level, box, gate_pos_4, z_gate, 'east')
        
        progress += 1
        logger.info('Placing {}s... ({}/4)'.format(building, progress))
        

    except Exception as e:
        logger.error(e)

def place_gate_floor(level, box, pos, width, direction):
    try:
        filename = os.path.join(os.path.dirname(__file__), 'schematics', 'wall', 'gate', 'gate_floor.schematic')
        gate_floor = MCSchematic(shape=(1,1,5), filename=filename)

        x = pos[0]+2
        y = pos[1]-1
        z = pos[2]+2

        if direction == 'north' or direction == 'south':
            for w in range(width):
                level.copyBlocksFrom(gate_floor, gate_floor.bounds, Vector(x, y, z))
                x += 1

        elif direction == 'west' or direction == 'east':
            gate_floor.rotateLeft()
            for w in range(width):
                level.copyBlocksFrom(gate_floor, gate_floor.bounds, Vector(x, y, z))
                z += 1

    except Exception as e:
        logger.error(e)

def get_command(direction, gate_size, control_type):
    try:
        start_y = '~-1'
        end_y = '~4'
        if direction == 'north':
            start_z = '~-1'
            end_z = '~-1'
            if control_type == 'open':
                start_x = '~2'
                end_x = '~' + str(1 + gate_size)
                block = 'air'
            elif control_type == 'close':
                start_x = '~-2'
                end_x = '~' + str(-1 - gate_size)
                block = 'spruce_fence'
        elif direction == 'west':
            start_x = '~-1'
            end_x = '~-1'
            if control_type == 'open':
                start_z = '~-2'
                end_z = '~' + str(-1 - gate_size)
                block = 'air'
            elif control_type == 'close':
                start_z = '~2'
                end_z = '~' + str(1 + gate_size)
                block = 'spruce_fence'
        elif direction == 'south':
            start_z = '~1'
            end_z = '~1'
            if control_type == 'close':
                start_x = '~-2'
                end_x = '~' + str(-1 - gate_size)
                block = 'air'
            elif control_type == 'open':
                start_x = '~2'
                end_x = '~' + str(1 + gate_size)
                block = 'spruce_fence'
        elif direction == 'east':
            start_x = '~1'
            end_x = '~1'
            if control_type == 'close':
                start_z = '~2'
                end_z = '~' + str(1 + gate_size)
                block = 'air'
            elif control_type == 'open':
                start_z = '~-2'
                end_z = '~' + str(-1 - gate_size)
                block = 'spruce_fence'

        command = 'fill {} {} {} {} {} {} {}'.format(start_x, start_y, start_z, end_x, end_y, end_z, block)
        return command
    except Exception as e:
        logger.error(e)

def gate_control_tile_entity(level, box, x, y, z, gate_size, command):
    try:
        
        # Create Tile Entity
        command_block = TAG_Compound()
        command_block["conditionMet"] = TAG_Byte(0)
        command_block["auto"] = TAG_Byte(0)
        command_block["CustomName"] = TAG_String(u'@')
        command_block["powered"] = TAG_Byte(0)
        command_block["Command"] = TAG_String(u'{}'.format(command))
        command_block["x"] = TAG_Int(x)
        command_block["y"] = TAG_Int(y)
        command_block["z"] = TAG_Int(z)
        command_block["id"] = TAG_String(u'minecraft:command_block')
        command_block["SuccessCount"] = TAG_Int(0)
        command_block["TrackOutput"] = TAG_Byte(1)
        command_block["UpdateLastExecution"] = TAG_Byte(1)

        chunk = level.getChunk(x/16, z/16)

        chunk.TileEntities.append(command_block)
        chunk.dirty = True

    except Exception as e:
        logger.error(e)

def place_gates_controls(level, box, pos, gate_size, direction):
    try:
        # Find gate controls position
        if direction == 'north' or direction == 'south':
            gate_open_pos = [pos[0], pos[1]+1, pos[2]+4]
            gate_close_pos = [pos[0]+gate_size+3, pos[1]+1, pos[2]+4]
        elif direction == 'west' or direction == 'east':
            gate_open_pos = [pos[0]+4, pos[1]+1, pos[2]+gate_size+3]
            gate_close_pos = [pos[0]+4, pos[1]+1, pos[2]]

        # Generate Command Block
        level.setBlockAt(gate_open_pos[0], gate_open_pos[1], gate_open_pos[2], 137)
        level.setBlockAt(gate_close_pos[0], gate_close_pos[1], gate_close_pos[2], 137)

        command = get_command(direction, gate_size, 'open')
        gate_control_tile_entity(level, box, gate_open_pos[0], gate_open_pos[1], gate_open_pos[2], gate_size, command)
        command = get_command(direction, gate_size, 'close')
        gate_control_tile_entity(level, box, gate_close_pos[0], gate_close_pos[1], gate_close_pos[2], gate_size, command)

    except Exception as e:
        logger.error(e)

def place_walls(level, box, heightmap, combinedHM):
    try:
        
        x_left, x_right, x_gate, z_left, z_right, z_gate = calc_wall_sections(box) # calculate wall sections and gate sizes
        
        place_wall_corners(level, box, heightmap, combinedHM)
        gate_pos_1, gate_pos_2, gate_pos_3, gate_pos_4 = place_wall_sections(level, box, heightmap, combinedHM, x_left, x_right, z_left, z_right)
        place_gates(level, box, heightmap, gate_pos_1, gate_pos_2, gate_pos_3, gate_pos_4, x_gate, z_gate)

        logger.info('Wall generation completed.')

    except Exception as e:
        logger.error(e)