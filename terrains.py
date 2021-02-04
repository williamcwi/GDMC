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
                    region =  None
                    if len(surroundingRegion) > 0:
                        region = max(set(surroundingRegion), key=surroundingRegion.count)   
                    if region != None and len(area) <= (minimumArea*4):
                        for item in area:
                            maskedHM[item[0]][item[1]] = region
                            #diffHM[item[0]][item[1]] =  - (heightMap[item[0]][item[1]] - int((heightMap[item[0]+1][item[1]] + heightMap[item[0]-1][item[1]] + heightMap[item[0]][item[1]+1] + heightMap[item[0]][item[1]-1])/4)) if maskedHM[item[0]][item[1]] in excludedBlocks.values() else (regionDict.get(int(maskedHM[item[0]][item[1]])) - heightMap[item[0]][item[1]])
                            alterDict[item[0],item[1]] = - (heightMap[item[0]][item[1]] - int((heightMap[item[0]+1][item[1]] + heightMap[item[0]-1][item[1]] + heightMap[item[0]][item[1]+1] + heightMap[item[0]][item[1]-1])/4)) if maskedHM[item[0]][item[1]] in excludedBlocks.values() else (regionDict.get(int(maskedHM[item[0]][item[1]])) - heightMap[item[0]][item[1]])
                            alterHeightDict[item[0],item[1]] = heightMap[item[0]][item[1]]

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
        return heightmap.heightMap(level, box)

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
                    block = level.blockAt(x, oldy, z)
                    while oldy > newy:
                        level.setBlockAt(x, oldy, z, 0)
                        oldy -= 1
                    level.setBlockAt(x, oldy, z, block)
                if ydiff > 0:
                    oldy = oldHeightMap[zpos][xpos]
                    newy = oldy + ydiff
                    block = level.blockAt(x, oldy, z)
                    while oldy == newy:
                        oldy += 1
                        level.setBlockAt(x, oldy, z, block)
                xpos += 1
            zpos += 1
    except Exception as e:
        logger.error(e)

def pavingGate(level, box, heightMap):
    alterDict = dict()

    def getGatePostion(boxwidth):
        left = 0
        right = 0
        gate = boxwidth % 8
        if gate == 0:
            gate = 8
        else:
            while gate < 6:
                gate = gate + 4

        if (boxwidth - gate - 16) / 4 % 2 == 0:
            left = right = (boxwidth - gate - 16) / 8
        else:
            left = (((boxwidth - gate - 16) - 4) / 8)
            right = left + 1
        return left, right, gate

    left, right, gate = getGatePostion(box.maxx - box.minx)
    plat_pos_1 = heightMap[(right * 4) + 7][1] - 1
    plat_pos_3 = heightMap[((right * 4) + 7)][(len(heightMap[(((right) * 4) + 8)]) - 2)] - 1
    g1area=[]
    g3area=[]

    for z in range(((right * 4) + 6 - 20), ((right * 4) + 10 + gate + 20)): # Getting area to test bottom section
        for x in range(0,33):
            g1area.append(heightMap[z][x])
        for x in range(len(heightMap[0]) - 14 - 20,len(heightMap[0])):
            g3area.append(heightMap[z][x])

    for z in range(((right * 4) + 6), ((right * 4) + 10 + gate)):
        for x in range(0, 14):
            level.setBlockAt((box.minx + z), plat_pos_1, (box.minz + x), 43) # Making the base of plaza
            level.setBlockDataAt((box.minx + z), plat_pos_1, (box.minz + x), 0)
            if heightMap[z][x] > (plat_pos_1 + 20):
                for d in range((plat_pos_1 + 20), heightMap[z][x]): # Remove blocks above the plaza and wall
                    level.setBlockAt((box.minx + z), d, (box.minz + x), 0)

        for x in range(len(heightMap[0]) - 14, len(heightMap[0])):
            level.setBlockAt((box.minx + z), plat_pos_3, (box.minz + x), 43) # Making the base of plaza
            level.setBlockDataAt((box.minx + z), plat_pos_3, (box.minz + x), 0)
            if heightMap[z][x] > (plat_pos_3 + 20):
                for d in range((plat_pos_3 + 20), heightMap[z][x]): # Remove blocks above the plaza and wall
                    level.setBlockAt((box.minx + z), d, (box.minz + x), 0)

    mean_g1 = sum(g1area) / len(g1area) # calc stats
    mode_g1 = max(set(g1area), key=g1area.count)
    mean_g3 = sum(g3area) / len(g3area)
    mode_g3 = max(set(g3area), key=g3area.count)

    for y in range(1,20):
        for z in range(((right * 4) + 6 - y), ((right * 4) + 10 + gate + y)):
            for x in range(0, 14 + y):
                level.setBlockAt((box.minx + z), plat_pos_1 + y, (box.minz + x), 0) # clearing top section in stair shape
                if (plat_pos_1 - mean_g1 < 20) and (plat_pos_1 - mode_g1 < 20): # if the can reach the bottom
                    level.setBlockAt((box.minx + z), plat_pos_1 - y, (box.minz + x), 43) # create stair to bottom
                    level.setBlockDataAt((box.minx + z), plat_pos_1 - y, (box.minz + x), 0)

            for x in range(len(heightMap[0]) - 14 - y,len(heightMap[0])):
                level.setBlockAt((box.minx + z), plat_pos_3 + y, (box.minz + x), 0) # clearing top section in stair shape
                if (plat_pos_3 - mean_g3 < 20) and (plat_pos_3 - mode_g3 < 20): # if the can reach the bottom
                    level.setBlockAt((box.minx + z), plat_pos_3 - y, (box.minz + x), 43) # create stair to bottom
                    level.setBlockDataAt((box.minx + z), plat_pos_3 - y, (box.minz + x), 0)

    left, right, gate = getGatePostion(box.maxz - box.minz)
    plat_pos_2 = heightMap[1][(left * 4) + 7] - 1
    plat_pos_4 = heightMap[(len(heightMap) - 2)][(left * 4) + 7] - 1
    g2area=[]
    g4area=[]

    for i in range(((left * 4) + 6 - 20), ((left * 4) + 10 + gate + 20)):
        for x in range(0, 33):
            g2area.append(heightMap[x][i])
        for x in range(len(heightMap) - 34,len(heightMap)):
            g4area.append(heightMap[x][i])

    for z in range(((left * 4) + 6), ((left * 4) + 10 + gate)):
        for x in range(0, 14):
            level.setBlockAt((box.minx + x), plat_pos_2, (box.minz + z), 43) # Making the base of plaza
            level.setBlockDataAt((box.minx + x), plat_pos_2, (box.minz + z), 0)
            if heightMap[x][z] > (plat_pos_2 + 20):
                for d in range((plat_pos_2 + 20), heightMap[x][z]): # Remove blocks above the plaza and wall
                    level.setBlockAt((box.minx + x), d, (box.minz + z), 0)

        for x in range(len(heightMap) - 14, len(heightMap)):
            level.setBlockAt((box.minx + x), plat_pos_4, (box.minz + z), 43) # Making the base of plaza
            level.setBlockDataAt((box.minx + x), plat_pos_4, (box.minz + z), 0)
            if heightMap[x][z] > (plat_pos_4 + 20):
                    for d in range((plat_pos_4 + 20), heightMap[x][z]): # Remove blocks above the plaza and wall
                        level.setBlockAt((box.minx + x), d, (box.minz + z), 0)

    mean_g2 = sum(g2area) / len(g2area)
    mode_g2 = max(set(g2area), key=g2area.count)
    mean_g4 = sum(g4area) / len(g4area)
    mode_g4 = max(set(g4area), key=g4area.count)

    for y in range(1,20):
        for z in range(((left * 4) + 6 - y), ((left * 4) + 10 + gate) + y):
            for x in range(0, 14 + y): #West
                level.setBlockAt((box.minx + x), plat_pos_2 + y, (box.minz + z), 0) # clearing top section in stair shape
                if (plat_pos_2 - mean_g2 < 20) and (plat_pos_2 - mode_g2 < 20): # if the can reach the bottom
                    level.setBlockAt((box.minx + x), plat_pos_2 - y, (box.minz + z), 43) # create stair to bottom
                    level.setBlockDataAt((box.minx + x), plat_pos_2 - y, (box.minz + z), 0)
                
            for x in range(len(heightMap) - 14 - y,len(heightMap)): #East
                level.setBlockAt((box.minx + x), plat_pos_4 + y, (box.minz + z), 0) # clearing top section in stair shape
                if (plat_pos_4 - mean_g4 < 20) and (plat_pos_4 - mode_g4 < 20): # if the can reach the bottom
                    level.setBlockAt((box.minx + x), plat_pos_4 - y, (box.minz + z), 43) # create stair to bottom
                    level.setBlockDataAt((box.minx + x), plat_pos_4 - y, (box.minz + z), 0)


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
