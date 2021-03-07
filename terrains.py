from logger import Logger

import platform
import os.path
import datetime
from copy import deepcopy
import heightmap

import sys
sys.setrecursionlimit(65536)  #!!IMPORTANT to allow floodFill and RECURSIVE

logger = Logger('Terrains')

def floodFill(heightMap, minimumArea, exclusion = 0): # Flood Fill RECURSIVE
    try:
        tempHM = deepcopy(heightMap)
        maskedHM = [['%04d' % 0 for k in range(len(heightMap[0]))] for j in range(len(heightMap))]  # initialse post-process HM
        #diffHM = [[0 for k in range(len(heightMap[0]))] for j in range(len(heightMap))]

        if exclusion >= len(heightMap) / 3 or exclusion >= len(heightMap[0]) / 3:
            logger.warning("Invalid Exclusion block width")
            logger.warning("Continue with 0 Exclusion block width")
            exclusion = 0

        currentLevel = 999
        currentRegion = 1
        excludedBlocks = { # excluded blocks - excluded from labelling 
            -1 : "wate",
            -2 : "lava"
        }
        regionDict = {
            "wate" : -1,
            "lava" : -2,
            999 : -7
        }
        alterDict = dict()
        alterHeightDict = dict()

        def FF(x, y, area):
            tempHM[x][y] = 999
            area.append([x,y])
            if len(area) <= 10000:
                if ((y - 1) >= (0 + exclusion)):  # go to west
                    if tempHM[x][y - 1] == currentLevel:
                        area = FF(x, y - 1, area)
                if ((y + 1) < (len(tempHM[x]) - exclusion)): # go to east
                    if tempHM[x][y + 1] == currentLevel:
                        area = FF(x, y + 1, area)
                if ((x + 1) < (len(tempHM) - exclusion)): # go to south
                    if tempHM[x + 1][y] == currentLevel:
                        area = FF(x + 1, y, area)
                if ((x - 1) >= (0 + exclusion)): # go to north
                    if tempHM[x - 1][y] == currentLevel:
                        area = FF(x - 1, y, area)
            return area

        def FFZero(x, y, area, height, water, surroundingRegion):
            maskedHM[x][y] = 999
            if heightMap[x][y] == "wate":
                water.append([x, y])
            area.append([x,y])
            height.append(heightMap[x][y])
            if len(area) <= 10000:
                if ((x + 1) < (len(maskedHM) - exclusion)): # go to south
                    if maskedHM[x + 1][y] == "0000":
                        area, height, water, surroundingRegion  = FFZero(x + 1, y, area, height, water, surroundingRegion)
                    elif maskedHM[x + 1][y] != "0000" and maskedHM[x + 1][y] != 999 and maskedHM[x + 1][y] not in excludedBlocks.values():
                        surroundingRegion.append(maskedHM[x + 1][y])
                if ((y - 1) >= (0 + exclusion)):  # go to west
                    if maskedHM[x][y - 1] == "0000":
                        area, height, water, surroundingRegion  = FFZero(x, y - 1, area, height, water, surroundingRegion)
                    elif maskedHM[x][y - 1] != "0000" and maskedHM[x][y - 1] != 999 and maskedHM[x][y - 1] not in excludedBlocks.values():
                        surroundingRegion.append(maskedHM[x][y - 1])
                if ((x - 1) >= (0 + exclusion)): # go to north
                    if maskedHM[x - 1][y] == "0000":
                        area, height, water, surroundingRegion  = FFZero(x - 1, y, area, height, water, surroundingRegion)
                    elif maskedHM[x - 1][y] != "0000" and maskedHM[x - 1][y] != 999 and maskedHM[x - 1][y] not in excludedBlocks.values():
                        surroundingRegion.append(maskedHM[x - 1][y])
                if ((y + 1) < (len(maskedHM[x]) - exclusion)): # go to east
                    if maskedHM[x][y + 1] == "0000":
                        area, height, water, surroundingRegion  = FFZero(x, y + 1, area, height, water, surroundingRegion)
                    elif maskedHM[x][y + 1] != "0000" and maskedHM[x][y + 1] != 999 and maskedHM[x][y + 1] not in excludedBlocks.values():
                        surroundingRegion.append(maskedHM[x][y + 1])
            return area, height, water, surroundingRegion



        for x in range(exclusion, (len(tempHM) - exclusion)):
            for y in range(exclusion, (len(tempHM[0]) - exclusion)):
                if tempHM[x][y] < 257 and tempHM[x][y] >= -20:
                    currentLevel = tempHM[x][y]
                    regionAlias = excludedBlocks.get(currentLevel, '%04d' % currentRegion) # switch between excluded blocks and region label
                    area = FF(x, y, [])
                    
                    if len(area) >= minimumArea or currentLevel < 0: # if area greater equals to the threshold
                        valid = False
                        for cell in area:
                            if cell[0] + 12 < len(heightMap) and cell[1] + 12 <  len(heightMap[0]):
                                plotArea = list([heightMap[i][k] for i in range(cell[0], cell[0] + 12) for k in range(cell[1], cell[1] + 12)])
                                if len(set(plotArea)) == 1 and list(set(plotArea))[0] == currentLevel:
                                    valid = True
                                    break
                        if valid:
                            for blocks in area:
                                maskedHM[blocks[0]][blocks[1]] = regionAlias
                            if currentLevel > 0:
                                regionDict[currentRegion] = currentLevel
                                currentRegion = currentRegion + 1
                    
        for x in range(exclusion, (len(maskedHM) - exclusion)):
            for y in range(exclusion, (len(maskedHM[0]) - exclusion)):
                logger.info(u"{} {}".format(x, y))
                if maskedHM[x][y] == "0000":
                    area, height, water, surroundingRegion = FFZero(x, y, [], [], [], [])
                    region = None
                    if len(surroundingRegion) > 0:
                        region = max(set(surroundingRegion), key=surroundingRegion.count)   
                    if region != None and len(area) <= (minimumArea * 4):
                        for item in area:
                            if heightMap[item[0]][item[1]] != -1:
                                maskedHM[item[0]][item[1]] = region
                                #diffHM[item[0]][item[1]] =  - (heightMap[item[0]][item[1]] - int((heightMap[item[0]+1][item[1]] + heightMap[item[0]-1][item[1]] + heightMap[item[0]][item[1]+1] + heightMap[item[0]][item[1]-1])/4)) if maskedHM[item[0]][item[1]] in excludedBlocks.values() else (regionDict.get(int(maskedHM[item[0]][item[1]])) - heightMap[item[0]][item[1]])
                                alterDict[item[0],item[1]] = - (heightMap[item[0]][item[1]] - int((heightMap[item[0]+1][item[1]] + heightMap[item[0]-1][item[1]] + heightMap[item[0]][item[1]+1] + heightMap[item[0]][item[1]-1])/4)) if maskedHM[item[0]][item[1]] in excludedBlocks.values() else (regionDict.get(int(maskedHM[item[0]][item[1]])) - heightMap[item[0]][item[1]])
                                alterHeightDict[item[0],item[1]] = heightMap[item[0]][item[1]]
                    else:
                        tempHeight = deepcopy(height)
                        tempHeight.sort()
                        tempHeight = [i for i in tempHeight if i > 0]
                        if len(tempHeight) > 1:
                            removal = tempHeight[int(len(tempHeight) * 0.75):len(tempHeight)]
                            removal = list(set(removal))
                            if len([i for i in list(set(tempHeight)) if i not in removal]) > 1:
                                targetHeight = max([i for i in list(set(tempHeight)) if i not in removal])
                                if len(tempHeight[int(len(tempHeight) * 0.75):len(tempHeight)]) > 5:
                                    for i in range(len(height)):
                                        if height[i] in removal and height[i] > 0 and targetHeight > 0:
                                            alterDict[area[i][0], area[i][1]] = targetHeight - height[i]
                                            alterHeightDict[area[i][0], area[i][1]] = height[i]

        # afterHM = [[regionDict.get(maskedHM[j][k], tempHM[j][k]) if maskedHM[j][k] in excludedBlocks.values() else regionDict.get(int(maskedHM[j][k]), tempHM[j][k]) if maskedHM[j][k] != -7 else heightMap[j][k] for k in range(len(maskedHM[j]))] for j in range(len(maskedHM))]
        # ---------------HM naming---------------
        # diffHM - List height difference before and after moderification
        # afterHM - List height after moderification
        # maskedHM - List region group after moderification

        # heightMap2File(afterHM, "HMA")
        # heightMap2File(diffHM, "HMD")
        # heightMap2File(maskedHM, "HMM")
        return alterDict, alterHeightDict # return Dict with changed blocks and orginal blocks height
    except Exception as e:
        logger.error(e)

def editTerrainFF(level, box, alterDict, alterHeightdict):
    try:
        for key, value in alterDict:
            x = key
            y = value
            diff = alterDict[x, y]
            mappedx = box.minx + x
            mappedz = box.minz + y
            topblock = level.blockAt(mappedx, alterHeightdict[x, y] - 1, mappedz)
            block = level.blockAt(mappedx, alterHeightdict[x, y] - 1, mappedz)
            if diff < 0:
                diff -= 1
                block = 0
            for e in xrange(abs(diff)):
                level.setBlockAt(mappedx, (alterHeightdict[x, y] + (e * (diff / abs(diff)))), mappedz, block)
            if diff < 0 :
                level.setBlockAt(mappedx, (alterHeightdict[x, y] + diff), mappedz, topblock)

    except Exception as e:
        logger.error(e)

def removeSurfaceWater(level, box, exclusion, heightMap, waterHM):
    hmCopy = deepcopy(heightMap)
    alterDict = dict()
    alterHeightDict = dict()

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
                if height > targetHeight:
                    for cell in area:
                        alterDict[cell[0], cell[1]] = targetHeight - height
                        alterHeightDict[cell[0], cell[1]] = waterHM[cell[0]][cell[1]]
                        level.setBlockAt(box.minx + cell[0], height - 1, box.minz + cell[1], targetBlock)

    editTerrainFF(level, box, alterDict, alterHeightDict)

def findWaterSurface(waterHeightmap, processedHeightmap):
    try:
        combinedHM = []
        for water, processed in zip(waterHeightmap, processedHeightmap):
            row = []
            for w, p in zip(water, processed):
                if p == -1:
                    row.append(w)
                else:
                    row.append(p)
            combinedHM.append(row)
        return combinedHM

    except Exception as e:
        logger.error(e)

def removeLava(level, box, lavaHeightmap, groundHeightmap, processedHeightmap):
    try:
        # Gets the index rather than value
        for i in range(len(processedHeightmap)):
            for j in range(len(processedHeightmap[i])):
                if processedHeightmap[i][j] == -2: # lava
                    x = box.minx + i
                    z = box.minz + j
                    y1 = lavaHeightmap[i][j]
                    y2 = groundHeightmap[i][j]
                    for l in range(y2, y1):
                        level.setBlockAt(x, l, z, 2)
        logger.info('Removing lava pools...')

    except Exception as e:
        logger.error(e)
