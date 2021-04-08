from logger import Logger
from collections import Counter
import math


name = 'path'
logger = Logger(name)


# Buildable area filter
# =============================================================================================
def areaScreening(mapArr):
    toZero = []
    for x in range(1, len(mapArr) - 1):
        for y in range(1, len(mapArr[0]) - 1):
            if mapArr[x][y] > 0:
                plotArea = list([mapArr[i][k] for i in range(x - 1, x + 2) for k in range(y - 1, y + 2)])
                if len(set(plotArea)) == 1:
                    toZero.append([x,y])
    for cell in toZero:
        mapArr[cell[0]][cell[1]] = 0
    return mapArr

# Convert 2DArray to startingPosition
# =============================================================================================
def getStartingPosition(mapArr):
    temp = []
    for row in mapArr:
        temp.extend(row)
    noAreas = len(Counter(temp).keys()) # total number of areas including 0
    startingPositions = []
    for area in Counter(temp).keys():
        area = int(area)
        if area == 0:
            continue
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
    pos = pts[0]
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

def aStar(mapArr, treeMap, start, end):
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
        orthogonal = [[0, -1], [0, 1], [-1, 0], [1, 0]]

        # all adjacent including diagonal
        # for new_position in adjacent:

        #     if new_position in [(-1, 1), (1, 1), (-1, -1), (1, -1)]:
        #         dist = 1.4
        #     else:
        #         dist = 1.0
        
        # orthogonally adjacent
        for new_position in orthogonal:
            dist = 1.0

            node_position = [current_node.position[0] + new_position[0], current_node.position[1] + new_position[1]]

            if node_position[0] > (len(mapArr) - 1) or node_position[0] < 0 or node_position[1] > (len(mapArr[len(mapArr)-1]) -1) or node_position[1] < 0:
                # position out of range
                continue

            if mapArr[node_position[0]][node_position[1]] != 0 or treeMap[node_position[0]][node_position[1]] == 2:
                # non-walkable terrain
                continue

            new_node = Node(current_node, node_position)
            # g, h, f values
            new_node.g = current_node.g + dist
            new_node.h = euclid(node_position, end_node.position)
            new_node.f = new_node.g + new_node.h
            children.append(new_node)

        for child in children:
            VALID_FLAG = True
            for closed_child in close_list:
                if child == closed_child:
                    VALID_FLAG = False
                    # child in close list
                    continue
                if (child.position[0] == closed_child.position[0]) and (child.position[1] == closed_child.position[1]):
                    VALID_FLAG = False
                    continue
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    # greater g distance from start
                    VALID_FLAG = False
                    continue
                if (child.position[0] == open_node.position[0]) and (child.position[1] == open_node.position[1]):
                    VALID_FLAG = False
                    continue
            if VALID_FLAG:
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

                    level.setBlockAt(x, y, z, 98)
                    level.setBlockDataAt(x, y, z, 0)
                    level.setBlockAt(x, y+1, z, 0)
                    level.setBlockDataAt(x, y+1, z, 0)

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

                elif block_difference < -1: # lower
                    
                    level.setBlockAt(x, y, z, 98)
                    level.setBlockDataAt(x, y, z, 0)
                    level.setBlockAt(x, y+1, z, 0)
                    level.setBlockDataAt(x, y+1, z, 0)

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

                    level.setBlockAt(x, y, z, 98)
                    level.setBlockDataAt(x, y, z, 0)
                    level.setBlockAt(x, y+1, z, 0)
                    level.setBlockDataAt(x, y+1, z, 0)
                    
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

                elif block_difference < -1: # lower
                    # place ladder on new block

                    level.setBlockAt(x, y, z, 98)
                    level.setBlockDataAt(x, y, z, 0)
                    level.setBlockAt(x, y+1, z, 0)
                    level.setBlockDataAt(x, y+1, z, 0)
                    
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
def generatePaths(level, box, mapArr, treeMap, heightMap):
    try:

        mapArr = areaScreening(mapArr)
        startingPositions = getStartingPosition(mapArr)
        vertices = len(startingPositions)
        logger.info('Finding all possible paths...')

        # input:
        # pos = [x, z]
        # area = [pos]
        # startingPositions = [area]

        pairsList = getAllPairs(startingPositions)

        matrix = toMatrix(pairsList, vertices)
        # print(matrix)

        logger.info("Running Prim's minimum spanning tree...")

        links = primMST(vertices, matrix)

        aStarStarting = getAStarStarting(pairsList, links)
        # print('aStarStarting: ')
        # print(aStarStarting)
        logger.info('Running A* algorithm...')
        
        paths = []
        for pair in aStarStarting:
            new_map = newMap(mapArr, pair[0], pair[1])
            start = [pair[0][0], pair[0][1]]
            end = [pair[1][0], pair[1][1]]
            # print(start, end)
            path = aStar(new_map, treeMap, start, end)
            paths.append(path)
            # print(path)

        logger.info('Placing paths...')

        placePath(level, box, paths, heightMap)

        logger.info('Path generation completed.')

    except Exception as e:
        logger.error(e)