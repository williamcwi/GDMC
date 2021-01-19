import numpy as np
import pandas as pd
import scipy as sp

import platform
import os.path
import datetime

import sys
sys.setrecursionlimit(65536) #!!IMPORTANT to allow CCL2DFF and CCL3DFF RECURSIVE

heightmap = input()
df = pd.read_csv('{}'.format(heightmap), header=None, delimiter=r'\s+')

data = df.to_numpy()

# Translates 2D array to 3D Binary array
def heightmap2binary(data):
    binary_heightmap = []
    for height in range(min(map(min, data)), max(map(max, data))+1): # for height in dataset
        new_heightmap = []
        for i in data: # row
            new_row = []
            for j in i:
                if (j == height): # if cell matches current height
                    new_row.append(1)
                else:
                    new_row.append(0)
            new_heightmap.append(new_row)
        binary_heightmap.append(new_heightmap)
    # print(binary_heightmap)
    return binary_heightmap

# Connected Component Labelling
def CCL(heightMap): ################# TODO:VERIFY #################
    region = 1 # region label
    minHM = min(map(min,heightMap)) # get lowerbound of level
    maxHM = max(map(max,heightMap)) # get upperbound of level
    maskedHM = [[[0 for k in range(len(heightMap))] for j in range(len(heightMap[0]))] for i in range((maxHM - minHM) + 1)] # initialse post-process HM

    for x in range(len(heightMap)): # for row
        for z in range(len(heightMap[x])): # for column
            upregion = leftregion = -1 # initalise neighbour region
            uplevel = leftlevel = 999 # initalise neighbour level
            level = heightMap[x][z]
            maskedlevel = level - minHM
            if level >= 0: # if not lava or water
                if x - 1 >= 0:
                    if heightMap[x-1][z] == level:
                        upregion = maskedHM[maskedlevel][x-1][z]
                        uplevel = heightMap[x-1][z]
                if z - 1 >= 0:
                    if heightMap[x][z-1] == level:
                        leftregion = maskedHM[maskedlevel][x][z-1]
                        leftlevel = heightMap[x][z-1]
                
                if level == uplevel or level == leftlevel:
                    if leftregion > 0 != upregion > 0:# if only one neighbour belongs to a region
                        maskedHM[maskedlevel][x][z] = max(leftregion, upregion)
                    elif (leftregion > 0 and upregion > 0) and (leftregion != upregion) and (level == leftlevel and level == uplevel):# if conflicts
                        min_region, max_region = min(leftregion, upregion), max(leftregion, upregion)
                        maskedHM[maskedlevel][x][z] = max_region
                        maskedHM[maskedlevel] = [[e if e!=max_region else min_region for e in r] for r in maskedHM[maskedlevel]]
                else: # if new region
                    maskedHM[maskedlevel][x][z] = region
                    region = region + 1
    #heightMap2File(maskedHM[0])
    return maskedHM

def CCL2DFF(heightMap, minimumArea, exclusion = 0): # CCL2D via Flood Fill RECURSIVE ################# POC OK TODO:VERIFY #################
    tempHM = heightMap.copy()
    maskedHM = [['%04d' % 0 for k in range(len(heightMap[0]))] for j in range(len(heightMap))]  # initialse post-process HM
    diffHM = [[0 for k in range(len(heightMap[0]))] for j in range(len(heightMap))]

    if exclusion >= len(heightMap) / 2 or exclusion >= len(heightMap[0]) / 2:
        print("Invalid Exclusion block width")
        return maskedHM

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

    def CCL(x, y, area):
        tempHM[x][y] = 999
        area.append([x,y])
        if ((y - 1) >= (0 + exclusion)):  # go to west
            if tempHM[x][y - 1] == currentLevel:
                area = CCL(x, y - 1, area)
        if ((y + 1) < (len(tempHM[x]) - exclusion)): # go to east
            if tempHM[x][y + 1] == currentLevel:
                area = CCL(x, y + 1, area)
        if ((x + 1) < (len(tempHM) - exclusion)): # go to south
            if tempHM[x + 1][y] == currentLevel:
                area = CCL(x + 1, y, area)
        if ((x - 1) >= (0 + exclusion)): # go to north
            if tempHM[x - 1][y] == currentLevel:
                area = CCL(x - 1, y, area)
        return area

    def CCLZero(x, y, area, surroundingRegion):
        maskedHM[x][y] = 999
        area.append([x,y])
        if ((x + 1) < (len(maskedHM) - exclusion)): # go to south
            if maskedHM[x + 1][y] == "0000":
                area, surroundingRegion = CCLZero(x + 1, y, area, surroundingRegion)
        if ((y - 1) >= (0 + exclusion)):  # go to west
            if maskedHM[x][y - 1] == "0000":
                area, surroundingRegion = CCLZero(x, y - 1, area, surroundingRegion)
        if ((x - 1) >= (0 + exclusion)): # go to north
            if maskedHM[x - 1][y] == "0000":
                area, surroundingRegion = CCLZero(x - 1, y, area, surroundingRegion)
        if ((y + 1) < (len(maskedHM[x]) - exclusion)): # go to east
            if maskedHM[x][y + 1] == "0000":
                area, surroundingRegion = CCLZero(x, y + 1, area, surroundingRegion)
        
        if ((x + 1) < (len(maskedHM) - exclusion)): # go to south
            if maskedHM[x + 1][y] != "0000" and maskedHM[x + 1][y] != 999 and maskedHM[x + 1][y] not in excludedBlocks.values():
                surroundingRegion.append(maskedHM[x + 1][y])
        if ((y - 1) >= (0 + exclusion)):  # go to west
            if maskedHM[x][y - 1] != "0000" and maskedHM[x][y - 1] != 999 and maskedHM[x][y - 1] not in excludedBlocks.values():
                surroundingRegion.append(maskedHM[x][y - 1])
        if ((x - 1) >= (0 + exclusion)): # go to north
            if maskedHM[x + 1][y] != "0000" and maskedHM[x + 1][y] != 999 and maskedHM[x - 1][y] not in excludedBlocks.values():
                surroundingRegion.append(maskedHM[x + 1][y])
        if ((y + 1) < (len(maskedHM[x]) - exclusion)): # go to east
            if maskedHM[x][y + 1] != "0000" and maskedHM[x][y + 1] != 999 and maskedHM[x][y + 1] not in excludedBlocks.values():
                surroundingRegion.append(maskedHM[x][y + 1])

        return area, surroundingRegion 

    for x in range(exclusion, (len(tempHM) - exclusion)):
        for y in range(exclusion, (len(tempHM[0]) - exclusion)):
            if tempHM[x][y] < 257 and tempHM[x][y] >= -20:
                currentLevel = tempHM[x][y]
                regionAlias = excludedBlocks.get(currentLevel, '%04d' % currentRegion) # switch between excluded blocks and region label
                area = CCL(x, y, [])
                
                if len(area) >= minimumArea or currentLevel < 0: # if area greater equals to the threshold
                    for blocks in area:
                        maskedHM[blocks[0]][blocks[1]] = regionAlias
                    if currentLevel > 0:
                        regionDict[currentRegion] = currentLevel
                        currentRegion = currentRegion + 1
                
    for x in range(exclusion, (len(maskedHM) - exclusion)):
        for y in range(exclusion, (len(maskedHM[0]) - exclusion)):
            if maskedHM[x][y] == "0000":
                area, surroundingRegion = CCLZero(x, y, [], [])
                if len(surroundingRegion) > 0:
                    region = max(set(surroundingRegion), key=surroundingRegion.count)
                else:
                    region =  None
                if region != None:
                    for item in area:
                        maskedHM[item[0]][item[1]] = region
                        diffHM[item[0]][item[1]] =  - (heightMap[item[0]][item[1]] - regionDict.get(maskedHM[item[0]][item[1]])) if maskedHM[item[0]][item[1]] in excludedBlocks.values() else (regionDict.get(int(maskedHM[item[0]][item[1]])) - heightMap[item[0]][item[1]])

    afterHM = [[regionDict.get(maskedHM[j][k], tempHM[j][k]) if maskedHM[j][k] in excludedBlocks.values() else regionDict.get(int(maskedHM[j][k]), tempHM[j][k]) for k in range(len(maskedHM[j]))] for j in range(len(maskedHM))]
    # ---------------HM naming---------------
    # diffHM - List height difference before and after moderification
    # afterHM - List height after moderification
    # maskedHM - List region group after moderification

    heightMap2File(afterHM, "HMA")
    heightMap2File(diffHM, "HMD")
    heightMap2File(maskedHM, "HMM")
    return maskedHM # return 2D array

def CCL3DFF(heightMap, minimumArea, exclusion = 0): # CCL3D via Flood Fill RECURSIVE ################# NOT TESTED TODO:VERIFY #################
    tempHM = heightMap.copy()
    minHM = min(map(min,heightMap)) 
    maskedHM = [[['%04d' % 0 for k in range(len(heightMap[0]))] for j in range(len(heightMap))] for i in range((max(map(max,heightMap)) - min(map(min,heightMap))))]  # initialse post-process HM
    if exclusion >= len(heightMap) / 2 or exclusion >= len(heightMap[0]) / 2 :
        print("Invalid Exclusion block width")
        return maskedHM

    currentLevel = 999
    currentRegion = 1
    excludedBlocks = { # excluded blocks - excluded from labelling 
        -1 : "wate",
        -2 : "lava"
    }

    def CCL(x, y, HMLevel, area):
        tempHM[x][y] = -999 
        if ((x + 1) < len(tempHM[x]) - exclusion): # go to east
            if tempHM[x + 1][y] == currentLevel:
                area = CCL(x + 1, y, HMLevel, area + 1)
        if ((x - 1) >= 0 + exclusion): # go to west
            if tempHM[x - 1][y] == currentLevel:
                area = CCL(x - 1, y, HMLevel, area + 1)
        if ((y + 1) < len(tempHM) - exclusion): # go to north
            if tempHM[x][y + 1] == currentLevel:
                area = CCL(x, y + 1, HMLevel, area + 1)
        if ((y - 1) >= 0 + exclusion): # go to south
            if tempHM[x][y - 1] == currentLevel:
                area = CCL(x, y - 1, HMLevel, area + 1)
        if area > minimumArea: # if area greater the threshold
            maskedHM[HMLevel][x][y] = regionAlias
        return area

    for x in range(exclusion, len(tempHM) - exclusion):
        for y in range(exclusion, len(tempHM[0]) - exclusion):
            if tempHM[x][y] < 257 and tempHM[x][y] >= -900:
                currentLevel = tempHM[x][y]
                regionAlias = excludedBlocks.get(currentLevel, '%04d' % currentRegion) # switch between excluded blocks and region label
                HMLevel = currentLevel - minHM
                area = CCL(x, y, HMLevel, 1)
                if area > minimumArea:
                    currentRegion = currentRegion + 1

    return maskedHM # return 3D array

def heightMap2File(heightMap, HMname = "HMS"):
    if platform.system()==("Darwin") and int(platform.release()[:2]) >= 19:
        with open(os.path.join(os.path.expanduser("~/Desktop"), HMname + '-'+ datetime.datetime.now().strftime('%H%M%S') +'.txt'), 'w+') as f:
            np.savetxt(f, heightMap, fmt='%s')
            f.close()
    else:
        with open(HMname + '-' + datetime.datetime.now().strftime('%H%M%S') +'.txt', 'w+') as f:
            np.savetxt(f, heightMap, fmt='%s')
            f.close()


    # # Sobel Operator
    # edge_map = []
    # for i in range(len(new_heightmap)): # row
    #     if i == 0:
    #         edge_map.append(np.zeros(256).astype(int).tolist())
    #     else:
    #         edge_row = []
    #         for j, k in zip(new_heightmap[i], new_heightmap[i-1]): # compare current row and previous row
    #             if j == k:
    #                 edge_row.append(0)
    #             else:
    #                 edge_row.append(1)
    #         edge_map.append(edge_row)
    # print(edge_map)

CCL2DFF(data, 169, 9)

# CCL(data)