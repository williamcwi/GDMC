from pymclevel import TAG_Compound, TAG_Int, TAG_Short, TAG_Byte, TAG_String, TAG_Float, TAG_Double, TAG_List

displayName = "Generate Test Building (blockAt)"

def perform(level, box, options): 
    
    # x/y/z value of building is 11/6/11

    # level.setBlockDataAt(x, y, z, orientation)
    # orientation: 
    #   Downwards (towards -y): 0
    #   Upwards (towards +y): 1
    #   Northwards (towards -z): 2
    #   Southwards (towards +z): 3
    #   Westwards (towards -x): 4
    #   Eastwards (towards +x): 5
    
    for x in xrange(box.minx, box.maxx):
        for z in xrange(box.minz, box.maxz):
            for y in xrange(box.miny, box.maxy):
                # layer 1
                if y == box.miny:
                    
                    # fences
                    if x == box.maxx - 2:
                        if z == box.maxz - 2 or z == box.maxz - 9:
                            level.setBlockAt(x, y, z, 85)

                    if x == box.maxx - 9:
                        if z == box.maxz - 2 or z == box.maxz - 9:
                            level.setBlockAt(x, y, z, 85)

                    # stairs
                    if x == box.maxx - 7 or x == box.maxx - 8:
                        if z == box.maxz - 11:
                            level.setBlockAt(x, y, z, 53)
                            level.setBlockDataAt(x, y, z, 2)

                    if z == box.maxz - 7 or z == box.maxz - 8:
                        if x == box.maxx - 11:
                            level.setBlockAt(x, y, z, 53)

                # layer 2
                if y == box.miny + 1:

                    # platform
                    if box.maxx - 2 >= x >= box.maxx - 9:
                        if box.maxz - 2 >= z >= box.maxz - 9:
                            level.setBlockAt(x, y, z, 5)
                            level.setBlockDataAt(x, y, z, 5)
                    
                    if box.maxx - 3 >= x >= box.maxx - 8:
                        if box.maxz - 3 >= z >= box.maxz - 8:
                            level.setBlockAt(x, y, z, 5)
                            level.setBlockDataAt(x, y, z, 1)

                    if box.maxx - 4 >= x >= box.maxx - 6:
                        if box.maxz - 4 >= z >= box.maxz - 6:
                            level.setBlockAt(x, y, z, 5)
                            level.setBlockDataAt(x, y, z, 0)

                    # stairs
                    if x == box.maxx - 7 or x == box.maxx - 8:
                        if z == box.maxz - 10:
                            level.setBlockAt(x, y, z, 53)
                            level.setBlockDataAt(x, y, z, 2)

                    if z == box.maxz - 7 or z == box.maxz - 8:
                        if x == box.maxx - 10:
                            level.setBlockAt(x, y, z, 53)

                # layer 3
                if y == box.miny + 2:

                    # fences
                    if box.maxx - 2 >= x >= box.maxx - 6:
                        if z == box.maxz - 9:
                            level.setBlockAt(x, y, z, 85)
                    
                    if box.maxz - 2 >= z >= box.maxz - 6:
                        if x == box.maxx - 9:
                            level.setBlockAt(x, y, z, 85)

                    if z == box.maxz - 9:
                        if x == box.maxx - 9:
                            level.setBlockAt(x, y, z, 85)

                    if z == box.maxz - 8:
                        if x == box.maxx - 2:
                            level.setBlockAt(x, y, z, 85)

                    if z == box.maxz - 2:
                        if x == box.maxx - 8:
                            level.setBlockAt(x, y, z, 85)

                    # pillars
                    if x == box.maxx - 2:
                        if z == box.maxz - 2 or z == box.maxz - 7:
                            level.setBlockAt(x, y, z, 17)

                    if x == box.maxx - 5:
                        if z == box.maxz - 7:
                            level.setBlockAt(x, y, z, 17)

                    if x == box.maxx - 7:
                        if z == box.maxz - 2 or z == box.maxz - 5:
                            level.setBlockAt(x, y, z, 17)

                    # walls
                    if x == box.maxx - 3:
                        if box.maxz - 3 >= z >= box.maxz - 7:
                            level.setBlockAt(x, y, z, 5)

                    if z == box.maxz - 3:
                        if box.maxx - 4 >= x >= box.maxx - 7:
                            level.setBlockAt(x, y, z, 5)

                    if x == box.maxx - 4:
                        if z == box.maxz - 7:
                            level.setBlockAt(x, y, z, 5)

                    if x == box.maxx - 7:
                        if z == box.maxz - 4:
                            level.setBlockAt(x, y, z, 5)

                    # plant
                    if z == box.maxz - 2:
                        if box.maxx - 4 >= x >= box.maxx - 5:
                            level.setBlockAt(x, y, z, 18)

                    if x == box.maxx - 2:
                        if box.maxz - 4 >= z >= box.maxz - 5:
                            level.setBlockAt(x, y, z, 18)

                    if z == box.maxz - 8:
                        if box.maxx - 3 >= x >= box.maxx - 5:
                            level.setBlockAt(x, y, z, 18)

                    if x == box.maxx - 8:
                        if box.maxz - 3 >= z >= box.maxz - 5:
                            level.setBlockAt(x, y, z, 18)

                    # # TODO: entities
                    # # bed
                    # if x == box.maxx - 4:
                    #     if z == box.maxz - 5:
                    #         level.setBlockAt(x, y, z, 26)

                    # # chest
                    # if x == box.maxx - 6:
                    #     if z == box.maxz - 4:
                    #         level.setBlockAt(x, y, z, 54)

                    # # doors
                    # if x == box.maxx - 6:
                    #     if z == box.maxz - 7:
                    #         level.setBlockAt(x, y, z, 197)

                    # # trapdoors
                    # if x == box.maxx - 1:
                    #     if z == box.maxz - 4 or z == box.maxz - 5:
                    #         level.setBlockAt(x, y, z, 96)

                # layer 4
                if y == box.miny + 3:

                    # pillars
                    if x == box.maxx - 2:
                        if z == box.maxz - 2 or z == box.maxz - 7:
                            level.setBlockAt(x, y, z, 17)

                    if x == box.maxx - 5:
                        if z == box.maxz - 7:
                            level.setBlockAt(x, y, z, 17)

                    if x == box.maxx - 7:
                        if z == box.maxz - 2 or z == box.maxz - 5:
                            level.setBlockAt(x, y, z, 17)

                    # walls
                    if x == box.maxx - 3:
                        if box.maxz - 6 >= z >= box.maxz - 7:
                            level.setBlockAt(x, y, z, 5)

                    if z == box.maxz - 3:
                        if box.maxx - 6 >= x >= box.maxx - 7:
                            level.setBlockAt(x, y, z, 5)

                    if x == box.maxx - 4:
                        if z == box.maxz - 7:
                            level.setBlockAt(x, y, z, 5)

                    if x == box.maxx - 7:
                        if z == box.maxz - 4:
                            level.setBlockAt(x, y, z, 5)

                    if x == box.maxx - 3:
                        if z == box.maxz - 3:
                            level.setBlockAt(x, y, z, 5)

                    # windows
                    if x == box.maxx - 3:
                        if box.maxz - 4 >= z >= box.maxz - 5:
                            level.setBlockAt(x, y, z, 160)
                            level.setBlockDataAt(x, y, z, 12)

                    if z == box.maxz - 3:
                        if box.maxx - 4 >= x >= box.maxx - 5:
                            level.setBlockAt(x, y, z, 160)
                            level.setBlockDataAt(x, y, z, 12)

                # layer 5
                if y == box.miny + 4:

                    # pillars
                    if x == box.maxx - 2:
                        if z == box.maxz - 2 or z == box.maxz - 7:
                            level.setBlockAt(x, y, z, 17)

                    if x == box.maxx - 5:
                        if z == box.maxz - 7:
                            level.setBlockAt(x, y, z, 17)

                    if x == box.maxx - 7:
                        if z == box.maxz - 2 or z == box.maxz - 5:
                            level.setBlockAt(x, y, z, 17)

                    # walls
                    if x == box.maxx - 3:
                        if box.maxz - 3 >= z >= box.maxz - 7:
                            level.setBlockAt(x, y, z, 5)

                    if z == box.maxz - 3:
                        if box.maxx - 4 >= x >= box.maxx - 7:
                            level.setBlockAt(x, y, z, 5)

                    if x == box.maxx - 4:
                        if z == box.maxz - 7:
                            level.setBlockAt(x, y, z, 5)

                    if x == box.maxx - 7:
                        if z == box.maxz - 4:
                            level.setBlockAt(x, y, z, 5)

                # # layer 6
                if y == box.miny + 5:

                    # pillars
                    if x == box.maxx - 2:
                        if z == box.maxz - 2 or z == box.maxz - 7:
                            level.setBlockAt(x, y, z, 17)

                    if x == box.maxx - 5:
                        if z == box.maxz - 7:
                            level.setBlockAt(x, y, z, 17)

                    if x == box.maxx - 7:
                        if z == box.maxz - 2 or z == box.maxz - 5:
                            level.setBlockAt(x, y, z, 17)

                    # roof
                    if x == box.maxx - 2:
                        if box.maxz - 3 >= z >= box.maxz - 6:
                            level.setBlockAt(x, y, z, 17)
                            level.setBlockDataAt(x, y, z, 8)

                    if z == box.maxz - 2:
                        if box.maxx - 3 >= x >= box.maxx - 6:
                            level.setBlockAt(x, y, z, 17)
                            level.setBlockDataAt(x, y, z, 4)

                    if x == box.maxx - 7:
                        if box.maxz - 3 >= z >= box.maxz - 4:
                            level.setBlockAt(x, y, z, 17)
                            level.setBlockDataAt(x, y, z, 8)

                    if z == box.maxz - 7:
                        if box.maxx - 3 >= x >= box.maxx - 4:
                            level.setBlockAt(x, y, z, 17)
                            level.setBlockDataAt(x, y, z, 4)

                    if box.maxx - 3 >= x >= box.maxx - 6:
                        if box.maxz - 3 >= z >= box.maxz - 6:
                            level.setBlockAt(x, y, z, 5)

                    if x == box.maxx - 5:
                        if z == box.maxz - 5:
                            level.setBlockAt(x, y, z, 89)