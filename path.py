from logger import Logger
from collections import Counter
import math

name = 'path'
logger = Logger(name)


# Convert 2DArray to startingPosition
# =============================================================================================
def getStartingPosition(mapArr):
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


# Find the minimum distances between buildable areas/gates
# =============================================================================================

def euclid(pt1, pt2): # distance between two points
    # [x, z] coordinate of each points
    side1 = (pt2[0] - pt1[0])
    side2 = (pt2[1] - pt1[1])
    dist = math.sqrt(side1**2 + side2**2)
    return dist


def closest(origin, pts): # closest distance between point A and all points in array
    closestPoint = 999999
    for pt in pts:
        if euclid(origin, pt) < closestPoint:
            closestPoint = euclid(origin, pt)
            pos = pt
    return closestPoint, pos

def minDistance(area1, area2): # closest distance between two points arrays
    closestPoint = 999999
    for pt in area1:
        dist, pos = closest(pt, area2)
        if dist < closestPoint:
            closestPoint = dist
            pos1 = pos
            pos2 = pt
    return pos1, pos2, closestPoint

def getAllPairs(startingPositions):
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

def toMatrix(pairsList, vertices):
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


# Minimum Spanning Tree
# =============================================================================================
def minDist(vertices, key, mstSet):
    INF = 999999
    min = INF # initialise min value

    for v in range(vertices):

        if key[v] < min and mstSet[v] == False:
            min = key[v]
            minIndex = v

    return minIndex

def primMST(vertices, matrix):
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


# A* Algorithm
# =============================================================================================
def getAStarStarting(pairsList, links):
    a_star = []
    for link in links:
        for pair in pairsList:
            if (link[0] == pair[0] and link[1] == pair[2]) or (link[1] == pair[0] and link[0] == pair[2]):
                coord = [pair[1], pair[3]]
                a_star.append(coord)
    return a_star

class Node():
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        
        self.g = 0
        self.h = 0
        self.f = 0
    
    def __eq__(self, other):
        return self.position == other.position

def aStar(mapArr, start, end):
    # input: mapArr, start pos and end pos (map, (x1, z1), (x2, z2))

    # initialise open and close list
    open_list = [] # nodes visited but not expanded
    close_list = [] # nodes visited and expanded

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = 0
    start_node.h = euclid(start, end)
    start_node.f = start_node.g + start_node.h

    end_node = Node(None, end)
    end_node.g = 999999
    end_node.h = 0
    end_node.f = end_node.g + end_node.h

    # add start node to open list
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0:

        # get current node (lowest f)
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index
        open_list.pop(current_index) # remove current node from open list
        close_list.append(current_node) # add current node to close list

        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            reversed_path = path[::-1]
            return reversed_path

        # generate children
        children = []

        adjacent = [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        orthogonal = [(0, -1), (0, 1), (-1, 0), (1, 0)]

        # all adjacent including diagonal
        # for new_position in adjacent:

        #     if new_position in [(-1, 1), (1, 1), (-1, -1), (1, -1)]:
        #         dist = 1.4
        #     else:
        #         dist = 1.0
        
        # orthogonally adjacent
        for new_position in orthogonal:
            dist = 1.0

            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            if node_position[0] > (len(mapArr) - 1) or node_position[0] < 0 or node_position[1] > (len(mapArr[len(mapArr)-1]) -1) or node_position[1] < 0:
                # position out of range
                continue

            if mapArr[node_position[0]][node_position[1]] != 0:
                # non-walkable terrain
                continue

            new_node = Node(current_node, node_position)
            # g, h, f values
            new_node.g = current_node.g + dist
            new_node.h = euclid(node_position, end_node.position)
            new_node.f = new_node.g + new_node.h
            children.append(new_node)

        for child in children:
            for closed_child in close_list:
                if child == closed_child:
                    # child in close list
                    continue
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    # greater g distance from start
                    continue
            open_list.append(child)

def newMap(mapArr, start, end):
    mapArr[start[0]][start[1]] = 0
    mapArr[end[0]][end[1]] = 0
    # print(mapArr)
    return mapArr


# Placing path
# =============================================================================================
def placePath(level, box, paths, heightMap):
    print(paths)
    for path in paths:
        block_difference = 0
        previous_block = None
        for idx, block in enumerate(path):
            if idx == 0:
                # initiate block height
                previous_block = block
            elif idx == (len(path)-1):
                
                x = box.minx + block[1]
                y = heightMap[block[1]][block[0]] - 1
                z = box.minz + block[0]

                # find out if blocks are more than 1 block high
                previous_height = heightMap[previous_block[1]][previous_block[0]] - 1
                block_difference = y - previous_height

                if block_difference > 1: # higher

                    # find ladder position
                    if block[0] > previous_block[0]:
                        position = 2 # north
                    elif block[0] < previous_block[0]:
                        position = 3 # south
                    elif block[1] > previous_block[1]:
                        position = 4 # west
                    elif block[1] < previous_block[1]:
                        position = 5 # east

                    previous_x = box.minx + previous_block[1]
                    previous_y = heightMap[previous_block[1]][previous_block[0]] - 1
                    previous_z = box.minz + previous_block[0]

                    for ladder_increment in range(1, abs(block_difference)):

                        level.setBlockAt(x, previous_y + ladder_increment, z, 98)
                        level.setBlockDataAt(x, previous_y + ladder_increment, z, 0)

                        level.setBlockAt(previous_x, previous_y + ladder_increment, previous_z, 65)
                        level.setBlockDataAt(previous_x, previous_y + ladder_increment, previous_z, position)

                    level.setBlockAt(previous_x, y, previous_z, 65)
                    level.setBlockDataAt(previous_x, y, previous_z, position)

                elif block_difference < 1: # lower
                    
                    # find ladder position
                    if block[0] > previous_block[0]:
                        position = 3 # south
                    elif block[0] < previous_block[0]:
                        position = 2 # north
                    elif block[1] > previous_block[1]:
                        position = 5 # east
                    elif block[1] < previous_block[1]:
                        position = 4 # west

                    previous_x = box.minx + previous_block[1]
                    previous_y = heightMap[previous_block[1]][previous_block[0]] - 1
                    previous_z = box.minz + previous_block[0]

                    for ladder_increment in range(1, abs(block_difference)):
                        
                        level.setBlockAt(previous_x, y + ladder_increment, previous_z, 98)
                        level.setBlockDataAt(previous_x, y + ladder_increment, previous_z, 0)

                        level.setBlockAt(x, y + ladder_increment, z, 65)
                        level.setBlockDataAt(x, y + ladder_increment, z, position)
                    
                    level.setBlockAt(x, previous_y, z, 65)
                    level.setBlockDataAt(x, previous_y, z, position)
            else:
                x = box.minx + block[1]
                y = heightMap[block[1]][block[0]] - 1
                z = box.minz + block[0]

                # find out if blocks are more than 1 block high
                previous_height = heightMap[previous_block[1]][previous_block[0]] - 1
                block_difference = y - previous_height

                previous_x = box.minx + previous_block[1]
                previous_y = heightMap[previous_block[1]][previous_block[0]] - 1
                previous_z = box.minz + previous_block[0]

                if -1 <= block_difference <= 1:
                    level.setBlockAt(x, y, z, 98)
                    level.setBlockDataAt(x, y, z, 0)
                elif block_difference > 1: # higher
                    # place ladder on previous block
                    
                    # find ladder position
                    if block[0] > previous_block[0]:
                        position = 2 # north
                    elif block[0] < previous_block[0]:
                        position = 3 # south
                    elif block[1] > previous_block[1]:
                        position = 4 # west
                    elif block[1] < previous_block[1]:
                        position = 5 # east

                    for ladder_increment in range(1, abs(block_difference) + 1):

                        level.setBlockAt(x, previous_y + ladder_increment, z, 98)
                        level.setBlockDataAt(x, previous_y + ladder_increment, z, 0)

                        level.setBlockAt(previous_x, previous_y + ladder_increment, previous_z, 65)
                        level.setBlockDataAt(previous_x, previous_y + ladder_increment, previous_z, position)

                elif block_difference < 1: # lower
                    # place ladder on new block
                    
                    # find ladder position
                    if block[0] > previous_block[0]:
                        position = 3 # south
                    elif block[0] < previous_block[0]:
                        position = 2 # north
                    elif block[1] > previous_block[1]:
                        position = 5 # east
                    elif block[1] < previous_block[1]:
                        position = 4 # west

                    for ladder_increment in range(1, abs(block_difference) + 1):
                        
                        level.setBlockAt(previous_x, y + ladder_increment, previous_z, 98)
                        level.setBlockDataAt(previous_x, y + ladder_increment, previous_z, 0)

                        level.setBlockAt(x, y + ladder_increment, z, 65)
                        level.setBlockDataAt(x, y + ladder_increment, z, position)
                
                # update previous block
                previous_block = block


# =============================================================================================
def generatePaths(level, box, mapArr, heightMap):
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
        # print('aStarStarting: ')
        # print(aStarStarting)
        
        paths = []
        for pair in aStarStarting:
            new_map = newMap(mapArr, pair[0], pair[1])
            start = (pair[0][0], pair[0][1])
            end = (pair[1][0], pair[1][1])
            # print(start, end)
            path = aStar(new_map, start, end)
            paths.append(path)
            # print(path)

        placePath(level, box, paths, heightMap)

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


# mapArr = [
#     [0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0],
#     [0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0],
#     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,2,2,2,0,0,0,0,0,0,0],
#     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,2,2,2,0,0,0,0,0,0,0],
#     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,2,2,2,2,0,0,0,0,0,0],
#     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,2,2,2,2,0,0,0,0,0,0],
#     [0,0,0,0,0,0,3,3,3,0,0,0,0,0,2,2,2,2,2,2,0,0,0,0,0,0],
#     [0,0,0,0,0,0,3,3,3,3,3,0,0,0,2,2,2,2,2,2,0,0,0,0,0,0],
#     [0,0,0,0,0,0,0,0,3,3,3,0,0,0,0,0,2,2,2,0,0,0,0,0,0,0],
#     [0,0,0,0,0,0,0,0,3,3,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#     [0,0,0,0,0,0,0,0,3,3,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#     [4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,5],
#     [4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,5],
#     [4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,6,6,6,6,6,0,0,0,0,5,5],
#     [4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,6,6,6,6,6,0,0,0,0,5,5],
#     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,6,6,6,6,6,6,0,0,0,0,0,0],
#     [0,0,0,0,0,0,7,7,7,7,0,0,0,0,6,6,6,6,6,6,0,0,0,0,0,0],
#     [0,0,0,0,0,7,7,7,7,7,0,0,0,0,6,6,6,6,6,0,0,0,0,0,0,0],
#     [0,0,0,0,0,0,7,7,7,7,7,7,0,0,6,6,6,6,6,0,0,0,0,0,0,0],
#     [0,0,0,0,0,0,0,0,0,7,7,7,0,0,0,0,6,0,0,0,0,0,8,0,0,0],
#     [0,0,0,0,0,0,0,0,0,0,7,7,0,0,0,0,0,0,0,0,0,8,8,0,0,0],
#     [0,0,0,0,0,0,0,0,0,0,7,7,0,0,0,0,0,0,8,8,8,8,8,0,0,0],
#     [0,0,0,0,0,0,0,0,0,0,7,7,0,0,0,0,0,8,8,8,8,8,8,0,0,0],
#     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8,8,8,8,8,0,0,0],
#     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8,8,8,8,8,0,0,0],
#     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8,8,8,0,0,0,0],
#     [0,0,0,0,0,0,0,0,0,0,0,9,9,9,9,0,0,0,0,0,0,0,0,0,0,0],
#     [0,0,0,0,0,0,0,0,0,0,0,9,9,9,9,0,0,0,0,0,0,0,0,0,0,0]
# ]

# run(mapArr)

