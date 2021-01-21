def editTerrain (level, box, oldHeightMap, heightMapDiff):
    try:
        zpos = 0
        for z in xrange(box.minz, box.maxz):
            xpos = 0
            for x in xrange(box.minx, box.maxx):
                ydiff = heightMapDiff[zpos][xpos]
                if ydiff < 0:
                    oldy = oldHeightMap[zpos][xpos]
                    newy = oldy + ydiff
                    while oldy > newy:
                        level.setBlockAt(x, oldy, z, 0)
                        oldy -= 1
                if ydiff > 0:
                    oldy = oldHeightMap[zpos][xpos]
                    newy = oldy + ydiff
                    block = level.blockAt(x, oldy, z)
                    while oldy < newy:
                        oldy += 1
                        level.setBlockAt(x, oldy, z, block)
                xpos += 1
            zpos += 1
    except Exception as e:
        logger.error(e)