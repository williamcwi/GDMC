import math
import random
import os
import common
import cityPlanning
from logger import Logger

import sys
import numpy
# numpy.set_printoptions(threshold=sys.maxsize)

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
            # # checks if the start is within the box x-axis selection and z-axis selection
            # if box.minx <= tempStart[0] <= box.maxx and box.minz <= tempStart[1] <= box.maxz:
            #     trees.append(tempStart)
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
            # if box.minx <= tempStart[0] <= box.maxx and box.minz <= tempStart[1] <= box.maxz:
            #     trees.append(tempStart)
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
        #print(trees)
        for t in trees:
            t[0] -= box.minx
            t[1] -= box.minz
        return trees
    
    except Exception as e:
        logger.error(e)


# checks the mapArr with the trees array
def compareTreePosition(trees, mapArr):
    try:
        # print mapArr
        # print(trees)
        # print(len(trees))
        for pos in reversed(trees): 
            z = pos[0]
            x = pos[1]
            # print('testing')
            # print(z, x)
            # print(mapArr[z][x])
            if mapArr[x][z] != 0:
                trees.remove(pos)
        # print(trees)
        # print('Mapppp Arrr')
        
        # for i in trees:
        #     print('test1')
        #     print(i)
        #     z = i[0]
        #     x = i[1]
        #     print('testing')
        #     print(z, x)
        #     print(mapArr[z][x])
        #     # checks if the area is for trees (non-buildable areas)
        #     if mapArr[z][x] != 0:
        #         trees.remove(i)
        # print(trees)
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

        if y > 0:
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

# acts as controller 
def treePlacement(level, box, mapArr, afterHM):
    try:
        trees = findPosition(level, box)
        # # updates trees array
        # print('map array beforeeeee')
        # print(mapArr)
        mapArr = reassignGate(mapArr)
        # print('mapArr')
        # print(mapArr)
        # print(trees)
        trees = compareTreePosition(trees, mapArr)
        # print('trees')
        # print(trees)
        generateTrees(afterHM, trees, level, box)
    except Exception as e:
        logger.error(e)

# arr = [
#     [0, 0, 0, 0],
#     [0, 0, 0, 0],
#     [1, 1, 1, 1],
#     [1, 1, 1, 1],
# ]

# trees = [[0,2], [3,3]]

# print(compareTreePosition(trees, arr))