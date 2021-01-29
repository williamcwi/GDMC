from logger import Logger
import numpy as np

logger = Logger('cityPlanning')

def bestStartingPoint(box, afterHM):
    try:
        pointDict = dict()
        for x in range(4):
            for z in range(4):
                startingx, startingz, flatGrids = calculateGrids(box, afterHM, x, z)
                pointDict[str(startingx), str(startingz)] = flatGrids
        bestPoint = (max(pointDict, key = pointDict.get))
        return map(int, bestPoint)
    except Exception as e:
        logger.error(e)

def calculateGrids(box, afterHM, startingx, startingz):
    try:
        flatGrids = 0
        for z in range(startingz, box.length, 4):
            for x in range(startingx, box.width, 4):
                if(z + 4 <= box.length and x + 4 <= box.width):
                    heights = []
                    for zgrid in range(4):
                        for xgrid in range(4):
                            heights.append(afterHM[x + xgrid][z + zgrid])
                    if len(set(heights)) == 1:
                        flatGrids += 1
        return startingx, startingz, flatGrids
    except Exception as e:
        logger.error(e)