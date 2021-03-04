from logger import Logger
import math

name = 'path'
logger = Logger(name)


# Find the minimum distances between buildable areas/gates
# =============================================================================================

def euclid(pt1, pt2): # distance between two points
    # [x, z] coordinate of each points
    try:
        side1 = (pt2[0] - pt1[0])
        side2 = (pt2[1] - pt1[1])
        dist = math.sqrt(side1**2 + side2**2)
        return dist

    except Exception as e:
        logger.error(e)

def closest(origin, pts): # closest distance between point A and all points in array
    try:
        closestPoint = 999999
        for pt in pts:
            if euclid(origin, pt) < closestPoint:
                closestPoint = euclid(origin, pt)
                pos = pt
        return closestPoint, pos
    except Exception as e:
        logger.error(e)

def minDistance(area1, area2): # closest distance between two points arrays
    try:
        closestPoint = 999999
        for pt in area1:
            dist, pos = closest(pt, area2)
            if dist < closestPoint:
                closestPoint = dist
                pos1 = pos
                pos2 = pt
        return pos1, pos2, closestPoint
    except Exception as e:
        logger.error(e)

def getAllPairs(startingPositions):
    try:
        # pairsList = [idx1, [x1, z1], idx2, [x2, z2], dist]
        pairsList = []
        for area1 in range(len(startingPositions)):
            if area1 == len(startingPositions):
                break
            for area2 in range(area1+1, len(startingPositions)):
                pos2, pos1, dist = minDistance(startingPositions[area1], startingPositions[area2])
                pairs = [area1, pos1, area2, pos2, dist]
                pairsList.append(pairs)
        return pairsList
    except Exception as e:
        logger.error(e)

# Minimum Spanning Tree
# =============================================================================================

# A* Algorithm
# =============================================================================================

# =============================================================================================
def run():
    try:
        # input: 
        # pos = [x, z]
        # area = [pos]
        # startingPositions = [area]
        pairsList = getAllPairs(startingPositions)
        print(pairsList)
    except Exception as e:
        logger.error(e)

run()