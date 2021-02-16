from logger import Logger
import math
import numpy as np

logger = Logger('cityPlanning')

def bestStartingPoint(box, afterHM):
    try:
        pointDict = dict()
        for x in range(4):
            for z in range(4):
                xoffset, zoffset, gridArray, heightArray = calculateGrids(box, afterHM, x, z)
                # print(np.sum(gridArray))
                pointDict[str(xoffset), str(zoffset)] = np.sum(gridArray)
        bestPoint = (max(pointDict, key = pointDict.get))
        xoffset, zoffset, gridArray, heightArray = calculateGrids(box, afterHM, int(bestPoint[0]), int(bestPoint[1]))
        return map(int, bestPoint), gridArray, heightArray
    except Exception as e:
        logger.error(e)

def calculateGrids(box, afterHM, xoffset, zoffset):
    try:
        gridArray = np.full((math.ceil(box.length/4), math.ceil(box.width/4)), False)
        heightArray = np.full((math.ceil(box.length/4), math.ceil(box.width/4)), 0)
        for z in range(zoffset + 9, box.length - 9, 4):
            for x in range(xoffset + 9, box.width - 9, 4):
                if(z - 1 >= 9 and z + 5 <= box.length - 9 and x - 1 >= 9 and x + 5 <= box.width - 9):
                    heights = []
                    for zgrid in range(-1, 5):
                        for xgrid in range(-1, 5):
                            heights.append(afterHM[x + xgrid][z + zgrid])
                    if len(set(heights)) == 1:
                        gridArray[z / 4][x / 4] = True
                        heightArray[z / 4][x / 4] = heights[0]
        for z in range(gridArray.shape[0]):
            for x in range(gridArray.shape[1]):
                print(heightArray[z][x])
        return xoffset, zoffset, gridArray, heightArray
    except Exception as e:
        logger.error(e)

def addBorder(level, box, afterHM, gridArray, heightArray, xoffset, zoffset):
    try:
        for z in range(gridArray.shape[0]):
            for x in range(gridArray.shape[1]):
                if westBorder(gridArray, heightArray, x, z):
                    for n in range(4):
                        level.setBlockAt(box.minx + (x * 4) + xoffset - 1, heightArray[z][x] - 1, box.minz + (z * 4) + zoffset + n, 109)
                    if northBorder(gridArray, heightArray, x, z):
                        if x > 0 and z > 0:
                            if southBorder(gridArray, heightArray, x - 1, z - 1) == False:
                                level.setBlockAt(box.minx + (x * 4) + xoffset - 1, heightArray[z][x] - 1, box.minz + (z * 4) + zoffset - 1, 109)
                    if southBorder(gridArray, heightArray, x, z):
                        if x > 0 and z < gridArray.shape[0] - 1:
                            if northBorder(gridArray, heightArray, x - 1, z + 1) == False:
                                level.setBlockAt(box.minx + (x * 4) + xoffset - 1, heightArray[z][x] - 1, box.minz + (z * 4) + zoffset + 4, 109)
                if eastBorder(gridArray, heightArray, x, z):
                    for n in range(4):
                        level.setBlockAt(box.minx + (x * 4) + xoffset + 4, heightArray[z][x] - 1, box.minz + (z * 4) + zoffset + n, 109)
                    if northBorder(gridArray, heightArray, x, z):
                        if x < gridArray.shape[1] - 1 and z > 0:
                            if southBorder(gridArray, heightArray, x + 1, z - 1) == False:
                                level.setBlockAt(box.minx + (x * 4) + xoffset + 4, heightArray[z][x] - 1, box.minz + (z * 4) + zoffset - 1, 109)
                    if southBorder(gridArray, heightArray, x, z):
                        if x < gridArray.shape[1] - 1 and z < gridArray.shape[0] - 1:
                            if northBorder(gridArray, heightArray, x + 1, z + 1) == False:
                                level.setBlockAt(box.minx + (x * 4) + xoffset + 4, heightArray[z][x] - 1, box.minz + (z * 4) + zoffset + 4, 109)
                if northBorder(gridArray, heightArray, x, z):
                    for n in range(4):
                        level.setBlockAt(box.minx + (x * 4) + xoffset + n, heightArray[z][x] - 1, box.minz + (z * 4) + zoffset - 1, 109)
                if southBorder(gridArray, heightArray, x, z):
                    for n in range(4):
                        level.setBlockAt(box.minx + (x * 4) + xoffset + n, heightArray[z][x] - 1, box.minz + (z * 4) + zoffset + 4, 109)
    except Exception as e:
        logger.error(e)

def westBorder(gridArray, heightArray, x, z):
    try:
        if x == 0:
            if gridArray[z][x]:
                return True
        else:
            if gridArray[z][x]:
                if gridArray[z][x - 1] == False:
                    return True
                if gridArray[z][x - 1] and heightArray[z][x] != heightArray[z][x - 1]:
                    return True
            return False
    except Exception as e:
        logger.error(e)

def eastBorder(gridArray, heightArray, x, z):
    try:
        if x == gridArray.shape[1] - 1:
            if gridArray[z][x]:
                return True
        else:
            if gridArray[z][x]:
                if gridArray[z][x + 1] == False:
                    return True
                if gridArray[z][x + 1] and heightArray[z][x] != heightArray[z][x + 1]:
                    return True
            return False
    except Exception as e:
        logger.error(e)

def northBorder(gridArray, heightArray, x, z):
    try:
        if z == 0:
            if gridArray[z][x]:
                return True
        else:
            if gridArray[z][x]:
                if gridArray[z - 1][x] == False:
                    return True
                if gridArray[z - 1][x] and heightArray[z][x] != heightArray[z - 1][x]:
                    return True
            return False
    except Exception as e:
        logger.error(e)

def southBorder(gridArray, heightArray, x, z):
    try:
        if z == gridArray.shape[0] - 1:
            if gridArray[z][x]:
                return True
        else:
            if gridArray[z][x]:
                if gridArray[z + 1][x] == False:
                    return True
                if gridArray[z + 1][x] and heightArray[z][x] != heightArray[z + 1][x]:
                    return True
            return False
    except Exception as e:
        logger.error(e)