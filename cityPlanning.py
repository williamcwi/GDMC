from logger import Logger
import math
import numpy as np

logger = Logger('cityPlanning')

def bestStartingPoint(box, afterHM):
    try:
        pointDict = dict()
        for x in range(4):
            for z in range(4):
                startingx, startingz, gridArray = calculateGrids(box, afterHM, x, z)
                # print(np.sum(gridArray))
                pointDict[str(startingx), str(startingz)] = np.sum(gridArray)
        bestPoint = (max(pointDict, key = pointDict.get))
        startingx, startingz, gridArray = calculateGrids(box, afterHM, int(bestPoint[0]), int(bestPoint[1]))
        return map(int, bestPoint), gridArray
    except Exception as e:
        logger.error(e)

def calculateGrids(box, afterHM, startingx, startingz):
    try:
        gridArray = np.full((math.ceil(box.length/4), math.ceil(box.width/4)), False)
        for z in range(startingz, box.length, 4):
            for x in range(startingx, box.width, 4):
                if(z + 4 <= box.length and x + 4 <= box.width):
                    heights = []
                    for zgrid in range(4):
                        for xgrid in range(4):
                            heights.append(afterHM[x + xgrid][z + zgrid])
                    if len(set(heights)) == 1:
                        gridArray[z/4][x/4] = True
        # for z in range(gridArray.shape[0]):
            # for x in range(gridArray.shape[1]):
                # print(gridArray[z][x])
        return startingx, startingz, gridArray
    except Exception as e:
        logger.error(e)