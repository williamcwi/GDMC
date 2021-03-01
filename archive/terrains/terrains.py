def removeFlowingLava(level, box):
    try:
        for (chunk, slices, point) in level.getChunkSlices(box):
            blocks = chunk.Blocks[slices]
            # Change blocks to air
            blocks[blocks == 10] = 0 # flowing lava
            chunk.dirty = True
        
        logger.info('Removing flowing lava...')
    

    except Exception as e:
        logger.error(e)