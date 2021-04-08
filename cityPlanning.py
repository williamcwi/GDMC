from logger import Logger
import math
import numpy as np
import common
from copy import deepcopy

name = 'cityPlanning'
logger = Logger(name)

def bestStartingPoint(box, afterHM):
    try:
        logger.info('Calculating optimal starting x and z coordinates for grid...')
        pointDict = dict()
        for x in range(4):
            for z in range(4):
                # Iterate through all 16 combinations of x and z offset
                xoffset, zoffset, gridArray, innerGridArray, heightArray, innerHeightArray = calculateGrids(box, afterHM, x, z)
                pointDict[str(xoffset), str(zoffset)] = np.sum(gridArray)
        # Find the x and z offset resulting in the highest number of flat 4x4 areas
        bestPoint = (max(pointDict, key = pointDict.get))
        # This becomes the starting point for the grid
        xoffset, zoffset, gridArray, innerGridArray, heightArray, innerHeightArray = calculateGrids(box, afterHM, int(bestPoint[0]), int(bestPoint[1]))
        logger.info('Placing grid with x offset {} and z offset {}'.format(xoffset, zoffset))
        return map(int, bestPoint), gridArray, innerGridArray, heightArray, innerHeightArray
    except Exception as e:
        logger.error(e)

def calculateGrids(box, afterHM, xoffset, zoffset):
    try:
        gridArray = np.full((math.ceil(float(box.length) / 4), math.ceil(float(box.width) / 4)), False)
        innerGridArray = np.full((math.ceil(float(box.length) / 4), math.ceil(float(box.width) / 4)), False)
        heightArray = np.full((math.ceil(float(box.length) / 4), math.ceil(float(box.width) / 4)), 0)
        innerHeightArray = np.full((math.ceil(float(box.length) / 4), math.ceil(float(box.width) / 4)), 0)
        tempGridArray = common.mapArray(gridArray, 0, 0, box)
        zgateWidth, xgateWidth, zgatePos, xgatePos = calculateGridPositions(np.array(tempGridArray))
        for z in range(zoffset + 12, box.length - 9, 4):
            for x in range(xoffset + 12, box.width - 9, 4):
                if(z - 1 >= 9 and z + 5 <= box.length - 9 and x - 1 >= 9 and x + 5 <= box.width - 9):
                    heights = []
                    isGateArea = False
                    # Check that the 4x4 area does not overlap with where the gate entrances will be placed
                    for ztemp in range(-1, 5):
                        for xtemp in range(-1, 5):
                            if (((zgatePos <= (z + ztemp) < (zgatePos + zgateWidth)) and ((10 <= (x + xtemp) < 15) or ((len(tempGridArray[0]) - 13) <= (x + xtemp) < len(tempGridArray[0]))))):
                                    isGateArea = True
                                    break
                            if (((10 <= (z + ztemp) < 15) or ((len(tempGridArray) - 13) <= (z + ztemp) < len(tempGridArray))) and (xgatePos <= (x + xtemp) < (xgatePos + xgateWidth))):
                                    isGateArea = True
                                    break
                            if isGateArea:
                                break
                    # Only attempt to label the 4x4 area as buildable if it is not a gate area
                    if isGateArea == False:
                        for zgrid in range(-1, 5):
                            for xgrid in range(-1, 5):
                                heights.append(afterHM[x + xgrid][z + zgrid])
                        if len(set(heights)) == 1 and heights[0] > 0:
                            # If entire 6x6 area containing 4x4 has the same height level, label it as a buildable area. The 6x6 is checked so that a border can be added
                            gridArray[z / 4][x / 4] = True
                            heightArray[z / 4][x / 4] = heights[0]
                        for zgrid in range(4):
                            for xgrid in range(4):
                                heights.append(afterHM[x + xgrid][z + zgrid])
                        if len(set(heights)) == 1 and heights[0] > 0:
                            # An "inner" buildable area is one in which the 4x4 area is flat, but the 6x6 containing it is not
                            innerGridArray[z / 4][x / 4] = True
                            innerHeightArray[z / 4][x / 4] = heights[0]
        return xoffset, zoffset, gridArray, innerGridArray, heightArray, innerHeightArray
    except Exception as e:
        logger.error(e)

def expandBuildableAreas(level, box, afterHM, gridArray, innerGridArray, heightArray, innerHeightArray, xoffset, zoffset):
    try:
        logger.info('Expanding buildable areas...')
        buildableAreasArray = np.full((math.ceil(float(box.length) / 4), math.ceil(float(box.width) / 4)), 0)
        for z in range(gridArray.shape[0]):
            for x in range(gridArray.shape[1]):
                buildableAreasArray[z][x] = getAdjacentBuildableAreas(gridArray, innerGridArray, x, z)
        for z in range(gridArray.shape[0]):
            for x in range(gridArray.shape[1]):
                if hasMostBuildableAreas(buildableAreasArray, x, z) and innerGridArray[z][x] == True and gridArray[z][x] == False:
                    # "Claim" a border adjacent to multiple other buildable areas. Only the largest adjacent buildable area is allowed to claim the border
                    logger.info('Claiming border at region {},{}'.format(x, z))
                    claimBorder(level, box, afterHM, innerHeightArray, x, z, xoffset, zoffset)
                    # Set the corresponding 6x6 area to buildable, as it has now been claimed
                    gridArray[z][x] = True
                    heightArray[z][x] = innerHeightArray[z][x]
        return gridArray, heightArray
    except Exception as e:
        logger.error(e)

def getAdjacentBuildableAreas(gridArray, innerGridArray, x, z):
    try:
        adjacentBuildableAreas = 0
        if innerGridArray[z][x] == True and gridArray[z][x] == False:
            # Add up the number of adjacent 4x4 buildable areas
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
        return adjacentBuildableAreas
    except Exception as e:
        logger.error(e)

def hasMostBuildableAreas(buildableAreasArray, x, z):
    try:
        # Compares a buildable area with all adjacent areas to find which one is connected to the most buildable areas
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
                # "Claims" border by raising/lowering the height level of each block to that of the inner area
                if innerHeightArray[z][x] < ypos:
                    while innerHeightArray[z][x] < ypos:
                        # Lowers the height level
                        level.setBlockAt(box.minx + xpos, ypos, box.minz + zpos, 0)
                        ypos -= 1
                if innerHeightArray[z][x] > ypos:
                    while innerHeightArray[z][x] > ypos:
                        # Raises the height level
                        block = level.blockAt(box.minx + xpos, ypos, box.minz + zpos)
                        level.setBlockAt(box.minx + xpos, ypos, box.minz + zpos, block)
                        ypos += 1
    except Exception as e:
        logger.error(e)

def addBorder(level, box, gridArray, heightArray, xoffset, zoffset):
    try:
        logger.info('Adding stone brick borders...')
        for z in range(gridArray.shape[0]):
            for x in range(gridArray.shape[1]):
                # Adds stone brick borders around buildable areas in all four cardinal directions, then adds corner stairs as necessary.
                if westBorder(gridArray, heightArray, x, z):
                    for n in range(4):
                        level.setBlockAt(box.minx + (x * 4) + xoffset - 1, heightArray[z][x] - 1, box.minz + (z * 4) + zoffset + n, 109)
                        level.setBlockDataAt(box.minx + (x * 4) + xoffset - 1, heightArray[z][x] - 1, box.minz + (z * 4) + zoffset + n, 1)
                    if northBorder(gridArray, heightArray, x, z):
                        if x > 0 and z > 0:
                            if southBorder(gridArray, heightArray, x - 1, z - 1) == False and level.blockAt(box.minx + (x * 4) + xoffset - 1, heightArray[z][x] - 1, box.minz + (z * 4) + zoffset - 1) != 109:
                                level.setBlockAt(box.minx + (x * 4) + xoffset - 1, heightArray[z][x] - 1, box.minz + (z * 4) + zoffset - 1, 109)
                                level.setBlockDataAt(box.minx + (x * 4) + xoffset - 1, heightArray[z][x] - 1, box.minz + (z * 4) + zoffset - 1, 1)
                    if southBorder(gridArray, heightArray, x, z):
                        if x > 0 and z < gridArray.shape[0] - 1:
                            if northBorder(gridArray, heightArray, x - 1, z + 1) == False and level.blockAt(box.minx + (x * 4) + xoffset - 1, heightArray[z][x] - 1, box.minz + (z * 4) + zoffset + 4) != 109:
                                level.setBlockAt(box.minx + (x * 4) + xoffset - 1, heightArray[z][x] - 1, box.minz + (z * 4) + zoffset + 4, 109)
                                level.setBlockDataAt(box.minx + (x * 4) + xoffset - 1, heightArray[z][x] - 1, box.minz + (z * 4) + zoffset + 4, 1)
                if eastBorder(gridArray, heightArray, x, z):
                    for n in range(4):
                        level.setBlockAt(box.minx + (x * 4) + xoffset + 4, heightArray[z][x] - 1, box.minz + (z * 4) + zoffset + n, 109)
                        level.setBlockDataAt(box.minx + (x * 4) + xoffset + 4, heightArray[z][x] - 1, box.minz + (z * 4) + zoffset + n, 0)
                    if northBorder(gridArray, heightArray, x, z):
                        if x < gridArray.shape[1] - 1 and z > 0:
                            if southBorder(gridArray, heightArray, x + 1, z - 1) == False and level.blockAt(box.minx + (x * 4) + xoffset + 4, heightArray[z][x] - 1, box.minz + (z * 4) + zoffset - 1) != 109:
                                level.setBlockAt(box.minx + (x * 4) + xoffset + 4, heightArray[z][x] - 1, box.minz + (z * 4) + zoffset - 1, 109)
                                level.setBlockDataAt(box.minx + (x * 4) + xoffset + 4, heightArray[z][x] - 1, box.minz + (z * 4) + zoffset - 1, 0)
                    if southBorder(gridArray, heightArray, x, z):
                        if x < gridArray.shape[1] - 1 and z < gridArray.shape[0] - 1:
                            if northBorder(gridArray, heightArray, x + 1, z + 1) == False and level.blockAt(box.minx + (x * 4) + xoffset + 4, heightArray[z][x] - 1, box.minz + (z * 4) + zoffset + 4) != 109:
                                level.setBlockAt(box.minx + (x * 4) + xoffset + 4, heightArray[z][x] - 1, box.minz + (z * 4) + zoffset + 4, 109)
                                level.setBlockDataAt(box.minx + (x * 4) + xoffset + 4, heightArray[z][x] - 1, box.minz + (z * 4) + zoffset + 4, 0)
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
        logger.info('Labelling buildable areas...')
        gridArray = np.array(gridArray)
        heightArray = np.array(heightArray)
        buildableAreaArray = np.full((box.length, box.width), 0)
        zgateWidth, xgateWidth, zgatePos, xgatePos = calculateGridPositions(buildableAreaArray)
        # Adds the north, west, east, and south gates as the first areas to connect, labelled 1 through 4
        for z in range(zgateWidth):
            for x in range(5):
                buildableAreaArray[zgatePos + z][9 + x] = 2
                buildableAreaArray[zgatePos + z][(buildableAreaArray.shape[1] - 14) + x] = 3
        for z in range(5):
            for x in range(xgateWidth):
                buildableAreaArray[9 + z][xgatePos + x] = 1
                buildableAreaArray[(buildableAreaArray.shape[0] - 14) + z][xgatePos + x] = 4
        currentID = 5
        buildableArea = False
        for z in range(buildableAreaArray.shape[0]):
            for x in range(buildableAreaArray.shape[1]):
                numAdjacent = 0
                # Labels all blocks that are part of buildable areas, ensuring each area has a unique identifying number
                if x < buildableAreaArray.shape[1] - 1:
                    if z > 0 and buildableAreaArray[z][x] == 0:
                        ztemp = z
                        xtemp = x
                        xAreasToCheck = True
                        zAreasToCheck = True
                        # Checks if the current block connects to any existing buildable areas. If so, labels it with the same number
                        while zAreasToCheck:
                            while xAreasToCheck:
                                if gridArray[ztemp - 1][xtemp] and heightArray[ztemp - 1][xtemp] == heightArray[z][x] and buildableAreaArray[z][x] == 0 and buildableAreaArray[ztemp - 1][xtemp] > 4:
                                    buildableAreaArray[z][x] = buildableAreaArray[ztemp - 1][xtemp]
                                    buildableArea = True
                                if gridArray[ztemp][xtemp] and heightArray[ztemp][xtemp] == heightArray[z][x]:
                                    xtemp += 1
                                else:
                                    xtemp = x
                                    if ztemp < buildableAreaArray.shape[0] - 1:
                                        ztemp += 1
                                    xAreasToCheck = False
                            if gridArray[ztemp][xtemp] and heightArray[ztemp][xtemp] == heightArray[z][x]:
                                xAreasToCheck = True
                            else:
                                zAreasToCheck = False
                    if(gridArray[z][x] and heightArray[z][x + 1] == heightArray[z][x]):
                        if buildableAreaArray[z][x] == 0:
                            buildableAreaArray[z][x] = currentID
                            numAdjacent += 1
                            buildableArea = True
                        if buildableAreaArray[z][x + 1] == 0 and buildableAreaArray[z][x] > 4:
                            buildableAreaArray[z][x + 1] = buildableAreaArray[z][x]
                if z < buildableAreaArray.shape[0] - 1:
                    if(gridArray[z][x] and heightArray[z + 1][x] == heightArray[z][x]):
                        if buildableAreaArray[z][x] == 0:
                            buildableAreaArray[z][x] = currentID
                            numAdjacent += 1
                            buildableArea = True
                        if buildableAreaArray[z + 1][x] == 0 and buildableAreaArray[z][x] > 4:
                            buildableAreaArray[z + 1][x] = buildableAreaArray[z][x]
                if(numAdjacent == 0 and buildableArea):
                    # Iterates to the next number once it has run out of blocks to label with the existing one
                    currentID += 1
                    buildableArea = False
        tempBuildableAreaArray = np.copy(buildableAreaArray)
        # Adds the border blocks to the buildable area labelling
        for z in range(9, buildableAreaArray.shape[0] - 9):
            for x in range(9, buildableAreaArray.shape[1] - 9):
                if buildableAreaArray[z - 1][x] > 4 and buildableAreaArray[z][x] == 0:
                    tempBuildableAreaArray[z][x] = buildableAreaArray[z - 1][x]
                if buildableAreaArray[z - 1][x + 1] > 4 and buildableAreaArray[z][x] == 0:
                    tempBuildableAreaArray[z][x] = buildableAreaArray[z - 1][x + 1]
                if buildableAreaArray[z][x + 1] > 4 and buildableAreaArray[z][x] == 0:
                    tempBuildableAreaArray[z][x] = buildableAreaArray[z][x + 1]
                if buildableAreaArray[z + 1][x + 1] > 4 and buildableAreaArray[z][x] == 0:
                    tempBuildableAreaArray[z][x] = buildableAreaArray[z + 1][x + 1]
                if buildableAreaArray[z + 1][x] > 4 and buildableAreaArray[z][x] == 0:
                    tempBuildableAreaArray[z][x] = buildableAreaArray[z + 1][x]
                if buildableAreaArray[z + 1][x - 1] > 4 and buildableAreaArray[z][x] == 0:
                    tempBuildableAreaArray[z][x] = buildableAreaArray[z + 1][x - 1]
                if buildableAreaArray[z][x - 1] > 4 and buildableAreaArray[z][x] == 0:
                    tempBuildableAreaArray[z][x] = buildableAreaArray[z][x - 1]
                if buildableAreaArray[z - 1][x - 1] > 4 and buildableAreaArray[z][x] == 0:
                    tempBuildableAreaArray[z][x] = buildableAreaArray[z - 1][x - 1]
        buildableAreaArray = np.copy(tempBuildableAreaArray) 
        return buildableAreaArray
    except Exception as e:
        logger.error(e)

def calculateGridPositions(array):
    try:
        # Calculates where the gate entrances for the walls will be. Used in several methods to avoid overlap with buildable areas
        zgateWidth = (array.shape[0] - 16) % 8
        while zgateWidth < 6:
            zgateWidth += 4
        xgateWidth = (array.shape[1] - 16) % 8
        while xgateWidth < 6:
            xgateWidth += 4
        zleft = 0
        xleft = 0
        zlength = array.shape[0] - 16
        xlength = array.shape[1] - 16
        if (zlength - zgateWidth) / 4 % 2 == 0:
            zleft = (zlength - zgateWidth) / 8
        else:
            zleft = (((zlength - zgateWidth) - 4) / 8)
        if (xlength - xgateWidth) / 4 % 2 == 0:
            xleft = (xlength - xgateWidth) / 8
        else:
            xleft = (((xlength - xgateWidth) + 4) / 8)
        zgatePos = 6 + (zleft *4)
        xgatePos = 6 + (xleft *4)
        return zgateWidth + 4, xgateWidth + 4, zgatePos, xgatePos
    except Exception as e:
        logger.error(e)

def screening(gridArray):
    try:
        tempGA = deepcopy(gridArray)
        def FFFF (x, y, area):
            area.append([x,y])
            stonks = []
            stonks.append([x,y])
            length = len(stonks)
            tempGA[x][y] = 999

            while length >= 1:
                x = stonks[0][0]
                y = stonks[0][1]
                stonks.pop(0)
                if ((y - 1) >= (0)): # go to west
                    if tempGA[x][y - 1] == 1:
                        stonks.append([x, y - 1])
                        area.append([x, y - 1])
                        tempGA[x][y - 1] = 999
                if ((y + 1) < (len(tempGA[x]))): # go to east
                    if tempGA[x][y + 1] == 1:
                        stonks.append([x, y + 1])
                        area.append([x, y + 1])
                        tempGA[x][y + 1] = 999
                if ((x + 1) < (len(tempGA))): # go to south
                    if tempGA[x + 1][y] == 1:
                        stonks.append([x + 1, y])
                        area.append([x + 1, y])
                        tempGA[x + 1][y] = 999
                if ((x - 1) >= (0)): # go to north
                    if tempGA[x - 1][y] == 1:
                        stonks.append([x - 1, y])
                        area.append([x - 1, y])
                        tempGA[x - 1][y] = 999
                length = len(stonks)
            return area
        
        for x in range((len(tempGA))):
            for y in range((len(tempGA[0]))):
                if tempGA[x][y] == 1:
                    area = FFFF(x, y, [])
                    if len(area) <= 4:
                        for cell in area:
                            gridArray[cell[0]][cell[1]] = 0
                    else:
                        valid = False
                        for cell in area: # check if area contains minimum 2 x 2 (8 x 8) area
                            if cell[0] + 2 < len(gridArray) and cell[1] + 2 < len(gridArray[0]):
                                plotArea = list([gridArray[i][k] for i in range(cell[0], cell[0] + 2) for k in range(cell[1], cell[1] + 2)])
                                if sum(plotArea) == 4:
                                    valid = True
                                    break
                        if not valid:
                            for cell in area:
                                gridArray[cell[0]][cell[1]] = 0
        return gridArray
    except Exception as e:
        logger.error(e)