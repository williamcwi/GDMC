from logger import Logger

import platform
import os.path
import datetime
from copy import deepcopy
import heightmap
import numpy as np

import sys
sys.setrecursionlimit(65536)  #!!IMPORTANT to allow floodFill and RECURSIVE

logger = Logger('Terrains')

def execute(level, box, heightMap, waterHM, minimumArea, exclusion = 0):
    alterDict, alterHeightDict = floodFill(level, box, heightMap, waterHM, minimumArea, exclusion)
    editTerrainFF(level, box, alterDict, alterHeightDict)

def floodFill(level, box, heightMap, waterHM, minimumArea, exclusion = 0): # Flood Fill RECURSIVE
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
            9999 : 63
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
            if maskedHM[x][y] == "wate":
                water.append([x,y])
                height.append(waterHM[x][y])
            else:
                height.append(heightMap[x][y])
            maskedHM[x][y] = 999
            area.append([x,y])
            
            if len(area) <= max(min(5000, int(len(tempHM) * len(tempHM[0]) / 10)), 3000):
                if ((x + 1) < (len(maskedHM) - exclusion)): # go to south
                    if maskedHM[x + 1][y] == "0000" or (maskedHM[x + 1][y] == "wate" and waterHM[x + 1][y] != 63):
                        area, height, water, surroundingRegion  = FFZero(x + 1, y, area, height, water, surroundingRegion)
                    elif maskedHM[x + 1][y] != "0000" and maskedHM[x + 1][y] != 999 and maskedHM[x + 1][y] not in excludedBlocks.values():
                        surroundingRegion.append(maskedHM[x + 1][y])
                if ((y - 1) >= (0 + exclusion)):  # go to west
                    if maskedHM[x][y - 1] == "0000" or (maskedHM[x][y - 1] == "wate" and waterHM[x][y - 1] != 63):
                        area, height, water, surroundingRegion  = FFZero(x, y - 1, area, height, water, surroundingRegion)
                    elif maskedHM[x][y - 1] != "0000" and maskedHM[x][y - 1] != 999 and maskedHM[x][y - 1] not in excludedBlocks.values():
                        surroundingRegion.append(maskedHM[x][y - 1])
                if ((x - 1) >= (0 + exclusion)): # go to north
                    if maskedHM[x - 1][y] == "0000" or (maskedHM[x - 1][y] == "wate" and waterHM[x - 1][y] != 63):
                        area, height, water, surroundingRegion  = FFZero(x - 1, y, area, height, water, surroundingRegion)
                    elif maskedHM[x - 1][y] != "0000" and maskedHM[x - 1][y] != 999 and maskedHM[x - 1][y] not in excludedBlocks.values():
                        surroundingRegion.append(maskedHM[x - 1][y])
                if ((y + 1) < (len(maskedHM[x]) - exclusion)): # go to east
                    if maskedHM[x][y + 1] == "0000" or (maskedHM[x][y + 1] == "wate" and waterHM[x][y + 1] != 63):
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
                    if len(area) >= minimumArea: # if area greater equa, ls to the threshold
                        valid = False
                        for cell in area:
                            if cell[0] + 12 < len(heightMap) and cell[1] + 12 < len(heightMap[0]):
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
                    elif regionAlias is "wate" or regionAlias is "lava":
                        if waterHM[x][y] == 63 and len(area) > minimumArea:
                            regionAlias = 9999
                        for blocks in area:
                            maskedHM[blocks[0]][blocks[1]] = regionAlias

        for x in range(exclusion, (len(maskedHM) - exclusion)):
            for y in range(exclusion, (len(maskedHM[0]) - exclusion)):
                # logger.info(u"{} {}".format(x, y))
                if maskedHM[x][y] == "0000":
                    area, height, water, surroundingRegion = FFZero(x, y, [], [], [], [])
                    region = None
                    if len(surroundingRegion) > 0:
                        region = max(set(surroundingRegion), key=surroundingRegion.count)   
                    if region != None and len(area) <= (minimumArea * 4):
                        for item in area:
                                # diffHM[item[0]][item[1]] =  - (heightMap[item[0]][item[1]] - int((heightMap[item[0]+1][item[1]] + heightMap[item[0]-1][item[1]] + heightMap[item[0]][item[1]+1] + heightMap[item[0]][item[1]-1])/4)) if maskedHM[item[0]][item[1]] in excludedBlocks.values() else (regionDict.get(int(maskedHM[item[0]][item[1]])) - heightMap[item[0]][item[1]])
                                alterDict[item[0],item[1]] = (regionDict.get(int(region)) - waterHM[item[0]][item[1]]) if heightMap[item[0]][item[1]] == -1 else (regionDict.get(int(region)) - heightMap[item[0]][item[1]])
                                alterHeightDict[item[0],item[1]] = waterHM[item[0]][item[1]] if heightMap[item[0]][item[1]] == -1 else heightMap[item[0]][item[1]]
                                if heightMap[item[0]][item[1]] == -1 and (regionDict.get(int(region)) - waterHM[item[0]][item[1]] > 0):
                                    level.setBlockAt(box.minx + item[0], waterHM[item[0]][item[1]] - 1, box.minz + item[1], 2)
                                maskedHM[item[0]][item[1]] = region
                                
                    else:
                        tempHeight = deepcopy(height)
                        tempHeight.sort()
                        tempHeight = [i for i in tempHeight if i > 0]
                        if len(tempHeight) > 1:
                            upperRemoval = tempHeight[int(len(tempHeight) * 0.75):len(tempHeight)]
                            upperRemoval = list(set(upperRemoval))
                            lowerRemoval = tempHeight[0:int(len(tempHeight) * 0.1)]
                            lowerRemoval = list(set(lowerRemoval))
                            if len([i for i in list(set(tempHeight)) if i not in upperRemoval]) > 1:
                                targetHeight = max([i for i in list(set(tempHeight)) if i not in upperRemoval])
                                if len(tempHeight[int(len(tempHeight) * 0.75):len(tempHeight)]) > 5:
                                    for i in range(len(height)):
                                        if height[i] in upperRemoval and height[i] > 0 and targetHeight > 0:
                                            if len(water) < minimumArea:
                                                if heightMap[area[i][0]][area[i][1]] == -1:
                                                    # if waterHM[area[i][0]][area[i][1]] > 63 or waterHM[area[i][0]][area[i][1]] < 63:
                                                        level.setBlockAt(box.minx + area[i][0], waterHM[area[i][0]][area[i][1]] - 1, box.minz + area[i][1], 2)
                                                        level.setBlockDataAt(box.minx + area[i][0], waterHM[area[i][0]][area[i][1]] - 1, box.minz + area[i][1], 0)
                                                        level.setBlockAt(box.minx + area[i][0], targetHeight - 1, box.minz + area[i][1], 2)
                                                        level.setBlockDataAt(box.minx + area[i][0], targetHeight - 1, box.minz + area[i][1], 0)
                                                alterDict[area[i][0], area[i][1]] = targetHeight - height[i]
                                                alterHeightDict[area[i][0], area[i][1]] = height[i]

                            if len([i for i in list(set(tempHeight)) if i not in lowerRemoval]) > 1:
                                targetHeight = min([i for i in list(set(tempHeight)) if i not in lowerRemoval])
                                if len(tempHeight[0:int(len(tempHeight) * 0.1)]) > 5:
                                    widthLFlag = False
                                    widthRFlag = False
                                    heightUFlag = False
                                    heightLFlag = False
                                    for i in range(len(height)):
                                        if area[i] in water:
                                            if area[i][0] <= 7:
                                                widthLFlag = True
                                            if area[i][1] <= 7:
                                                heightUFlag = True
                                            if area[i][0] >= box.length - 7:
                                                widthRFlag = True
                                            if area[i][1] >= box.width - 7:
                                                heightLFlag = True
                                    if sum([widthLFlag, widthRFlag, heightUFlag, heightLFlag]) <= 1:
                                        for i in range(len(height)):
                                            if height[i] in lowerRemoval and targetHeight > 0:
                                                    if heightMap[area[i][0]][area[i][1]] == -1:
                                                        # if len(water) < ((len(area) - len(water)) / 10) and (waterHM[area[i][0]][area[i][1]] > 63 or waterHM[area[i][0]][area[i][1]] < 63):
                                                            level.setBlockAt(box.minx + area[i][0], waterHM[area[i][0]][area[i][1]] - 1, box.minz + area[i][1], 2)
                                                            level.setBlockDataAt(box.minx + area[i][0], waterHM[area[i][0]][area[i][1]] - 1, box.minz + area[i][1], 0)
                                                            level.setBlockAt(box.minx + area[i][0], targetHeight - 1, box.minz + area[i][1], 2)
                                                            level.setBlockDataAt(box.minx + area[i][0], targetHeight - 1, box.minz + area[i][1], 0)
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
                level.setBlockDataAt(mappedx, (alterHeightdict[x, y] + (e * (diff / abs(diff)))), mappedz, 0)
            if diff < 0 :
                level.setBlockAt(mappedx, (alterHeightdict[x, y] + diff), mappedz, topblock)
                level.setBlockDataAt(mappedx, (alterHeightdict[x, y] + diff), mappedz, 0)

    except Exception as e:
        logger.error(e)

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
                        level.setBlockDataAt(x, l, z, 0)
        logger.info('Removing lava pools...')

    except Exception as e:
        logger.error(e)
