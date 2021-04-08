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

def calc_ma(box):
    try:
        x_len = box.size[0]
        z_len = box.size[2]

        percentage = 0.1

        xma = int(round(x_len * 0.1, 0))
        zma = int(round(z_len * 0.1, 0))

        return xma, zma
    except Exception as e:
        logger.error(e)

def average(arr):
    try:
        return int(round(sum(arr)/len(arr), 0))
    except Exception as e:
        logger.error(e)

def removeBlocks(level, box, type, coord):
    if type == 'corner':
        minx = coord[0]
        maxx = coord[0] + 8
        minz = coord[2]
        maxz = coord[2] + 8
        miny = coord[1] + 12
    
        for x in xrange(minx, maxx):
            for z in xrange(minz, maxz):
                for y in xrange(miny, box.maxy):
                    level.setBlockAt(x, y, z, 0)

    elif type == 'pillar_z' or type == 'section_z' or type == 'water_pillar_z' or type == 'water_section_z':
        if type == 'pillar_z':
            minx = coord[0]
            minz = coord[2]
            maxz = coord[2] + 9
            miny = coord[1] + 12
        elif type == 'section_z':
            minx = coord[0]
            minz = coord[2]
            maxz = coord[2] + 8
            miny = coord[1] + 11
        elif type == 'water_pillar_z':
            minx = coord[0]
            minz = coord[2]
            maxz = coord[2] + 8
            miny = coord[1] + 10
        elif type == 'water_section_z':
            minx = coord[0]
            minz = coord[2]
            maxz = coord[2] + 8
            miny = coord[1] + 9

        for z in xrange(minz, maxz):
            for y in xrange(miny, box.maxy):
                level.setBlockAt(minx, y, z, 0)

    elif type == 'pillar_x' or type == 'section_x' or type == 'water_pillar_x' or type == 'water_section_x':
        if type == 'pillar_x':
            minx = coord[0]
            maxx = coord[0] + 9
            minz = coord[2]
            miny = coord[1] + 12
        elif type == 'section_x':
            minx = coord[0]
            maxx = coord[0] + 8
            minz = coord[2]
            miny = coord[1] + 11
        elif type == 'water_pillar_x':
            minx = coord[0]
            maxx = coord[0] + 8
            minz = coord[2]
            miny = coord[1] + 10
        elif type == 'water_section_x':
            minx = coord[0]
            maxx = coord[0] + 8
            minz = coord[2]
            miny = coord[1] + 9

        for x in xrange(minx, maxx):
            for y in xrange(miny, box.maxy):
                level.setBlockAt(x, y, minz, 0)


def place_wall_corners(level, box, heightmap, combinedHM):
    try:
        wall_type = 'corner'
        building = 'wall {}'.format(wall_type)
        progress = 0

        xma, zma = calc_ma(box)

        corner_ground = []

        # +x -z:
        filename = os.path.join(os.path.dirname(__file__), 'schematics', 'wall', 'wall_{}.schematic'.format(wall_type))
        wall_corner = MCSchematic(shape=(8,12,8), filename=filename)
        arr = []
        for i in range(xma + 8):
            if heightmap[len(heightmap)-1-i][0] == -1:
                arr.append(combinedHM[len(heightmap)-1-i][0])
            else: 
                arr.append(heightmap[len(heightmap)-1-i][0])
        for i in range(zma + 8):
            if heightmap[len(heightmap)-1][i] == -1:
                arr.append(combinedHM[len(heightmap)-1][i])
            else:
                arr.append(heightmap[len(heightmap)-1][i])
        ground = average(arr)
        level.copyBlocksFrom(wall_corner, wall_corner.bounds, Vector(box.maxx-8, ground, box.minz))
        corner_ground.append(ground)
        removeBlocks(level, box, 'corner', [box.maxx-8, ground, box.minz])
        progress += 1
        logger.info('Placing {}s... ({}/4)'.format(building, progress))

        # -x -z:
        wall_corner.rotateLeft()
        arr = []
        for i in range(xma + 8):
            if heightmap[i][0] == -1:
                arr.append(combinedHM[i][0])
            else: 
                arr.append(heightmap[i][0])
        for i in range(zma + 8):
            if heightmap[0][i] == -1:
                arr.append(combinedHM[0][i])
            else:
                arr.append(heightmap[0][i])
        ground = average(arr)
        level.copyBlocksFrom(wall_corner, wall_corner.bounds, Vector(box.minx, ground, box.minz))
        corner_ground.append(ground)
        removeBlocks(level, box, 'corner', [box.minx, ground, box.minz])
        progress += 1
        logger.info('Placing {}s... ({}/4)'.format(building, progress))

        # -x +z:
        wall_corner.rotateLeft()
        arr = []
        for i in range(xma + 8):
            if heightmap[i][len(heightmap[0])-1] == -1:
                arr.append(combinedHM[i][len(combinedHM[0])-1])
            else: 
                arr.append(heightmap[i][len(heightmap[0])-1])
        for i in range(zma + 8):
            if heightmap[0][len(heightmap[0])-1-i] == -1:
                arr.append(combinedHM[0][len(combinedHM[0])-1-i])
            else:
                arr.append(heightmap[0][len(heightmap[0])-1-i])
        ground = average(arr)
        level.copyBlocksFrom(wall_corner, wall_corner.bounds, Vector(box.minx, ground, box.maxz-8))
        corner_ground.append(ground)
        removeBlocks(level, box, 'corner', [box.minx, ground, box.maxz-8])
        progress += 1
        logger.info('Placing {}s... ({}/4)'.format(building, progress))
        
        # +x +z:
        wall_corner.rotateLeft()
        arr = []
        for i in range(xma + 8):
            if heightmap[len(heightmap)-1-i][len(heightmap[len(heightmap)-1])-1] == -1:
                arr.append(combinedHM[len(heightmap)-1-i][len(heightmap[len(heightmap)-1])-1])
            else: 
                arr.append(heightmap[len(heightmap)-1-i][len(heightmap[len(heightmap)-1])-1])
        for i in range(zma + 8):
            if heightmap[len(heightmap)-1][len(heightmap[len(heightmap)-1])-1-i] == -1:
                arr.append(combinedHM[len(heightmap)-1][len(heightmap[len(heightmap)-1])-1-i])
            else:
                arr.append(heightmap[len(heightmap)-1][len(heightmap[len(heightmap)-1])-1-i])
        ground = average(arr)
        level.copyBlocksFrom(wall_corner, wall_corner.bounds, Vector(box.maxx-8, ground, box.maxz-8))
        corner_ground.append(ground)
        removeBlocks(level, box, 'corner', [box.maxx-8, ground, box.maxz-8])
        progress += 1
        logger.info('Placing {}s... ({}/4)'.format(building, progress))

        return corner_ground
    except Exception as e:
        logger.error(e)

def place_wall_sections(level, box, heightmap, combinedHM, x_left, x_right, z_left, z_right, x_gate, z_gate):
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

        xma, zma = calc_ma(box)

        # -z:
        # left: 
        i = 1
        for sections in range(x_left):
            for wt in range(4): # wall type
                arr = []
                for index in range(xma):
                    if heightmap[len(heightmap)-8-i-index][1] == -1:
                        arr.append(combinedHM[len(heightmap)-8-i-index][1])
                    else: 
                        arr.append(heightmap[len(heightmap)-8-i-index][1])
                for index in range(8):
                    if heightmap[len(heightmap)-8-i+index][1] == -1:
                        arr.append(combinedHM[len(heightmap)-8-i+index][1])
                    else: 
                        arr.append(heightmap[len(heightmap)-8-i+index][1])
                ground = average(arr)

                if wt == 0: #left
                    if heightmap[len(heightmap)-8-i][1] == -1:
                        level.copyBlocksFrom(water_left, water_left.bounds, Vector(box.maxx-8-i, ground+2, box.minz+1))
                        removeBlocks(level, box, 'water_section_z', [box.maxx-8-i, ground+2, box.minz+1])
                    else: 
                        level.copyBlocksFrom(wall_left, wall_left.bounds, Vector(box.maxx-8-i, ground, box.minz+1))
                        removeBlocks(level, box, 'section_z', [box.maxx-8-i, ground, box.minz+1])
                    i += 1
                elif wt == 1: # middle
                    if heightmap[len(heightmap)-8-i][1] == -1:
                        level.copyBlocksFrom(water_middle, water_middle.bounds, Vector(box.maxx-8-i, ground+2, box.minz+1))
                        removeBlocks(level, box, 'water_section_z', [box.maxx-8-i, ground+2, box.minz+1])
                    else: 
                        level.copyBlocksFrom(wall_middle, wall_middle.bounds, Vector(box.maxx-8-i, ground, box.minz+1))
                        removeBlocks(level, box, 'section_z', [box.maxx-8-i, ground, box.minz+1])
                    i += 1
                elif wt == 2: # right
                    if sections is not x_left - 1:
                        if heightmap[len(heightmap)-8-i][1] == -1:
                            level.copyBlocksFrom(water_right, water_right.bounds, Vector(box.maxx-8-i, ground+2, box.minz+1))
                            removeBlocks(level, box, 'water_section_z', [box.maxx-8-i, ground+2, box.minz+1])
                        else: 
                            level.copyBlocksFrom(wall_right, wall_right.bounds, Vector(box.maxx-8-i, ground, box.minz+1))
                            removeBlocks(level, box, 'section_z', [box.maxx-8-i, ground, box.minz+1])
                        i += 1
                elif wt == 3: # pillar
                    if sections is not x_left - 1:
                        if heightmap[len(heightmap)-8-i][1] == -1:
                            level.copyBlocksFrom(water_pillar, water_pillar.bounds, Vector(box.maxx-8-i, ground+2, box.minz+1))
                            removeBlocks(level, box, 'water_pillar_z', [box.maxx-8-i, ground+2, box.minz+1])
                        else: 
                            level.copyBlocksFrom(wall_pillar, wall_pillar.bounds, Vector(box.maxx-8-i, ground, box.minz))
                            removeBlocks(level, box, 'pillar_z', [box.maxx-8-i, ground, box.minz])
                        i += 1

        # right: 
        i = 1
        for sections in range(x_right):
            for wt in range(4): # wall type
                arr = []
                for index in range(xma):
                    if heightmap[8+i+index][1] == -1:
                        arr.append(combinedHM[8+i+index][1])
                    else: 
                        arr.append(heightmap[8+i+index][1])
                for index in range(8):
                    if heightmap[8+i-index][1] == -1:
                        arr.append(combinedHM[8+i-index][1])
                    else: 
                        arr.append(heightmap[8+i-index][1])
                ground = average(arr)

                if wt == 0: # right
                    if heightmap[8+i][1] == -1:
                        level.copyBlocksFrom(water_right, water_right.bounds, Vector(box.minx+7+i, ground+2, box.minz+1))
                        removeBlocks(level, box, 'water_section_z', [box.minx+7+i, ground+2, box.minz+1])
                    else: 
                        level.copyBlocksFrom(wall_right, wall_right.bounds, Vector(box.minx+7+i, ground, box.minz+1))
                        removeBlocks(level, box, 'section_z', [box.minx+7+i, ground, box.minz+1])
                    i += 1
                elif wt == 1: # middle
                    if heightmap[8+i][1] == -1:
                        level.copyBlocksFrom(water_middle, water_middle.bounds, Vector(box.minx+7+i, ground+2, box.minz+1))
                        removeBlocks(level, box, 'water_section_z', [box.minx+7+i, ground+2, box.minz+1])
                    else: 
                        level.copyBlocksFrom(wall_middle, wall_middle.bounds, Vector(box.minx+7+i, ground, box.minz+1))
                        removeBlocks(level, box, 'section_z', [box.minx+7+i, ground, box.minz+1])
                    i += 1
                elif wt == 2: #left
                    if sections is not x_right - 1:
                        if heightmap[8+i][1] == -1:
                            level.copyBlocksFrom(water_left, water_left.bounds, Vector(box.minx+7+i, ground+2, box.minz+1))
                            removeBlocks(level, box, 'water_section_z', [box.minx+7+i, ground+2, box.minz+1])
                        else: 
                            level.copyBlocksFrom(wall_left, wall_left.bounds, Vector(box.minx+7+i, ground, box.minz+1))
                            removeBlocks(level, box, 'section_z', [box.minx+7+i, ground, box.minz+1])
                        i += 1
                    else: 
                        arr = []
                        for temp_left in range(xma + x_gate):
                            if heightmap[8+i+temp_left][1] == -1:
                                arr.append(combinedHM[8+i+temp_left][1])
                            else: 
                                arr.append(heightmap[8+i+temp_left][1])
                        for temp_right in range(xma):
                            if heightmap[8+i-temp_right][1] == -1:
                                arr.append(combinedHM[8+i-temp_right][1])
                            else: 
                                arr.append(heightmap[8+i-temp_right][1])
                        ground = average(arr)
                        gate_pos_1 = [box.minx+7+i, ground, box.minz]
                elif wt == 3: # pillar
                    if sections is not x_right - 1:
                        if heightmap[8+i][1] == -1:
                            level.copyBlocksFrom(water_pillar, water_pillar.bounds, Vector(box.minx+7+i, ground+2, box.minz+1))
                            removeBlocks(level, box, 'water_pillar_z', [box.minx+7+i, ground+2, box.minz+1])
                        else: 
                            level.copyBlocksFrom(wall_pillar, wall_pillar.bounds, Vector(box.minx+7+i, ground, box.minz))
                            removeBlocks(level, box, 'pillar_z', [box.minx+7+i, ground, box.minz])
                        i += 1
        progress += 1

        logger.info('Placing {}s... ({}/4)'.format(building, progress))

        wall_pillar.rotateLeft()
        wall_left.rotateLeft()
        wall_middle.rotateLeft()
        wall_right.rotateLeft()
        water_pillar.rotateLeft()
        water_left.rotateLeft()
        water_middle.rotateLeft()
        water_right.rotateLeft()

        # -x:
        # left: 
        i = 1
        for sections in range(z_left):
            for wt in range(4): # wall type
                arr = []
                for index in range(zma):
                    if heightmap[1][8+i+index] == -1:
                        arr.append(combinedHM[1][8+i+index])
                    else: 
                        arr.append(heightmap[1][8+i+index])
                for index in range(8):
                    if heightmap[1][8+i-index] == -1:
                        arr.append(combinedHM[1][8+i-index])
                    else: 
                        arr.append(heightmap[1][8+i-index])
                ground = average(arr)
                if wt == 0: #left
                    if heightmap[1][8+i] == -1:
                        level.copyBlocksFrom(water_left, water_left.bounds, Vector(box.minx+1, ground+2, box.minz+7+i))
                        removeBlocks(level, box, 'water_section_x', [box.minx+1, ground+2, box.minz+7+i])
                    else: 
                        level.copyBlocksFrom(wall_left, wall_left.bounds, Vector(box.minx+1, ground, box.minz+7+i))
                        removeBlocks(level, box, 'section_x', [box.minx+1, ground, box.minz+7+i])
                    i += 1
                elif wt == 1: # middle
                    if heightmap[1][8+i] == -1:
                        level.copyBlocksFrom(water_middle, water_middle.bounds, Vector(box.minx+1, ground+2, box.minz+7+i))
                        removeBlocks(level, box, 'water_section_x', [box.minx+1, ground+2, box.minz+7+i])
                    else: 
                        level.copyBlocksFrom(wall_middle, wall_middle.bounds, Vector(box.minx+1, ground, box.minz+7+i))
                        removeBlocks(level, box, 'section_x', [box.minx+1, ground, box.minz+7+i])
                    i += 1
                elif wt == 2: # right
                    if sections is not z_left - 1:
                        if heightmap[1][8+i] == -1:
                            level.copyBlocksFrom(water_right, water_right.bounds, Vector(box.minx+1, ground+2, box.minz+7+i))
                            removeBlocks(level, box, 'water_section_x', [box.minx+1, ground+2, box.minz+7+i])
                        else: 
                            level.copyBlocksFrom(wall_right, wall_right.bounds, Vector(box.minx+1, ground, box.minz+7+i))
                            removeBlocks(level, box, 'section_x', [box.minx+1, ground, box.minz+7+i])
                        i += 1
                    else: 
                        arr = []
                        for temp_left in range(zma):
                            if heightmap[1][8+i-temp_left] == -1:
                                arr.append(combinedHM[1][8+i-temp_left])
                            else: 
                                arr.append(heightmap[1][8+i-temp_left])
                        for temp_right in range(zma + z_gate):
                            if heightmap[1][8+i+temp_right] == -1:
                                arr.append(combinedHM[1][8+i+temp_right])
                            else: 
                                arr.append(heightmap[1][8+i+temp_right])
                        ground = average(arr)
                        gate_pos_2 = [box.minx, ground, box.minz+7+i]
                elif wt == 3: # pillar
                    if sections is not z_left - 1:
                        if heightmap[1][8+i] == -1:
                            level.copyBlocksFrom(water_pillar, water_pillar.bounds, Vector(box.minx+1, ground+2, box.minz+7+i))
                            removeBlocks(level, box, 'water_pillar_x', [box.minx+1, ground+2, box.minz+7+i])
                        else: 
                            level.copyBlocksFrom(wall_pillar, wall_pillar.bounds, Vector(box.minx, ground, box.minz+7+i))
                            removeBlocks(level, box, 'pillar_x', [box.minx, ground, box.minz+7+i])
                        i += 1

        # right: 
        i = 1
        for sections in range(z_right):
            for wt in range(4): # wall type
                arr = []
                for index in range(zma):
                    if heightmap[1][len(heightmap[1])-8-i-index] == -1:
                        arr.append(combinedHM[1][len(heightmap[1])-8-i-index])
                    else: 
                        arr.append(heightmap[1][len(heightmap[1])-8-i-index])
                for index in range(8):
                    if heightmap[1][len(heightmap[1])-8-i+index] == -1:
                        arr.append(combinedHM[1][len(heightmap[1])-8-i+index])
                    else: 
                        arr.append(heightmap[1][len(heightmap[1])-8-i+index])
                ground = average(arr)
                if wt == 0: # right
                    if heightmap[1][len(heightmap[1])-8-i] == -1:
                        level.copyBlocksFrom(water_right, water_right.bounds, Vector(box.minx+1, ground+2, box.maxz-8-i))
                        removeBlocks(level, box, 'water_section_x', [box.minx+1, ground+2, box.maxz-8-i])
                    else: 
                        level.copyBlocksFrom(wall_right, wall_right.bounds, Vector(box.minx+1, ground, box.maxz-8-i))
                        removeBlocks(level, box, 'section_x', [box.minx+1, ground, box.maxz-8-i])
                    i += 1
                elif wt == 1: # middle
                    if heightmap[1][len(heightmap[1])-8-i] == -1:
                        level.copyBlocksFrom(water_middle, water_middle.bounds, Vector(box.minx+1, ground+2, box.maxz-8-i))
                        removeBlocks(level, box, 'water_section_x', [box.minx+1, ground+2, box.maxz-8-i])
                    else: 
                        level.copyBlocksFrom(wall_middle, wall_middle.bounds, Vector(box.minx+1, ground, box.maxz-8-i))
                        removeBlocks(level, box, 'section_x', [box.minx+1, ground, box.maxz-8-i])
                    i += 1
                elif wt == 2: #left
                    if sections is not z_right - 1:
                        if heightmap[1][len(heightmap[1])-8-i] == -1:
                            level.copyBlocksFrom(water_left, water_left.bounds, Vector(box.minx+1, ground+2, box.maxz-8-i))
                            removeBlocks(level, box, 'water_section_x', [box.minx+1, ground+2, box.maxz-8-i])
                        else: 
                            level.copyBlocksFrom(wall_left, wall_left.bounds, Vector(box.minx+1, ground, box.maxz-8-i))
                            removeBlocks(level, box, 'section_x', [box.minx+1, ground, box.maxz-8-i])
                        i += 1
                elif wt == 3: # pillar
                    if sections is not z_right - 1:
                        if heightmap[1][len(heightmap[1])-8-i] == -1:
                            level.copyBlocksFrom(water_pillar, water_pillar.bounds, Vector(box.minx+1, ground+2, box.maxz-8-i))
                            removeBlocks(level, box, 'water_pillar_x', [box.minx+1, ground+2, box.maxz-8-i])
                        else: 
                            level.copyBlocksFrom(wall_pillar, wall_pillar.bounds, Vector(box.minx, ground, box.maxz-8-i))
                            removeBlocks(level, box, 'pillar_x', [box.minx, ground, box.maxz-8-i])
                        i += 1
        progress += 1

        logger.info('Placing {}s... ({}/4)'.format(building, progress))

        wall_pillar.rotateLeft()
        wall_left.rotateLeft()
        wall_middle.rotateLeft()
        wall_right.rotateLeft()
        water_pillar.rotateLeft()
        water_left.rotateLeft()
        water_middle.rotateLeft()
        water_right.rotateLeft()

        # +z:
        # left: 
        i = 1
        for sections in range(x_left):
            for wt in range(4): # wall type
                arr = []
                for index in range(xma):
                    if heightmap[len(heightmap)-8-i-index][len(heightmap[len(heightmap)-8-i-index])-2] == -1:
                        arr.append(combinedHM[len(heightmap)-8-i-index][len(heightmap[len(heightmap)-8-i-index])-2])
                    else: 
                        arr.append(heightmap[len(heightmap)-8-i-index][len(heightmap[len(heightmap)-8-i-index])-2])
                for index in range(8):
                    if heightmap[len(heightmap)-8-i+index][len(heightmap[len(heightmap)-8-i+index])-2] == -1:
                        arr.append(combinedHM[len(heightmap)-8-i+index][len(heightmap[len(heightmap)-8-i+index])-2])
                    else: 
                        arr.append(heightmap[len(heightmap)-8-i+index][len(heightmap[len(heightmap)-8-i+index])-2])
                ground = average(arr)
                if wt == 0: #left
                    if heightmap[len(heightmap)-8-i][len(heightmap[len(heightmap)-8-i])-2] == -1:
                        level.copyBlocksFrom(water_right, water_right.bounds, Vector(box.maxx-8-i, ground+2, box.maxz-9))
                        removeBlocks(level, box, 'water_section_z', [box.maxx-8-i, ground+2, box.maxz-9])
                    else: 
                        level.copyBlocksFrom(wall_right, wall_right.bounds, Vector(box.maxx-8-i, ground, box.maxz-9))
                        removeBlocks(level, box, 'section_z', [box.maxx-8-i, ground, box.maxz-9])
                    i += 1
                elif wt == 1: # middle
                    if heightmap[len(heightmap)-8-i][len(heightmap[len(heightmap)-8-i])-2] == -1:
                        level.copyBlocksFrom(water_middle, water_middle.bounds, Vector(box.maxx-8-i, ground+2, box.maxz-9))
                        removeBlocks(level, box, 'water_section_z', [box.maxx-8-i, ground+2, box.maxz-9])
                    else: 
                        level.copyBlocksFrom(wall_middle, wall_middle.bounds, Vector(box.maxx-8-i, ground, box.maxz-9))
                        removeBlocks(level, box, 'section_z', [box.maxx-8-i, ground, box.maxz-9])
                    i += 1
                elif wt == 2: # right
                    if sections is not x_left - 1:
                        if heightmap[len(heightmap)-8-i][len(heightmap[len(heightmap)-8-i])-2] == -1:
                            level.copyBlocksFrom(water_left, water_left.bounds, Vector(box.maxx-8-i, ground+2, box.maxz-9))
                            removeBlocks(level, box, 'water_section_z', [box.maxx-8-i, ground+2, box.maxz-9])
                        else: 
                            level.copyBlocksFrom(wall_left, wall_left.bounds, Vector(box.maxx-8-i, ground, box.maxz-9))
                            removeBlocks(level, box, 'section_z', [box.maxx-8-i, ground, box.maxz-9])
                        i += 1
                elif wt == 3: # pillar
                    if sections is not x_left - 1:
                        if heightmap[len(heightmap)-8-i][len(heightmap[len(heightmap)-8-i])-2] == -1:
                            level.copyBlocksFrom(water_pillar, water_pillar.bounds, Vector(box.maxx-8-i, ground+2, box.maxz-9))
                            removeBlocks(level, box, 'water_pillar_z', [box.maxx-8-i, ground+2, box.maxz-9])
                        else: 
                            level.copyBlocksFrom(wall_pillar, wall_pillar.bounds, Vector(box.maxx-8-i, ground, box.maxz-9))
                            removeBlocks(level, box, 'pillar_z', [box.maxx-8-i, ground, box.maxz-9])
                        i += 1

        # right: 
        i = 1
        for sections in range(x_right):
            for wt in range(4): # wall type
                arr = []
                for index in range(xma):
                    if heightmap[8+i+index][len(heightmap[8+i+index])-2] == -1:
                        arr.append(combinedHM[8+i+index][len(heightmap[8+i+index])-2])
                    else: 
                        arr.append(heightmap[8+i+index][len(heightmap[8+i+index])-2])
                for index in range(8):
                    if heightmap[8+i-index][len(heightmap[8+i-index])-2] == -1:
                        arr.append(combinedHM[8+i-index][len(heightmap[8+i-index])-2])
                    else: 
                        arr.append(heightmap[8+i-index][len(heightmap[8+i-index])-2])
                ground = average(arr)
                if wt == 0: # right
                    if heightmap[8+i][len(heightmap[8+i])-2] == -1:
                        level.copyBlocksFrom(water_left, water_left.bounds, Vector(box.minx+7+i, ground+2, box.maxz-9))
                        removeBlocks(level, box, 'water_section_z', [box.minx+7+i, ground+2, box.maxz-9])
                    else: 
                        level.copyBlocksFrom(wall_left, wall_left.bounds, Vector(box.minx+7+i, ground, box.maxz-9))
                        removeBlocks(level, box, 'section_z', [box.minx+7+i, ground, box.maxz-9])
                    i += 1
                elif wt == 1: # middle
                    if heightmap[8+i][len(heightmap[8+i])-2] == -1:
                        level.copyBlocksFrom(water_middle, water_middle.bounds, Vector(box.minx+7+i, ground+2, box.maxz-9))
                        removeBlocks(level, box, 'water_section_z', [box.minx+7+i, ground+2, box.maxz-9])
                    else: 
                        level.copyBlocksFrom(wall_middle, wall_middle.bounds, Vector(box.minx+7+i, ground, box.maxz-9))
                        removeBlocks(level, box, 'section_z', [box.minx+7+i, ground, box.maxz-9])
                    i += 1
                elif wt == 2: #left
                    if sections is not x_right - 1:
                        if heightmap[8+i][len(heightmap[8+i])-2] == -1:
                            level.copyBlocksFrom(water_right, water_right.bounds, Vector(box.minx+7+i, ground+2, box.maxz-9))
                            removeBlocks(level, box, 'water_section_z', [box.minx+7+i, ground+2, box.maxz-9])
                        else: 
                            level.copyBlocksFrom(wall_right, wall_right.bounds, Vector(box.minx+7+i, ground, box.maxz-9))
                            removeBlocks(level, box, 'section_z', [box.minx+7+i, ground, box.maxz-9])
                        i += 1
                    else: 
                        arr = []
                        for temp_left in range(xma + x_gate):
                            if heightmap[8+i+temp_left][len(heightmap[8+i+temp_left])-2] == -1:
                                arr.append(combinedHM[8+i+temp_left][len(heightmap[8+i+temp_left])-2])
                            else: 
                                arr.append(heightmap[8+i+temp_left][len(heightmap[8+i+temp_left])-2])
                        for temp_right in range(xma):
                            if heightmap[8+i-temp_right][len(heightmap[8+i-temp_right])-2] == -1:
                                arr.append(combinedHM[8+i-temp_right][len(heightmap[8+i-temp_right])-2])
                            else: 
                                arr.append(heightmap[8+i-temp_right][len(heightmap[8+i-temp_right])-2])
                        ground = average(arr)
                        gate_pos_3 = [box.minx+7+i, ground, box.maxz-9]
                elif wt == 3: # pillar
                    if sections is not x_right - 1:
                        if heightmap[8+i][len(heightmap[8+i])-2] == -1:
                            level.copyBlocksFrom(water_pillar, water_pillar.bounds, Vector(box.minx+7+i, ground+2, box.maxz-9))
                            removeBlocks(level, box, 'water_pillar_z', [box.minx+7+i, ground+2, box.maxz-9])
                        else: 
                            level.copyBlocksFrom(wall_pillar, wall_pillar.bounds, Vector(box.minx+7+i, ground, box.maxz-9))
                            removeBlocks(level, box, 'pillar_z', [box.minx+7+i, ground, box.maxz-9])
                        i += 1
        progress += 1

        logger.info('Placing {}s... ({}/4)'.format(building, progress))

        wall_pillar.rotateLeft()
        wall_left.rotateLeft()
        wall_middle.rotateLeft()
        wall_right.rotateLeft()
        water_pillar.rotateLeft()
        water_left.rotateLeft()
        water_middle.rotateLeft()
        water_right.rotateLeft()

        # +x:
        # left: 
        i = 1
        for sections in range(z_left):
            for wt in range(4): # wall type
                arr = []
                for index in range(zma):
                    if heightmap[len(heightmap)-2][8+i+index] == -1:
                        arr.append(combinedHM[len(heightmap)-2][8+i+index])
                    else: 
                        arr.append(heightmap[len(heightmap)-2][8+i+index])
                for index in range(8):
                    if heightmap[len(heightmap)-2][8+i-index] == -1:
                        arr.append(combinedHM[len(heightmap)-2][8+i-index])
                    else: 
                        arr.append(heightmap[len(heightmap)-2][8+i-index])
                ground = average(arr)
                if wt == 0: #left
                    if heightmap[len(heightmap)-2][8+i] == -1:
                        level.copyBlocksFrom(water_right, water_right.bounds, Vector(box.maxx-9, ground+2, box.minz+7+i))
                        removeBlocks(level, box, 'water_section_x', [box.maxx-9, ground+2, box.minz+7+i])
                    else: 
                        level.copyBlocksFrom(wall_right, wall_right.bounds, Vector(box.maxx-9, ground, box.minz+7+i))
                        removeBlocks(level, box, 'section_x', [box.maxx-9, ground, box.minz+7+i])
                    i += 1
                elif wt == 1: # middle
                    if heightmap[len(heightmap)-2][8+i] == -1:
                        level.copyBlocksFrom(water_middle, water_middle.bounds, Vector(box.maxx-9, ground+2, box.minz+7+i))
                        removeBlocks(level, box, 'water_section_x', [box.maxx-9, ground+2, box.minz+7+i])
                    else: 
                        level.copyBlocksFrom(wall_middle, wall_middle.bounds, Vector(box.maxx-9, ground, box.minz+7+i))
                        removeBlocks(level, box, 'section_x', [box.maxx-9, ground, box.minz+7+i])
                    i += 1
                elif wt == 2: # right
                    if sections is not z_left - 1:
                        if heightmap[len(heightmap)-2][8+i] == -1:
                            level.copyBlocksFrom(water_left, water_left.bounds, Vector(box.maxx-9, ground+2, box.minz+7+i))
                            removeBlocks(level, box, 'water_section_x', [box.maxx-9, ground+2, box.minz+7+i])
                        else: 
                            level.copyBlocksFrom(wall_left, wall_left.bounds, Vector(box.maxx-9, ground, box.minz+7+i))
                            removeBlocks(level, box, 'section_x', [box.maxx-9, ground, box.minz+7+i])
                        i += 1
                    else: 
                        arr = []
                        for temp_left in range(zma):
                            if heightmap[len(heightmap)-2][8+i-temp_left] == -1:
                                arr.append(combinedHM[len(heightmap)-2][8+i-temp_left])
                            else: 
                                arr.append(heightmap[len(heightmap)-2][8+i-temp_left])
                        for temp_right in range(zma + z_gate):
                            if heightmap[len(heightmap)-2][8+i+temp_right] == -1:
                                arr.append(combinedHM[len(heightmap)-2][8+i+temp_right])
                            else: 
                                arr.append(heightmap[len(heightmap)-2][8+i+temp_right])
                        ground = average(arr)
                        gate_pos_4 = [box.maxx-9, ground, box.minz+7+i]
                elif wt == 3: # pillar
                    if sections is not z_left - 1:
                        if heightmap[len(heightmap)-2][8+i] == -1:
                            level.copyBlocksFrom(water_pillar, water_pillar.bounds, Vector(box.maxx-9, ground+2, box.minz+7+i))
                            removeBlocks(level, box, 'water_pillar_x', [box.maxx-9, ground+2, box.minz+7+i])
                        else: 
                            level.copyBlocksFrom(wall_pillar, wall_pillar.bounds, Vector(box.maxx-9, ground, box.minz+7+i))
                            removeBlocks(level, box, 'pillar_x', [box.maxx-9, ground, box.minz+7+i])
                        i += 1

        # right: 
        i = 1
        for sections in range(z_right):
            for wt in range(4): # wall type
                arr = []
                for index in range(zma):
                    if heightmap[len(heightmap)-2][len(heightmap[len(heightmap)-2])-8-i-index] == -1:
                        arr.append(combinedHM[len(heightmap)-2][len(heightmap[len(heightmap)-2])-8-i-index])
                    else: 
                        arr.append(heightmap[len(heightmap)-2][len(heightmap[len(heightmap)-2])-8-i-index])
                for index in range(8):
                    if heightmap[len(heightmap)-2][len(heightmap[len(heightmap)-2])-8-i+index] == -1:
                        arr.append(combinedHM[len(heightmap)-2][len(heightmap[len(heightmap)-2])-8-i+index])
                    else: 
                        arr.append(heightmap[len(heightmap)-2][len(heightmap[len(heightmap)-2])-8-i+index])
                ground = average(arr)
                if wt == 0: # right
                    if heightmap[len(heightmap)-2][len(heightmap[len(heightmap)-2])-8-i] == -1:
                        level.copyBlocksFrom(water_left, water_left.bounds, Vector(box.maxx-9, ground+2, box.maxz-8-i))
                        removeBlocks(level, box, 'water_section_x', [box.maxx-9, ground+2, box.maxz-8-i])
                    else: 
                        level.copyBlocksFrom(wall_left, wall_left.bounds, Vector(box.maxx-9, ground, box.maxz-8-i))
                        removeBlocks(level, box, 'section_x', [box.maxx-9, ground, box.maxz-8-i])
                    i += 1
                elif wt == 1: # middle
                    if heightmap[len(heightmap)-2][len(heightmap[len(heightmap)-2])-8-i] == -1:
                        level.copyBlocksFrom(water_middle, water_middle.bounds, Vector(box.maxx-9, ground+2, box.maxz-8-i))
                        removeBlocks(level, box, 'water_section_x', [box.maxx-9, ground+2, box.maxz-8-i])
                    else: 
                        level.copyBlocksFrom(wall_middle, wall_middle.bounds, Vector(box.maxx-9, ground, box.maxz-8-i))
                        removeBlocks(level, box, 'section_x', [box.maxx-9, ground, box.maxz-8-i])
                    i += 1
                elif wt == 2: #left
                    if sections is not z_right - 1:
                        if heightmap[len(heightmap)-2][len(heightmap[len(heightmap)-2])-8-i] == -1:
                            level.copyBlocksFrom(water_right, water_right.bounds, Vector(box.maxx-9, ground+2, box.maxz-8-i))
                            removeBlocks(level, box, 'water_section_x', [box.maxx-9, ground+2, box.maxz-8-i])
                        else: 
                            level.copyBlocksFrom(wall_right, wall_right.bounds, Vector(box.maxx-9, ground, box.maxz-8-i))
                            removeBlocks(level, box, 'section_x', [box.maxx-9, ground, box.maxz-8-i])
                        i += 1
                elif wt == 3: # pillar
                    if sections is not z_right - 1:
                        if heightmap[len(heightmap)-2][len(heightmap[len(heightmap)-2])-8-i] == -1:
                            level.copyBlocksFrom(water_pillar, water_pillar.bounds, Vector(box.maxx-9, ground+2, box.maxz-8-i))
                            removeBlocks(level, box, 'water_section_x', [box.maxx-9, ground+2, box.maxz-8-i])
                        else: 
                            level.copyBlocksFrom(wall_pillar, wall_pillar.bounds, Vector(box.maxx-9, ground, box.maxz-8-i))
                            removeBlocks(level, box, 'section_x', [box.maxx-9, ground, box.maxz-8-i])
                        i += 1
        progress += 1

        logger.info('Placing {}s... ({}/4)'.format(building, progress))

        return gate_pos_1, gate_pos_2, gate_pos_3, gate_pos_4

    except Exception as e:
        logger.error(e)

def get_gate_schem(width):
    try:
        if width >= 6 and width <= 9:
            filename = os.path.join(os.path.dirname(__file__), 'schematics', 'wall', 'gate', 'gate_'+ str(width) +'.schematic')
            return MCSchematic(shape=((width + 4),12,9), filename=filename)
        
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

def place_wall_base(level, box, heightmap, combinedHM, x_left, x_right, z_left, z_right, gate_pos_1, gate_pos_2, gate_pos_3, gate_pos_4, corner_ground):
    try:
        building = 'inner wall'
        progress = 0

        filename = os.path.join(os.path.dirname(__file__), 'schematics', 'wall', 'wall_base.schematic')
        wall_base = MCSchematic(shape=(5,6,6), filename=filename)
        wall_base.rotateLeft()
        wall_base.rotateLeft()

        filename = os.path.join(os.path.dirname(__file__), 'schematics', 'wall', 'wall_base_gate.schematic')
        wall_base_gate = MCSchematic(shape=(3,6,2), filename=filename)
        wall_base_gate.rotateLeft()
        wall_base_gate.rotateLeft()
        
        filename = os.path.join(os.path.dirname(__file__), 'schematics', 'wall', 'wall_base_corner.schematic')
        wall_base_corner = MCSchematic(shape=(6,6,6), filename=filename)
        wall_base_corner.rotateLeft()
        wall_base_corner.rotateLeft()

        filename = os.path.join(os.path.dirname(__file__), 'schematics', 'wall', 'inner_wall.schematic')
        inner_wall = MCSchematic(shape=(5,1,5), filename=filename)
        inner_wall.rotateLeft()
        inner_wall.rotateLeft()
        
        filename = os.path.join(os.path.dirname(__file__), 'schematics', 'wall', 'inner_wall_corner.schematic')
        inner_wall_corner = MCSchematic(shape=(6,1,6), filename=filename)
        inner_wall_corner.rotateLeft()
        inner_wall_corner.rotateLeft()

        # -z:

        ground = heightmap[len(heightmap)-8][7]
        if ground == -1:
            pass
        elif ground < (corner_ground[0]+7):
            level.copyBlocksFrom(wall_base_corner, wall_base_corner.bounds, Vector(box.maxx-9, ground-3, box.minz+3))
            if ground < (corner_ground[0]):
                for y in range(256):
                    if level.blockAt(box.maxx-8, ground+3+y, box.minz+7) == 0:
                        level.copyBlocksFrom(inner_wall_corner, inner_wall_corner.bounds, Vector(box.maxx-9, ground+3+y, box.minz+3))
                    else:
                        break

        # left: 
        i = 4
        for sections in range(x_left):
            for wt in range(4): # wall type
                if wt == 3: # base

                    ground = heightmap[len(heightmap)-8-i][7]
                    outer = heightmap[len(heightmap)-8-i][0]
                    if heightmap[len(heightmap)-8-i][1] == -1 or ground == -1:
                        pass
                    elif ground < (outer+7):
                        if sections is not x_left - 1:
                            level.copyBlocksFrom(wall_base, wall_base.bounds, Vector(box.maxx-10-i, ground-3, box.minz+3))
                            if ground < (outer):
                                for y in range(256):
                                    if level.blockAt(box.maxx-8-i, ground+3+y, box.minz+7) == 0:
                                        level.copyBlocksFrom(inner_wall, inner_wall.bounds, Vector(box.maxx-10-i, ground+3+y, box.minz+3))
                                    else:
                                        break
                        else: 
                            level.copyBlocksFrom(wall_base_gate, wall_base_gate.bounds, Vector(box.maxx-9-i, gate_pos_1[1]-3, box.minz+7))

                    i += 4

        # right: 
        i = 4
        for sections in range(x_right):
            for wt in range(4): # wall type
                if wt == 3: # base

                    ground = heightmap[8+i][7]
                    outer = heightmap[8+i][0]
                    if heightmap[8+i][1] == -1 or ground == -1:
                        pass
                    elif ground < (outer+6):
                        if sections is not x_right - 1:
                            level.copyBlocksFrom(wall_base, wall_base.bounds, Vector(box.minx+5+i, ground-3, box.minz+3))
                            if ground < (outer):
                                for y in range(256):
                                    if level.blockAt(box.minx+7+i, ground+3+y, box.minz+7) == 0:
                                        level.copyBlocksFrom(inner_wall, inner_wall.bounds, Vector(box.minx+5+i, ground+3+y, box.minz+3))
                                    else:
                                        break
                        else: 
                            level.copyBlocksFrom(wall_base_gate, wall_base_gate.bounds, Vector(box.minx+6+i, gate_pos_1[1]-3, box.minz+7))

                    i += 4

        progress += 1

        logger.info('Placing {}s... ({}/4)'.format(building, progress))

        wall_base.rotateLeft()
        wall_base_gate.rotateLeft()
        wall_base_corner.rotateLeft()
        inner_wall.rotateLeft()
        inner_wall_corner.rotateLeft()

        # -x:

        ground = heightmap[8][8]
        if ground == -1:
            pass
        elif ground < (corner_ground[1]+6):
            level.copyBlocksFrom(wall_base_corner, wall_base_corner.bounds, Vector(box.minx+3, ground-3, box.minz+3))
            if ground < (corner_ground[1]):
                for y in range(256):
                    if level.blockAt(box.minx+7, ground+3+y, box.minz+7) == 0:
                        level.copyBlocksFrom(inner_wall_corner, inner_wall_corner.bounds, Vector(box.minx+3, ground+3+y, box.minz+3))
                    else:
                        break

        # left: 
        i = 4
        for sections in range(z_left):
            for wt in range(4): # wall type
                if wt == 3: # pillar
                    ground = heightmap[8][8+i]
                    outer = heightmap[1][8+i]
                    if heightmap[1][8+i] == -1 or ground == -1:
                        pass
                    elif ground < (outer+6):
                        if sections is not z_left - 1:
                            level.copyBlocksFrom(wall_base, wall_base.bounds, Vector(box.minx+3, ground-3, box.minz+5+i))
                            if ground < (outer):
                                for y in range(256):
                                    if level.blockAt(box.minx+7, ground+3+y, box.minz+7+i) == 0:
                                        level.copyBlocksFrom(inner_wall, inner_wall.bounds, Vector(box.minx+3, ground+3+y, box.minz+5+i))
                                    else:
                                        break
                        else: 
                            level.copyBlocksFrom(wall_base_gate, wall_base_gate.bounds, Vector(box.minx+7, gate_pos_2[1]-3, box.minz+6+i))

                    i += 4

        # right: 
        i = 4
        for sections in range(z_right):
            for wt in range(4): # wall type
                if wt == 3: # pillar
                    ground = heightmap[8][len(heightmap[1])-8-i]
                    outer = heightmap[1][len(heightmap[1])-8-i]
                    if heightmap[1][len(heightmap[1])-8-i] == -1 or ground == -1:
                        pass
                    elif ground < (outer+6):
                        if sections is not z_right - 1:
                            level.copyBlocksFrom(wall_base, wall_base.bounds, Vector(box.minx+3, ground-3, box.maxz-10-i))
                            if ground < (outer):
                                for y in range(256):
                                    if level.blockAt(box.minx+7, ground+3+y, box.maxz-8-i) == 0:
                                        level.copyBlocksFrom(inner_wall, inner_wall.bounds, Vector(box.minx+3, ground+3+y, box.maxz-10-i))
                                    else:
                                        break
                        else: 
                            level.copyBlocksFrom(wall_base_gate, wall_base_gate.bounds, Vector(box.minx+7, gate_pos_2[1]-3, box.maxz-9-i))
                    
                    i += 4
        progress += 1

        logger.info('Placing {}s... ({}/4)'.format(building, progress))

        wall_base.rotateLeft()
        wall_base_gate.rotateLeft()
        wall_base_corner.rotateLeft()
        inner_wall.rotateLeft()
        inner_wall_corner.rotateLeft()

        # +z:

        ground = heightmap[7][len(heightmap[8])-9]
        if ground == -1:
            pass
        elif ground < (corner_ground[2]+6):
            level.copyBlocksFrom(wall_base_corner, wall_base_corner.bounds, Vector(box.minx+3, ground-3, box.maxz-9))
            if ground < (corner_ground[2]):
                for y in range(256):
                    if level.blockAt(box.minx+7, ground+3+y, box.maxz-8) == 0:
                        level.copyBlocksFrom(inner_wall_corner, inner_wall_corner.bounds, Vector(box.minx+3, ground+3+y, box.maxz-9))
                        
                    else:
                        break

        # left: 
        i = 4
        for sections in range(x_left):
            for wt in range(4): # wall type
                if wt == 3: # pillar
                    ground = heightmap[len(heightmap)-8-i][len(heightmap[len(heightmap)-8-i])-9]
                    outer = heightmap[len(heightmap)-8-i][len(heightmap[len(heightmap)-8-i])-2]
                    if heightmap[len(heightmap)-8-i][len(heightmap[len(heightmap)-8-i])-2] == -1 or ground == -1:
                        pass
                    elif ground < (outer+6):
                        if sections is not x_left - 1:
                            level.copyBlocksFrom(wall_base, wall_base.bounds, Vector(box.maxx-10-i, ground-3, box.maxz-9))
                            if ground < (outer):
                                for y in range(256):
                                    if level.blockAt(box.maxx-8-i, ground+3+y, box.maxz-8) == 0:
                                        level.copyBlocksFrom(inner_wall, inner_wall.bounds, Vector(box.maxx-10-i, ground+3+y, box.maxz-8))
                                    else:
                                        break
                        else: 
                            level.copyBlocksFrom(wall_base_gate, wall_base_gate.bounds, Vector(box.maxx-9-i, gate_pos_3[1]-3, box.maxz-9))
                    
                    i += 4

        # right: 
        i = 4
        for sections in range(x_right):
            for wt in range(4): # wall type
                if wt == 3: # pillar
                    ground = heightmap[8+i][len(heightmap[8+i])-9]
                    outer = heightmap[8+i][len(heightmap[8+i])-2]
                    if heightmap[8+i][len(heightmap[8+i])-2] == -1 or ground == -1:
                        pass
                    elif ground < (outer+6):
                        if sections is not x_right - 1:
                            level.copyBlocksFrom(wall_base, wall_base.bounds, Vector(box.minx+5+i, ground-3, box.maxz-9))
                            if ground < (outer):
                                for y in range(256):
                                    if level.blockAt(box.minx+7+i, ground+3+y, box.maxz-8) == 0:
                                        level.copyBlocksFrom(inner_wall, inner_wall.bounds, Vector(box.minx+5+i, ground+3+y, box.maxz-8))
                                    else:
                                        break
                        else: 
                            level.copyBlocksFrom(wall_base_gate, wall_base_gate.bounds, Vector(box.minx+6+i, gate_pos_3[1]-3, box.maxz-9))

                    i += 4
        progress += 1

        logger.info('Placing {}s... ({}/4)'.format(building, progress))

        wall_base.rotateLeft()
        wall_base_gate.rotateLeft()
        wall_base_corner.rotateLeft()
        inner_wall.rotateLeft()
        inner_wall_corner.rotateLeft()

        # +x:

        ground = heightmap[len(heightmap)-8][len(heightmap[len(heightmap)-8])-8]
        if ground == -1:
            pass
        elif ground < (corner_ground[3]+6):
            level.copyBlocksFrom(wall_base_corner, wall_base_corner.bounds, Vector(box.maxx-9, ground-3, box.maxz-9))
            if ground < (corner_ground[3]):
                for y in range(256):
                    if level.blockAt(box.maxx-8, ground+3+y, box.maxz-8) == 0:
                        level.copyBlocksFrom(inner_wall_corner, inner_wall_corner.bounds, Vector(box.maxx-9, ground+3+y, box.maxz-9))
                    else:
                        break

        # left: 
        i = 4
        for sections in range(z_left):
            for wt in range(4): # wall type
                if wt == 3: # pillar
                    ground = heightmap[len(heightmap)-9][8+i]
                    outer = heightmap[len(heightmap)-2][8+i]
                    if heightmap[len(heightmap)-2][8+i] == -1 or ground == -1:
                        pass
                    elif ground < (outer+6):
                        if sections is not z_left - 1:
                            level.copyBlocksFrom(wall_base, wall_base.bounds, Vector(box.maxx-9, ground-3, box.minz+5+i))
                            if ground < (outer):
                                for y in range(256):
                                    if level.blockAt(box.maxx-8, ground+3+y, box.minz+7+i) == 0:
                                        level.copyBlocksFrom(inner_wall, inner_wall.bounds, Vector(box.maxx-8, ground+3+y, box.minz+5+i))
                                    else:
                                        break
                        else: 
                            level.copyBlocksFrom(wall_base_gate, wall_base_gate.bounds, Vector(box.maxx-9, gate_pos_4[1]-3, box.minz+6+i))

                    i += 4

        # right: 
        i = 4
        for sections in range(z_right):
            for wt in range(4): # wall type
                if wt == 3: # pillar
                    ground = heightmap[len(heightmap)-9][len(heightmap[len(heightmap)-2])-8-i]
                    outer = heightmap[len(heightmap)-2][len(heightmap[len(heightmap)-2])-8-i]
                    if heightmap[len(heightmap)-2][len(heightmap[len(heightmap)-2])-8-i] == -1 or ground == -1:
                        pass
                    elif ground < (outer+6):
                        if sections is not z_right - 1:
                            level.copyBlocksFrom(wall_base, wall_base.bounds, Vector(box.maxx-9, ground-3, box.maxz-10-i))
                            if ground < (outer):
                                for y in range(256):
                                    if level.blockAt(box.maxx-8, ground+3+y, box.maxz-8-i) == 0:
                                        level.copyBlocksFrom(inner_wall, inner_wall.bounds, Vector(box.maxx-8, ground+3+y, box.maxz-10-i))
                                    else:
                                        break
                        else: 
                            level.copyBlocksFrom(wall_base_gate, wall_base_gate.bounds, Vector(box.maxx-9, gate_pos_4[1]-3, box.maxz-9-i))
                    
                    i += 4
        progress += 1

        logger.info('Placing {}s... ({}/4)'.format(building, progress))

    except Exception as e:
        logger.error(e)

def pave_gates(level, box, combinedHM, gate_pos_1, gate_pos_2, gate_pos_3, gate_pos_4, x_gate, z_gate):
    gate_1_minh = gate_pos_1[1] - 5
    gate_2_minh = gate_pos_2[1] - 5
    gate_3_minh = gate_pos_3[1] - 5
    gate_4_minh = gate_pos_4[1] - 5
    for x in xrange(gate_pos_1[0], (gate_pos_1[0] + x_gate + 4)): # x_gate
        for z in xrange(gate_pos_1[2], (gate_pos_1[2] + 14)):
            if combinedHM[x - box.minx][z - box.minz] > (gate_pos_1[1]):
                for d in range((gate_pos_1[1]), combinedHM[x - box.minx][z - box.minz]): # Remove blocks above the plaza and wall
                    level.setBlockAt(x, d, z, 0)
            else:
                if combinedHM[x - box.minx][z - box.minz] < (gate_pos_1[1]) and combinedHM[x - box.minx][z - box.minz] < gate_1_minh:
                    gate_1_minh = combinedHM[x - box.minx][z - box.minz]

        
        for z in xrange(gate_pos_3[2] - 5, (gate_pos_3[2]) + 9):
            if combinedHM[x - box.minx][z - box.minz] > (gate_pos_3[1]):
                for d in range((gate_pos_3[1]), combinedHM[x - box.minx][z - box.minz]): # Remove blocks above the plaza and wall
                    level.setBlockAt(x, d, z, 0)
            else:
                if combinedHM[x - box.minx][z - box.minz] < (gate_pos_3[1]) and combinedHM[x - box.minx][z - box.minz] < gate_3_minh:
                    gate_3_minh = combinedHM[x - box.minx][z - box.minz]

    for z in xrange(gate_pos_2[2], (gate_pos_2[2] + z_gate + 4)): # z_gate
        for x in xrange(gate_pos_2[0], (gate_pos_2[0] + 14)):
            if combinedHM[x - box.minx][z - box.minz] > (gate_pos_2[1]):
                for d in range((gate_pos_2[1]), combinedHM[x - box.minx][z - box.minz]): # Remove blocks above the plaza and wall
                    level.setBlockAt(x, d, z, 0)
            else:
                if combinedHM[x - box.minx][z - box.minz] < (gate_pos_2[1]) and combinedHM[x - box.minx][z - box.minz] < gate_2_minh:
                    gate_2_minh = combinedHM[x - box.minx][z - box.minz]

        
        for x in xrange(gate_pos_4[0] - 5, (gate_pos_4[0]) + 9):
            if combinedHM[x - box.minx][z - box.minz] > (gate_pos_4[1]):
                for d in range((gate_pos_4[1]), combinedHM[x - box.minx][z - box.minz]): # Remove blocks above the plaza and wall
                    level.setBlockAt(x, d, z, 0)
            else:
                if combinedHM[x - box.minx][z - box.minz] < (gate_pos_4[1]) and combinedHM[x - box.minx][z - box.minz] < gate_4_minh:
                    gate_4_minh = combinedHM[x - box.minx][z - box.minz]

    for x in xrange(gate_pos_1[0], (gate_pos_1[0] + x_gate + 4)): # x_gate
        for z in xrange(gate_pos_1[2], (gate_pos_1[2] + 14)):
            for y in xrange(gate_1_minh, gate_pos_1[1]):
                level.setBlockAt(x, y, z, 43) # Making the base of plaza
                level.setBlockDataAt(x, y, z, 0)
        
        for z in xrange(gate_pos_3[2] - 5, (gate_pos_3[2]) + 9):
            for y in xrange(gate_3_minh, gate_pos_3[1]):
                level.setBlockAt(x, y, z, 43) # Making the base of plaza
                level.setBlockDataAt(x, y, z, 0)

    for z in xrange(gate_pos_2[2], (gate_pos_2[2] + z_gate + 4)): # z_gate
        for x in xrange(gate_pos_2[0], (gate_pos_2[0] + 14)):
            for y in xrange(gate_2_minh, gate_pos_2[1]):
                level.setBlockAt(x, y, z, 43) # Making the base of plaza
                level.setBlockDataAt(x, y, z, 0)
        
        for x in xrange(gate_pos_4[0] - 5, (gate_pos_4[0]) + 9):
            for y in xrange(gate_4_minh, gate_pos_4[1]):
                level.setBlockAt(x, y, z, 43) # Making the base of plaza
                level.setBlockDataAt(x, y, z, 0)

    for y in xrange(0, 6):
        x_width = z_length = x_length = z_width = y

        if (box.width < 50):
            x_width = 0
            z_length = 0

        if (box.length < 50):
            x_length = 0
            z_width = 0

        for x in xrange(gate_pos_1[0] - x_width, (gate_pos_1[0] + x_gate + x_width + 4)): # x_gate
            for z in xrange(gate_pos_1[2] + 9, (gate_pos_1[2] + x_length + 14)):
                if x <= gate_pos_1[0] - 1 or x >= gate_pos_1[0] + x_gate + 4 or z >= gate_pos_1[2] + 14:
                    level.setBlockAt((x), gate_pos_1[1] - 1 + y, (z), 0)
                    if combinedHM[x - box.minx][z - box.minz] > gate_pos_1[1] - 1 + y:
                        for d in range(gate_pos_1[1] - 1 + y, combinedHM[x - box.minx][z - box.minz]): # Remove blocks above the plaza and wall
                            level.setBlockAt(x, d, z, 0)
            
            for z in xrange(gate_pos_3[2] - 5 - x_length, (gate_pos_3[2])):
                if x <= gate_pos_3[0] - 1 or x >= gate_pos_3[0] + x_gate + 4 or z <= gate_pos_3[2] - 6:
                    level.setBlockAt((x), gate_pos_3[1] - 1 + y, (z), 0)
                    if combinedHM[x - box.minx][z - box.minz] > gate_pos_3[1] - 1 + y:
                        for d in range(gate_pos_3[1] - 1 + y, combinedHM[x - box.minx][z - box.minz]): # Remove blocks above the plaza and wall
                            level.setBlockAt(x, d, z, 0)

        for z in xrange(gate_pos_2[2] - z_width, (gate_pos_2[2] + z_gate + z_width + 4)): # z_gate
            for x in xrange(gate_pos_2[0] + 9, (gate_pos_2[0] + z_length + 14)):
                if z <= gate_pos_2[2] - 1 or z >= gate_pos_2[2] + z_gate + 4 or x >= gate_pos_2[0] + 14:
                    level.setBlockAt((x), gate_pos_2[1] - 1 + y, (z), 0)
                    if combinedHM[x - box.minx][z - box.minz] > gate_pos_2[1] - 1 + y:
                        for d in range(gate_pos_2[1] - 1 + y, combinedHM[x - box.minx][z - box.minz]): # Remove blocks above the plaza and wall
                            level.setBlockAt(x, d, z, 0)

            for x in xrange(gate_pos_4[0] - 5 - z_length, (gate_pos_4[0])):
                if z <= gate_pos_4[2] - 1 or z >= gate_pos_4[2] + z_gate + 4 or x <= gate_pos_4[0] - 6:
                    level.setBlockAt((x), gate_pos_4[1] - 1 + y, (z), 0)
                    if combinedHM[x - box.minx][z - box.minz] > gate_pos_4[1] - 1 + y:
                        for d in range(gate_pos_4[1] - 1 + y, combinedHM[x - box.minx][z - box.minz]): # Remove blocks above the plaza and wall
                            level.setBlockAt(x, d, z, 0)         

def place_walls(level, box, afterHM, combinedHM):
    try:
        
        x_left, x_right, x_gate, z_left, z_right, z_gate = calc_wall_sections(box) # calculate wall sections and gate sizes
        
        corner_ground = place_wall_corners(level, box, afterHM, combinedHM)
        gate_pos_1, gate_pos_2, gate_pos_3, gate_pos_4 = place_wall_sections(level, box, afterHM, combinedHM, x_left, x_right, z_left, z_right, x_gate, z_gate)
        pave_gates(level, box, combinedHM, gate_pos_1, gate_pos_2, gate_pos_3, gate_pos_4, x_gate, z_gate)
        place_gates(level, box, afterHM, gate_pos_1, gate_pos_2, gate_pos_3, gate_pos_4, x_gate, z_gate)
        place_wall_base(level, box, afterHM, combinedHM, x_left, x_right, z_left, z_right, gate_pos_1, gate_pos_2, gate_pos_3, gate_pos_4, corner_ground)
        
        logger.info('Wall generation completed.')

        return gate_pos_1, gate_pos_2, gate_pos_3, gate_pos_4, x_gate, z_gate
    except Exception as e:
        logger.error(e)