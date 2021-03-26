from logger import Logger
import math
import numpy as np
import common

logger = Logger('cityPlanning')

def bestStartingPoint(box, afterHM):
    try:
        pointDict = dict()
        for x in range(4):
            for z in range(4):
                xoffset, zoffset, gridArray, innerGridArray, heightArray, innerHeightArray = calculateGrids(box, afterHM, x, z)
                # print(np.sum(gridArray))
                pointDict[str(xoffset), str(zoffset)] = np.sum(gridArray)
        bestPoint = (max(pointDict, key = pointDict.get))
        xoffset, zoffset, gridArray, innerGridArray, heightArray, innerHeightArray = calculateGrids(box, afterHM, int(bestPoint[0]), int(bestPoint[1]))
        return map(int, bestPoint), gridArray, innerGridArray, heightArray, innerHeightArray
    except Exception as e:
        logger.error(e)

def calculateGrids(box, afterHM, xoffset, zoffset):
    try:
        gridArray = np.full((math.ceil(box.length / 4), math.ceil(box.width / 4)), False)
        innerGridArray = np.full((math.ceil(box.length / 4), math.ceil(box.width / 4)), False)
        heightArray = np.full((math.ceil(box.length / 4), math.ceil(box.width / 4)), 0)
        innerHeightArray = np.full((math.ceil(box.length / 4), math.ceil(box.width / 4)), 0)
        tempGridArray = common.mapArray(gridArray)
        zgateWidth, xgateWidth, zgatePos, xgatePos = calculateGridPositions(np.array(tempGridArray))
        for z in range(zoffset + 12, box.length - 9, 4):
            for x in range(xoffset + 12, box.width - 9, 4):
                if(z - 1 >= 9 and z + 5 <= box.length - 9 and x - 1 >= 9 and x + 5 <= box.width - 9):
                    heights = []
                    isGateArea = False
                    for ztemp in range(4):
                        for xtemp in range(4):
                            if ((zgatePos <= z + ztemp < (zgatePos + zgateWidth) and ((10 <= x + xtemp < 15) or (len(tempGridArray) - 13 <= x + xtemp < len(tempGridArray))))):
                                    isGateArea = True
                            if ((10 <= z + ztemp < 15) or (len(tempGridArray[0]) - 13 <= z + ztemp < len(tempGridArray[0])) and (xgatePos <= x + xtemp < xgateWidth)):
                                    isGateArea = True
                    if isGateArea == False:
                        for zgrid in range(-1, 5):
                            for xgrid in range(-1, 5):
                                heights.append(afterHM[x + xgrid][z + zgrid])
                        if len(set(heights)) == 1:
                            gridArray[z / 4][x / 4] = True
                            heightArray[z / 4][x / 4] = heights[0]
                        for zgrid in range(4):
                            for xgrid in range(4):
                                heights.append(afterHM[x + xgrid][z + zgrid])
                        if len(set(heights)) == 1:
                            innerGridArray[z / 4][x / 4] = True
                            innerHeightArray[z / 4][x / 4] = heights[0]
        # for z in range(gridArray.shape[0]):
            # for x in range(gridArray.shape[1]):
                # print(heightArray[z][x])
        return xoffset, zoffset, gridArray, innerGridArray, heightArray, innerHeightArray
    except Exception as e:
        logger.error(e)

def expandBuildableAreas(level, box, afterHM, gridArray, innerGridArray, heightArray, innerHeightArray, xoffset, zoffset):
    try:
        buildableAreasArray = np.full((math.ceil(box.length / 4), math.ceil(box.width / 4)), False)
        for z in range(gridArray.shape[0]):
            for x in range(gridArray.shape[1]):
                buildableAreasArray[z][x] = getAdjacentBuildableAreas(gridArray, innerGridArray, x, z)
        for z in range(gridArray.shape[0]):
            for x in range(gridArray.shape[1]):
                if hasMostBuildableAreas(buildableAreasArray, x, z) and innerGridArray[z][x] == True and gridArray[z][x] == False:
                    print("Claiming border.")
                    claimBorder(level, box, afterHM, innerHeightArray, x, z, xoffset, zoffset)
                    gridArray[z][x] = True
                    heightArray[z][x] = innerHeightArray[z][x]
        return gridArray, heightArray
    except Exception as e:
        logger.error(e)

def getAdjacentBuildableAreas(gridArray, innerGridArray, x, z):
    try:
        adjacentBuildableAreas = 0
        if innerGridArray[z][x] == True and gridArray[z][x] == False:
            if x > 0:
                if gridArray[z][x - 1]:
                    adjacentBuildableAreas += 1
                if z > 0:
                    if gridArray[z - 1][x - 1]:
                        adjacentBuildableAreas += 1
                if z < gridArray.shape[0] - 1:
                    if gridArray[z + 1][x - 1]:
                        adjacentBuildableAreas += 1
            if x < gridArray.shape[1] - 1:
                if gridArray[z][x + 1]:
                    adjacentBuildableAreas += 1
                if z > 0:
                    if gridArray[z - 1][x + 1]:
                        adjacentBuildableAreas += 1
                if z < gridArray.shape[0] - 1:
                    if gridArray[z + 1][x + 1]:
                        adjacentBuildableAreas += 1
            if z > 0:
                if gridArray[z - 1][x]:
                    adjacentBuildableAreas += 1
            if z < gridArray.shape[0] - 1:
                if gridArray[z + 1][x]:
                    adjacentBuildableAreas += 1
    except Exception as e:
        logger.error(e)

def hasMostBuildableAreas(buildableAreasArray, x, z):
    try:
        if x > 0:
            if buildableAreasArray[z][x - 1] > buildableAreasArray[z][x]:
                return False
            if z > 0:
                if buildableAreasArray[z - 1][x - 1] > buildableAreasArray[z][x]:
                    return False
            if z < buildableAreasArray.shape[0] - 1:
                if buildableAreasArray[z + 1][x - 1] > buildableAreasArray[z][x]:
                    return False
        if x < buildableAreasArray.shape[1] - 1:
            if buildableAreasArray[z][x + 1] > buildableAreasArray[z][x]:
                return False
            if z > 0:
                if buildableAreasArray[z - 1][x + 1] > buildableAreasArray[z][x]:
                    return False
            if z < buildableAreasArray.shape[0] - 1:
                if buildableAreasArray[z + 1][x + 1] > buildableAreasArray[z][x]:
                    return False
        if z > 0:
            if buildableAreasArray[z - 1][x] > buildableAreasArray[z][x]:
                return False
        if z < buildableAreasArray.shape[0] - 1:
            if buildableAreasArray[z + 1][x] > buildableAreasArray[z][x]:
                return False
        return True
    except Exception as e:
        logger.error(e)

def claimBorder(level, box, afterHM, innerHeightArray, x, z, xoffset, zoffset):
    try:
        for zgrid in range(-1, 5):
            for xgrid in range(-1, 5):
                xpos = (x * 4) + xoffset + xgrid
                zpos = (z * 4) + zoffset + zgrid
                ypos = afterHM[xpos][zpos]
                if innerHeightArray[z][x] < ypos:
                    while innerHeightArray[z][x] < ypos:
                        level.setBlockAt(box.minx + xpos, ypos, box.minz + zpos, 0)
                        ypos -= 1
                if innerHeightArray[z][x] > ypos:
                    while innerHeightArray[z][x] > ypos:
                        block = level.blockAt(box.minx + xpos, ypos, box.minz + zpos)
                        level.setBlockAt(box.minx + xpos, ypos, box.minz + zpos, block)
                        ypos += 1
    except Exception as e:
        logger.error(e)

def addBorder(level, box, gridArray, heightArray, xoffset, zoffset):
    try:
        for z in range(gridArray.shape[0]):
            for x in range(gridArray.shape[1]):
                if westBorder(gridArray, heightArray, x, z):
                    for n in range(4):
                        level.setBlockAt(box.minx + (x * 4) + xoffset - 1, heightArray[z][x] - 1, box.minz + (z * 4) + zoffset + n, 109)
                        level.setBlockDataAt(box.minx + (x * 4) + xoffset - 1, heightArray[z][x] - 1, box.minz + (z * 4) + zoffset + n, 1)
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
                        level.setBlockDataAt(box.minx + (x * 4) + xoffset + 4, heightArray[z][x] - 1, box.minz + (z * 4) + zoffset + n, 0)
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
                        level.setBlockDataAt(box.minx + (x * 4) + xoffset + n, heightArray[z][x] - 1, box.minz + (z * 4) + zoffset - 1, 3)
                if southBorder(gridArray, heightArray, x, z):
                    for n in range(4):
                        level.setBlockAt(box.minx + (x * 4) + xoffset + n, heightArray[z][x] - 1, box.minz + (z * 4) + zoffset + 4, 109)
                        level.setBlockDataAt(box.minx + (x * 4) + xoffset + n, heightArray[z][x] - 1, box.minz + (z * 4) + zoffset + 4, 2)
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

def createBuildableAreaArray(level, box, afterHM, gridArray, heightArray, xoffset, zoffset):
    try:
        gridArray = np.array(gridArray)
        heightArray = np.array(heightArray)
        buildableAreaArray = np.full((box.length, box.width), 0)
        zgateWidth, xgateWidth, zgatePos, xgatePos = calculateGridPositions(gridArray)
        for z in range(zgateWidth):
            for x in range(5):
                buildableAreaArray[zgatePos + z][9 + x] = 2
                buildableAreaArray[zgatePos + z][(gridArray.shape[1] - 13) + x] = 3
        for z in range(5):
            for x in range(xgateWidth):
                buildableAreaArray[9 + z][xgatePos + x] = 1
                buildableAreaArray[(gridArray.shape[0] - 13) + z][xgatePos + x] = 4
        currentID = 5
        buildableArea = False
        for z in range(gridArray.shape[0]):
            for x in range(gridArray.shape[1]):
                numAdjacent = 0
                if x < gridArray.shape[1] - 1:
                    if z > 0 and buildableAreaArray[z][x] == 0:
                        xtemp = x
                        while gridArray[z][xtemp] and heightArray[z][xtemp] == heightArray[z][x]:
                            if gridArray[z - 1][xtemp] and heightArray[z - 1][xtemp] == heightArray[z][x] and buildableAreaArray[z][x] == 0:
                                buildableAreaArray[z][x] = buildableAreaArray[z - 1][xtemp]
                                buildableArea = True
                            xtemp += 1
                    if(gridArray[z][x] and heightArray[z][x + 1] == heightArray[z][x]):
                        if buildableAreaArray[z][x] == 0:
                            buildableAreaArray[z][x] = currentID
                            numAdjacent += 1
                            buildableArea = True
                        if buildableAreaArray[z][x + 1] == 0:
                            buildableAreaArray[z][x + 1] = buildableAreaArray[z][x]
                if z < gridArray.shape[0] - 1:
                    if(gridArray[z][x] and heightArray[z + 1][x] == heightArray[z][x]):
                        if buildableAreaArray[z][x] == 0:
                            buildableAreaArray[z][x] = currentID
                            numAdjacent += 1
                            buildableArea = True
                        if buildableAreaArray[z + 1][x] == 0:
                            buildableAreaArray[z + 1][x] = buildableAreaArray[z][x]
                if(numAdjacent == 0 and buildableArea):
                    currentID += 1
                    buildableArea = False
        return buildableAreaArray
    except Exception as e:
        logger.error(e)

def calculateGridPositions(gridArray):
    try:
        zgateWidth = (gridArray.shape[0] - 16) % 8
        while zgateWidth < 6:
            zgateWidth += 4
        xgateWidth = (gridArray.shape[1] - 16) % 8
        while xgateWidth < 6:
            xgateWidth += 4
        zleft = 0
        xleft = 0
        zlength = gridArray.shape[0] - 16
        xlength = gridArray.shape[1] - 16
        if (zlength - zgateWidth) / 4 % 2 == 0:
            zleft = (zlength - zgateWidth) / 8
        else:
            zleft = (((zlength - zgateWidth) - 4) / 8)
        if (xlength - xgateWidth) / 4 % 2 == 0:
            xleft = (xlength - xgateWidth) / 8
        else:
            xleft = (((xlength - xgateWidth) - 4) / 8)
        zgatePos = 6 + (zleft *4)
        xgatePos = 6 + (xleft *4)
        return zgateWidth + 4, xgateWidth + 4, zgatePos, xgatePos
    except Exception as e:
        logger.error(e)