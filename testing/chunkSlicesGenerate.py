from pymclevel import TAG_Compound, TAG_Int, TAG_Short, TAG_Byte, TAG_String, TAG_Float, TAG_Double, TAG_List

displayName = "Generate Test Building (chunk slices)"

def perform(level, box, options):
    currentchunk = 1

    for (chunk, slices, point) in level.getChunkSlices(box):
        blocks = chunk.Blocks[slices]

        print(blocks)
        print(type(blocks))
        print (chunk)

        if currentchunk == 1:
            blocks[0][0][0] = 1
        elif currentchunk == 2:
            blocks[0][0][0] = 5
        else:
            blocks[0][0][0] = 54

        currentchunk = currentchunk + 1

        for x in xrange(box.minx, box.maxx):
            for z in xrange(box.minz, box.maxz):
                for y in xrange(box.miny, box.maxy):
                    if level.blockAt(x, y, z)==54:
                        level.setBlockDataAt(x, y, z, 5)

                        chest = TAG_Compound()
                        chest["x"] = TAG_Int(x)
                        chest["y"] = TAG_Int(y)
                        chest["z"] = TAG_Int(z)
                        chest["id"] = TAG_String(u'Chest')

                        chunk.TileEntities.append(chest)
        chunk.dirty = True