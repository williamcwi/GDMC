import math
import random
import os
import common
import cityPlanning
from logger import Logger

import sys
import numpy

from pymclevel import MCSchematic
from pymclevel.box import Vector

name = 'treePlacement'
logger = Logger(name)

# add gates in mapArr - needs to be 13 blocks away from edge 
def reassignGate(mapArr):
    for z in range(len(mapArr)):
        for x in range(len(mapArr[z])):
            if z < 13 or x < 13 or z > len(mapArr)-14 or x > len(mapArr[z])-14:
                mapArr[z][x] = 1
    return mapArr

# find all the possible tree positions   
def findPosition(level, box):
    try:
        trees = []
        start = [box.minx, box.minz]
       
        # loops through the z-axis within the box selection and dividing it into 11 sections 
        for z in range(int(math.ceil((box.maxz-(box.minz))/11))):
            tempStart = [start[0]-z, start[1]+(11*z)]
            if z == 1:
                bottomStart = trees[len(trees)-1]
            # loops through the x-axis within the box selection and dividing it into 11 sections
            for x in range(int(math.ceil((box.maxx-(box.minx-z))/11))):
                position = [tempStart[0]+(11*x), tempStart[1]+x]
                # checks if the position is within the box x-axis selection and box z-axis selection
                if box.minx < position[0] < box.maxx and box.minz < position[1] < box.maxz:
                    trees.append(position)
                else:
                    if position[0] < box.maxx and position[1] < box.maxz:
                        continue
                    else:
                        break
        
        for z in range(int(math.ceil((box.maxz-(box.minz))/11))):
            tempStart = [bottomStart[0]+z, bottomStart[1]-(11*z)]
            if z == 0:
                pass
            for x in range(int(math.ceil((box.maxx-(box.minx-z))/11))):
                position = [tempStart[0]-(11*x), tempStart[1]-x]
                if box.minx < position[0] < box.maxx and box.minz < position[1] < box.maxz:
                    trees.append(position)
                    if position in trees:
                        trees.pop()
                        break
                else: 
                    if position[0] > box.minx and position[1] > box.minz:
                        continue
                    else:
                        break

        for t in trees:
            t[0] -= box.minx
            t[1] -= box.minz
        return trees
    
    except Exception as e:
        logger.error(e)

# checks the buildableAreaArray with the trees array
def compareTreePosition(pos, mapArr, afterHM):
    try:
        # checks the adjacent area around the tree position
        adj = [(0, 0), (0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        
        for newPos in adj:
            z = pos[0] + newPos[0]
            x = pos[1] + newPos[1]
            if z < len(mapArr[0]) and x < len(mapArr) and z > 0 and x > 0:
                # checks if it is water or lava
                if mapArr[x][z] != 0 or afterHM[z][x] == -1 or afterHM[z][x] == -2:
                    return False
        return True

    except Exception as e:
        logger.error(e)

# checks adjacent area of the 3x3 tree pos
def treePositions(trees, mapArr, afterHM):
    try:
        for idx, pos in reversed(list(enumerate(trees))): 
            adj = [(0, 0), (0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]

            randPlot = random.randint(0, len(adj)-1)
            z = pos[0] + adj[randPlot][0]
            x = pos[1] + adj[randPlot][1]

            stop = False

            while compareTreePosition([z, x], mapArr, afterHM) == False:
                adj.pop(randPlot)

                if len(adj) == 0:
                    trees.pop(idx)
                    stop = True
                    break

                randPlot = random.randint(0, len(adj)-1)
                z = pos[0] + adj[randPlot][0]
                x = pos[1] + adj[randPlot][1]

            if stop is not True:
                trees[idx] = [z, x]

        return trees

    except Exception as e:
        logger.error(e)

# generates the trees in the postions
def generateTrees(heightMap, trees, level, box):
    #loads the schematics
    tree_type = '1'
    filename = os.path.join(os.path.dirname(__file__), 'schematics', 'tree', 'tree_{}.schematic'.format(tree_type))
    tree_1 = MCSchematic(shape=(7,10,8), filename=filename)

    tree_type = '2'
    filename = os.path.join(os.path.dirname(__file__), 'schematics', 'tree', 'tree_{}.schematic'.format(tree_type))
    tree_2 = MCSchematic(shape=(5,6,5), filename=filename)

    tree_type = '3'
    filename = os.path.join(os.path.dirname(__file__), 'schematics', 'tree', 'tree_{}.schematic'.format(tree_type))
    tree_3 = MCSchematic(shape=(7,10,7), filename=filename)

    tree_type = '3'
    filename = os.path.join(os.path.dirname(__file__), 'schematics', 'tree', 'tree_{}.schematic'.format(tree_type))
    tree_4 = MCSchematic(shape=(6,6,6), filename=filename)

    tree_type = '5'
    filename = os.path.join(os.path.dirname(__file__), 'schematics', 'tree', 'tree_{}.schematic'.format(tree_type))
    tree_5 = MCSchematic(shape=(8,9,8), filename=filename)

    tree_type = '6'
    filename = os.path.join(os.path.dirname(__file__), 'schematics', 'tree', 'tree_{}.schematic'.format(tree_type))
    tree_6 = MCSchematic(shape=(8,10,8), filename=filename)

    #loops through the available tree plots
    for pos in trees:
        x = pos[0] + box.minx
        y = heightMap[pos[0]][pos[1]]
        z = pos[1] + box.minz

        random_tree = random.randint(1, 6)

        if random_tree == 1:
            level.copyBlocksFrom(tree_1, tree_1.bounds, Vector(x-3, y, z-4))
        elif random_tree == 2:
            level.copyBlocksFrom(tree_2, tree_2.bounds, Vector(x-2, y, z-2))
        elif random_tree == 3:
            level.copyBlocksFrom(tree_3, tree_3.bounds, Vector(x-3, y, z-3))
        elif random_tree == 4:
            level.copyBlocksFrom(tree_4, tree_4.bounds, Vector(x-2, y, z-3))
        elif random_tree == 5:
            level.copyBlocksFrom(tree_5, tree_5.bounds, Vector(x-4, y, z-3))
        else:
            level.copyBlocksFrom(tree_6, tree_6.bounds, Vector(x-4, y, z-3))

# creates tree map
def createTreeMap(box, trees):
    try:
        # create map of zeros
        treeMap = []
        for z in range(box.length):
            row = []
            for x in range(box.width):
                row.append(0)
            treeMap.append(row)
        print(len(treeMap))

        # loops through trees and adjacent blocks
        for validTree in trees:
            adj = [(0, 0), (0, -1), (0, 1), (-1, 0), (1, 0)]
            for treeArea in adj:
                z = validTree[0] + treeArea[0]
                x = validTree[1] + treeArea[1]
                if treeArea == (0, 0):
                    treeMap[x][z] = 2
                else: 
                    treeMap[x][z] = 1

        return treeMap
     
    except Exception as e:
        logger.error(e)

# acts as controller 
def treePlacement(level, box, mapArr, afterHM):
    try:
        logger.info('Generating trees...')
        paddedMapArr = mapArr.copy()
        trees = findPosition(level, box)
        paddedMapArr = reassignGate(paddedMapArr)
        # updates trees array
        trees = treePositions(trees, paddedMapArr, afterHM)
        generateTrees(afterHM, trees, level, box)
        treeMap = createTreeMap(box, trees)
        return treeMap
    except Exception as e:
        logger.error(e)