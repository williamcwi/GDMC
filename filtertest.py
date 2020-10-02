displayName = "Test Filter"

inputs = (
    ("Boolean", True),
    ("Int", 5),
    ("Float", 1.0),
    ("Number Tuple", (5, -128, 128)),
    ("String Tuple", ("blockAt", "temp schematic", "chunk slices")),
    ("Block Type", "blocktype"),
)

def perform(level, box, options):

    selection = options["String Tuple"]
    
    # using level.blockAt and level.setBlockAt
    # slower than the other two methods, but easier to start using
    if selection == "blockAt":
        for x in xrange(box.minx, box.maxx):
            for z in xrange(box.minz, box.maxz):
                for y in xrange(box.miny, box.maxy): # nested loops can be slow

                    # replaces grass with gold
                    if level.blockAt(x, y, z) == 2:
                        level.setBlockAt(x, y, z, 41)
    
    # extract the segment of interest into a contiguous array using level.extractSchematic
    # this simplifies using numpy but at the cost of the temporary buffer and the risk of a memory error on 32-bit systems
    if selection == "temp schematic":
        temp = level.extractSchematic(box)

        # remove any entities in the temp.  this is an ugly move
        # because copyBlocksFrom actually copies blocks, entities, everything
        temp.removeEntitiesInBox(temp.bounds)
        temp.removeTileEntitiesInBox(temp.bounds)

        # replaces grass with gold
        # the expression in [] creates a temporary the same size, using more memory
        temp.Blocks[temp.Blocks == 2] = 41

        level.copyBlocksFrom(temp, temp.bounds, box.origin)

    if selection == "chunk slices":
        
        for (chunk, slices, point) in level.getChunkSlices(box):
            # chunk is an AnvilChunk object with attributes:
            # Blocks, Data, Entities, and TileEntities
            # Blocks and Data can be indexed using slices:
            blocks = chunk.Blocks[slices]

            # blocks now contains a "view" on the part of the chunk's blocks
            # that lie in the selection. This "view" is a numpy object that
            # accesses only a subsection of the original array, without copying

            # grass into gold
            blocks[blocks == 2] = 41

            # notify the world that the chunk changed
            # this gives finer control over which chunks are dirtied
            # you can call chunk.chunkChanged(False) if you want to dirty it
            # but not run the lighting calc later.

            chunk.chunkChanged()