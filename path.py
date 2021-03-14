from logger import Logger
from collections import Counter
import math

name = 'path'
logger = Logger(name)


# Convert 2DArray to startingPosition
# =============================================================================================
def getStartingPosition(mapArr):
    try:
        temp = []
        for row in mapArr:
            temp.extend(row)
        noAreas = len(Counter(temp).keys()) # total number of areas including 0
        startingPositions = []
        for area in range(1, noAreas):
            a = []
            for row in range(len(mapArr)):
                for col in range(len(mapArr[row])):
                    if mapArr[row][col] == area:
                        a.append([row, col])
            startingPositions.append(a)
        
        # print(startingPositions)
        return startingPositions
        
    except Exception as e:
        logger.error(e)


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

def toMatrix(pairsList, vertices):
    try:
        INF = 999999
        graph = []
        for x in range(vertices):
            row = []
            for z in range(vertices):
                row.append(INF)
            graph.append(row)

        for i in range(len(pairsList)): # each links
            start = pairsList[i][0]
            end = pairsList[i][2]
            dist = round(pairsList[i][4])

            graph[start][end] = dist
            graph[end][start] = dist

        return graph

    except Exception as e:
        logger.error(e)


# Minimum Spanning Tree
# =============================================================================================
def minDist(vertices, key, mstSet):
    try:
        INF = 999999
        min = INF # initialise min value

        for v in range(vertices):
            
            if key[v] < min and mstSet[v] == False:
                min = key[v]
                minIndex = v
        
        return minIndex
    except Exception as e:
        logger.error(e)

def primMST(vertices, matrix):
    try:
        INF = 999999

        # key values to pick minimum weight edge
        key = []
        for v in range(vertices):
            key.append(INF)

        # parent vertex linked to
        parent = []
        for v in range(vertices):
            parent.append(None)

        key[0] = 0 # vertex 0 picked as first vertex
        parent[0] = -1 # first node does not have parent

        mstSet = []
        for v in range(vertices):
            mstSet.append(False)


        for edge in range(vertices):
            minIndex = minDist(vertices, key, mstSet)
            # print(minIndex)
            mstSet[minIndex] = True

            for v in range(vertices):
                if matrix[minIndex][v] < key[v] and mstSet[v] == False:
                    key[v] = matrix[minIndex][v]
                    parent[v] = minIndex
        
        # print(parent)

        links = []
        for link in range(1, len(parent)):
            links.append([link, parent[link]]) # buildable area index start at 1
        return links

    except Exception as e:
        logger.error(e)


# A* Algorithm
# =============================================================================================
def getAStarStarting(pairsList, links):
    aStar = []
    for link in links:
        for pair in pairsList:
            if (link[0] == pair[0] and link[1] == pair[2]) or (link[1] == pair[0] and link[0] == pair[2]):
                coord = [pair[1], pair[3]]
                aStar.append(coord)
    return aStar


# =============================================================================================
def run(mapArr):
    try:

        startingPositions = getStartingPosition(mapArr)

        vertices = len(startingPositions)

        # input: 
        # pos = [x, z]
        # area = [pos]
        # startingPositions = [area]
        pairsList = getAllPairs(startingPositions)
        # print(pairsList)

        matrix = toMatrix(pairsList, vertices)
        # print(matrix)

        links = primMST(vertices, matrix)
        # print(links)

        aStarStarting = getAStarStarting(pairsList, links)
        print('aStarStarting')
        print(aStarStarting)

    except Exception as e:
        logger.error(e)


# testing
# startingPositions = [
#     [
#         [0,11],[0,12],[0,13],[0,14],[1,11],[1,12],[1,13],[1,14],
#     ],
#     [
#         [4,14],[4,15],[4,16],[4,17],[4,18],[5,14],[5,15],[5,16],[5,17],[5,18],[6,14],[6,15],[6,16],[6,17],[6,18],[6,19],[7,14],[7,15],[7,16],[7,17],[7,18],[7,19],[8,14],[8,15],[8,16],[8,17],[8,18],[8,19],[9,14],[9,15],[9,16],[9,17],[9,18],[9,19],[10,16],[10,17],[10,18]
#     ],
#     [
#         [8,6],[8,7],[8,8],[9,6],[9,7],[9,8],[9,9],[9,10],[10,8],[10,9],[10,10],[11,8],[11,9],[11,10],[12,8],[12,9],[12,10]
#     ],
#     [
#         [13,0],[13,1],[14,0],[14,1],[15,0],[15,1],[16,0],[16,1]
#     ],
#     [
#         [13,24],[13,25],[14,24],[14,25],[15,24],[15,25],[16,24],[16,25]
#     ],
#     [
#         [15,15],[15,16],[15,17],[15,18],[15,19],[16,15],[16,16],[16,17],[16,18],[16,19],[17,14],[17,15],[17,16],[17,17],[17,18],[17,19],[18,14],[18,15],[18,16],[18,17],[18,18],[18,19],[19,14],[19,15],[19,16],[19,17],[19,18],[20,14],[20,15],[20,16],[20,17],[20,18],[21,16]
#     ],
#     [
#         [18,6],[18,7],[18,8],[18,9],[19,5],[19,6],[19,7],[19,8],[19,9],[20,6],[20,7],[20,8],[20,9],[20,10],[20,11],[21,9],[21,10],[21,11],[22,10],[22,11],[23,10],[23,11],[24,10],[24,11]
#     ],
#     [
#         [21,22],[22,21],[22,22],[23,18],[23,19],[23,20],[23,21],[23,22],[24,17],[24,18],[24,19],[24,20],[24,21],[24,22],[25,18],[25,19],[25,20],[25,21],[25,22],[26,18],[26,19],[26,20],[26,21],[26,22],[27,19],[27,20],[27,21]
#     ],
#     [
#         [28,11],[28,12],[28,13],[28,14],[29,11],[29,12],[29,13],[29,14],
#     ],
# ]


mapArr = [
    [0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,2,2,2,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,2,2,2,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,2,2,2,2,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,2,2,2,2,0,0,0,0,0,0],
    [0,0,0,0,0,0,3,3,3,0,0,0,0,0,2,2,2,2,2,2,0,0,0,0,0,0],
    [0,0,0,0,0,0,3,3,3,3,3,0,0,0,2,2,2,2,2,2,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,3,3,3,0,0,0,0,0,2,2,2,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,3,3,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,3,3,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,5],
    [4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,5],
    [4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,6,6,6,6,6,0,0,0,0,5,5],
    [4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,6,6,6,6,6,0,0,0,0,5,5],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,6,6,6,6,6,6,0,0,0,0,0,0],
    [0,0,0,0,0,0,7,7,7,7,0,0,0,0,6,6,6,6,6,6,0,0,0,0,0,0],
    [0,0,0,0,0,7,7,7,7,7,0,0,0,0,6,6,6,6,6,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,7,7,7,7,7,7,0,0,6,6,6,6,6,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,7,7,7,0,0,0,0,6,0,0,0,0,0,8,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,7,7,0,0,0,0,0,0,0,0,0,8,8,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,7,7,0,0,0,0,0,0,8,8,8,8,8,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,7,7,0,0,0,0,0,8,8,8,8,8,8,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8,8,8,8,8,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8,8,8,8,8,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8,8,8,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,9,9,9,9,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,9,9,9,9,0,0,0,0,0,0,0,0,0,0,0]
]

run(mapArr)