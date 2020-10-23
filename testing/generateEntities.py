# jira linked issue GDMC-28

from pymclevel import TAG_Compound, TAG_Int, TAG_Short, TAG_Byte, TAG_String, TAG_Float, TAG_Double, TAG_List

displayName = "Generate Chests"

def perform(level, box, options):
    for (chunk, slices, point) in level.getChunkSlices(box):

        print chunk
        print slices
        print point

        print type(chunk)
        print type(slices)
        print type(point)

        # for e in chunk.TileEntities:
        #     print (e)

    # if box.width == 1 and box.height == 1 and box.length == 1 and level.blockAt(box.minx, box.miny, box.minz) == 0:
    #     level.setBlockAt(box.minx, box.miny, box.minz, 54)
    #     level.setBlockDataAt(box.minx, box.miny, box.minz, 5)

    #     chest = TAG_Compound()
    #     chest["x"] = TAG_Int(box.minx)
    #     chest["y"] = TAG_Int(box.miny)
    #     chest["z"] = TAG_Int(box.minz)
    #     chest["id"] = TAG_String(u'Chest')

    #     chunk = level.getChunk(box.minx/16, box.minz/16)

    #     chunk.TileEntities.append(chest)
    #     chunk.dirty = True

    if box.width == 1 and box.height == 2 and box.length == 1 and level.blockAt(box.minx, box.miny, box.minz) == 0 and level.blockAt(box.minx, box.miny+1, box.minz) == 0:
        level.setBlockAt(box.minx, box.miny, box.minz, 64)
        level.setBlockAt(box.minx, box.miny+1, box.minz, 64)
        level.setBlockDataAt(box.minx, box.miny, box.minz, 2)
        level.setBlockDataAt(box.minx, box.miny+1, box.minz, 9)

        # chest = TAG_Compound()
        # chest["x"] = TAG_Int(box.minx)
        # chest["y"] = TAG_Int(box.miny)
        # chest["z"] = TAG_Int(box.minz)
        # chest["id"] = TAG_String(u'Chest')

        # chunk = level.getChunk(box.minx/16, box.minz/16)

        # chunk.TileEntities.append(chest)
        # chunk.dirty = True