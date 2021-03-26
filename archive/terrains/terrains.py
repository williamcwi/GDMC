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

def removeSurfaceWater(level, box, exclusion, heightMap, waterHM):
    hmCopy = deepcopy(heightMap)
    alterDict = dict()
    alterHeightDict = dict()
    exclusion = 0
    def FF(x, y, area, block, surroundingHeight):
        if len(area) < 1000:
            hmCopy[x][y] = 999
            area.append([x, y])
            if ((x + 1) < (len(heightMap))): # go to south
                if hmCopy[x + 1][y] == -1:
                    area, block, surroundingHeight = FF(x + 1, y, area, block, surroundingHeight)
                elif hmCopy[x + 1][y] != 999 and heightMap[x + 1][y] != -1:
                    surroundingHeight.append(heightMap[x + 1][y])
                    block.append(level.blockAt(box.minx + x + 1, heightMap[x + 1][y] - 1, box.minz + y))
            if ((y - 1) >= (0)):  # go to west
                if hmCopy[x][y - 1] == -1:
                    area, block, surroundingHeight = FF(x, y - 1, area, block, surroundingHeight)
                elif hmCopy[x][y - 1] != 999 and heightMap[x][y - 1] != -1:
                    surroundingHeight.append(heightMap[x][y - 1])
                    block.append(level.blockAt(box.minx + x, heightMap[x][y - 1] - 1, box.minz + y - 1))
            if ((x - 1) >= (0)): # go to north
                if hmCopy[x - 1][y] == -1:
                    area, block, surroundingHeight = FF(x - 1, y, area, block, surroundingHeight)
                elif hmCopy[x - 1][y] != 999 and heightMap[x - 1][y] != -1:
                    surroundingHeight.append(heightMap[x - 1][y])
                    block.append(level.blockAt(box.minx + x - 1, heightMap[x - 1][y] - 1, box.minz + y))
            if ((y + 1) < (len(heightMap[x]))): # go to east
                if hmCopy[x][y + 1] == -1:
                    area, block, surroundingHeight = FF(x, y + 1, area, block, surroundingHeight)
                elif hmCopy[x][y + 1] != 999 and heightMap[x][y + 1] != -1:
                    surroundingHeight.append(heightMap[x][y + 1])
                    block.append(level.blockAt(box.minx + x, heightMap[x][y + 1] - 1, box.minz + y + 1))
        return area, block, surroundingHeight

    for x in range(exclusion, len(heightMap) - exclusion):
        for y in range(exclusion, len(heightMap[0]) - exclusion):
            if hmCopy[x][y] == -1:
                height = waterHM[x][y]
                area, block, surroundingHeight= FF(x, y, [], [], [])
                targetBlock = max(set(block), key=block.count) if len(block) > 1 else 133
                targetHeight = max(set(surroundingHeight), key=surroundingHeight.count) if len(block) > 1 else 133
                valid = False if len([i for i in area if i[0] < exclusion or i[0] > len(heightMap) - exclusion or i[1] < exclusion or i[1] > len(heightMap[0]) - exclusion]) > 0 else True
                if valid:
                    if height > targetHeight:
                        for cell in area:
                            alterDict[cell[0], cell[1]] = targetHeight - height
                            alterHeightDict[cell[0], cell[1]] = waterHM[cell[0]][cell[1]]
                            if len(area) < 150:
                                level.setBlockAt(box.minx + cell[0], height - 1, box.minz + cell[1], targetBlock)
                    if height < targetHeight and len(area) < 150:
                        for cell in area:
                            alterDict[cell[0], cell[1]] = targetHeight - height + 2
                            alterHeightDict[cell[0], cell[1]] = waterHM[cell[0]][cell[1]] - 2


    editTerrainFF(level, box, alterDict, alterHeightDict)