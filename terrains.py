from logger import Logger

import platform
import os.path
import datetime
from copy import deepcopy

import sys
sys.setrecursionlimit(65536)  #!!IMPORTANT to allow floodFill and RECURSIVE

logger = Logger('Terrains')

def floodFill(heightMap, minimumArea, exclusion = 0): # Flood Fill RECURSIVE ################# POC OK TODO:VERIFY #################
    try:
        tempHM = deepcopy(heightMap)
        maskedHM = [['%04d' % 0 for k in range(len(heightMap[0]))] for j in range(len(heightMap))]  # initialse post-process HM
        #diffHM = [[0 for k in range(len(heightMap[0]))] for j in range(len(heightMap))]

        if exclusion >= len(heightMap) / 2 or exclusion >= len(heightMap[0]) / 2:
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
            999 : -1
        }
        alterDict = dict()
        alterHeightDict = dict()

        def FF(x, y, area):
            tempHM[x][y] = 999
            area.append([x,y])
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

        def FFZero(x, y, area, surroundingRegion):
            maskedHM[x][y] = 999
            area.append([x,y])
            if ((x + 1) < (len(maskedHM) - exclusion)): # go to south
                if maskedHM[x + 1][y] == "0000":
                    area, surroundingRegion = FFZero(x + 1, y, area, surroundingRegion)
            if ((y - 1) >= (0 + exclusion)):  # go to west
                if maskedHM[x][y - 1] == "0000":
                    area, surroundingRegion = FFZero(x, y - 1, area, surroundingRegion)
            if ((x - 1) >= (0 + exclusion)): # go to north
                if maskedHM[x - 1][y] == "0000":
                    area, surroundingRegion = FFZero(x - 1, y, area, surroundingRegion)
            if ((y + 1) < (len(maskedHM[x]) - exclusion)): # go to east
                if maskedHM[x][y + 1] == "0000":
                    area, surroundingRegion = FFZero(x, y + 1, area, surroundingRegion)
            
            if ((x + 1) < (len(maskedHM) - exclusion)): # go to south
                if maskedHM[x + 1][y] != "0000" and maskedHM[x + 1][y] != 999 and maskedHM[x + 1][y] not in excludedBlocks.values():
                    surroundingRegion.append(maskedHM[x + 1][y])
            if ((y - 1) >= (0 + exclusion)):  # go to west
                if maskedHM[x][y - 1] != "0000" and maskedHM[x][y - 1] != 999 and maskedHM[x][y - 1] not in excludedBlocks.values():
                    surroundingRegion.append(maskedHM[x][y - 1])
            if ((x - 1) >= (0 + exclusion)): # go to north
                if maskedHM[x - 1][y] != "0000" and maskedHM[x - 1][y] != 999 and maskedHM[x - 1][y] not in excludedBlocks.values():
                    surroundingRegion.append(maskedHM[x - 1][y])
            if ((y + 1) < (len(maskedHM[x]) - exclusion)): # go to east
                if maskedHM[x][y + 1] != "0000" and maskedHM[x][y + 1] != 999 and maskedHM[x][y + 1] not in excludedBlocks.values():
                    surroundingRegion.append(maskedHM[x][y + 1])

            return area, surroundingRegion 

        for x in range(exclusion, (len(tempHM) - exclusion)):
            for y in range(exclusion, (len(tempHM[0]) - exclusion)):
                if tempHM[x][y] < 257 and tempHM[x][y] >= -20:
                    currentLevel = tempHM[x][y]
                    regionAlias = excludedBlocks.get(currentLevel, '%04d' % currentRegion) # switch between excluded blocks and region label
                    area = FF(x, y, [])
                    
                    if len(area) >= minimumArea or currentLevel < 0: # if area greater equals to the threshold
                        for blocks in area:
                            maskedHM[blocks[0]][blocks[1]] = regionAlias
                        if currentLevel > 0:
                            regionDict[currentRegion] = currentLevel
                            currentRegion = currentRegion + 1
                    
        for x in range(exclusion, (len(maskedHM) - exclusion)):
            for y in range(exclusion, (len(maskedHM[0]) - exclusion)):
                if maskedHM[x][y] == "0000":
                    area, surroundingRegion = FFZero(x, y, [], [])
                    if len(surroundingRegion) > 0:
                        region = max(set(surroundingRegion), key=surroundingRegion.count)
                    else:
                        region =  None
                    if region != None:
                        for item in area:
                            maskedHM[item[0]][item[1]] = region
                            #diffHM[item[0]][item[1]] =  - (heightMap[item[0]][item[1]] - int((heightMap[item[0]+1][item[1]] + heightMap[item[0]-1][item[1]] + heightMap[item[0]][item[1]+1] + heightMap[item[0]][item[1]-1])/4)) if maskedHM[item[0]][item[1]] in excludedBlocks.values() else (regionDict.get(int(maskedHM[item[0]][item[1]])) - heightMap[item[0]][item[1]])
                            alterDict[item[0],item[1]] = - (heightMap[item[0]][item[1]] - int((heightMap[item[0]+1][item[1]] + heightMap[item[0]-1][item[1]] + heightMap[item[0]][item[1]+1] + heightMap[item[0]][item[1]-1])/4)) if maskedHM[item[0]][item[1]] in excludedBlocks.values() else (regionDict.get(int(maskedHM[item[0]][item[1]])) - heightMap[item[0]][item[1]])
                            alterHeightDict[item[0],item[1]] = heightMap[item[0]][item[1]]

        # afterHM = [[regionDict.get(maskedHM[j][k], tempHM[j][k]) if maskedHM[j][k] in excludedBlocks.values() else regionDict.get(int(maskedHM[j][k]), tempHM[j][k]) for k in range(len(maskedHM[j]))] for j in range(len(maskedHM))]
        # ---------------HM naming---------------
        # diffHM - List height difference before and after moderification
        # afterHM - List height after moderification
        # maskedHM - List region group after moderification

        # heightMap2File(afterHM, "HMA")
        # heightMap2File(diffHM, "HMD")
        # heightMap2File(maskedHM, "HMM")
        return alterDict, alterHeightDict # return 2D array
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
            block = 0
            if diff > 0:
                block = 2
            elif diff < 0:
                diff -= 1
            for e in xrange(abs(diff)):
                level.setBlockAt(mappedx, (alterHeightdict[x, y] + (e * (diff / abs(diff)))), mappedz, block)
    except Exception as e:
        logger.error(e)

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