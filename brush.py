from logger import Logger
import numpy as np
import random
from copy import deepcopy
import os
import datetime
import time

from pymclevel import MCSchematic
from pymclevel.box import Vector
# import heightmap

logger = Logger("Brush")

def run(gridArray, heightMap, startingPoint, level, box):
    try:
        buildingDict = {# L W H
            "town_hall": [7,12],
            "simple_house": [3,3],
            "blacksmith": [2,3],
            "medium_house": [3,3],
            "small_library": [2,2],
            "library": [5,6],
            "tiny_house": [2,2],
            "notice_board":[2,1],
            "modern_house": [3,3],
            "stall": [2,1],
            "plot_tree": [2,2],
            "tower": [3,3],
            "portal": [3,2],
            "well": [2,2],
            "plant": [2,1],
            "bench": [2,1],
            "garden": [2,2],
            "greenhouse": [3,3],
            "bakery": [3,2]
        }

        plotNumDict = {
            "town_hall": 1,
            "simple_house": 300,
            "blacksmith": 3,
            "medium_house": 300,
            "small_library": 5,
            "library": 5,
            "tiny_house": 300,
            "notice_board": 2,
            "modern_house": 300,
            "stall": 20,
            "plot_tree": 55,
            "tower": 3,
            "portal": 2,
            "well": 10,
            "plant": 999,
            "bench": 10,
            "garden": 35,
            "greenhouse": 10,
            "bakery": 10
        }

        plotWeightingDict = {
            "town_hall": 100000,
            "simple_house": 5000,
            "blacksmith": 3000,
            "medium_house": 5000,
            "small_library": 50,
            "library": 8000,
            "tiny_house": 2000,
            "notice_board": 10,
            "modern_house": 5000,
            "stall": 50,
            "plot_tree": 50,
            "tower": 80000,
            "portal": 5000,
            "well": 300,
            "plant": 5,
            "bench": 5,
            "garden": 5,
            "greenhouse": 3000,
            "bakery": 5000
        }

        posFFDict = dict()
        posFFRDict = dict()

        attemptBuildDict = dict()
        attemptOccDict = dict()
        attemptScoringDict = dict()

        gridPos = getBuildableplot(gridArray)

        for key in buildingDict:
            logger.info("Figuring out: {}".format(key))
            posFFDict[key] = fitting(buildingDict[key], gridPos, gridArray)
            if buildingDict[key][0] == buildingDict[key][1]:
                posFFRDict[key] = posFFDict[key]
            else:
                posFFRDict[key] = fitting([buildingDict[key][1], buildingDict[key][0]], gridPos, gridArray)


        plotRemaining = 0
        for key in posFFDict:
            plotRemaining += int((len(posFFDict[key]) + len(posFFRDict[key])))
        sumPlotAvilable = plotRemaining
        prevPlotRemaining = plotRemaining
        for index in range(10):
            plotRemaining = sumPlotAvilable
            logger.info(u'{} - calc - {}'.format(index, plotRemaining))
            build = True
            localPlotWeightingDict = plotWeightingDict.copy()
            localPlotNumDict = plotNumDict.copy()
            localPosDict = posFFDict.copy()
            localPosRDict = posFFRDict.copy()
            occPlot = []
            scoring = 0
            idle = 0
            builtDict = dict()
            while build:
                plotName = getRandomPlot(localPlotWeightingDict)
                plot = buildingDict[plotName]
                rotat = True if random.randint(1, 3) % 2 == 0 else False
                pDict = localPosRDict if rotat else localPosDict
                if len(pDict[plotName]) < 1:
                    rotat = not(rotat)
                    pDict = localPosRDict if rotat else localPosDict
                if len(pDict[plotName]) >= 1:
                    location = pDict[plotName][random.randint(0, len(pDict[plotName]) - 1)]
                    tempPlot = []
                    valid = True
                    x = plot[1] if rotat else plot[0]
                    z = plot[0] if rotat else plot[1]

                    tempPlot = list([[m, k] for k in range(location[0], location[0] + x) for m in range(location[1], location[1] + z)])

                    if [i for e in tempPlot for i in occPlot if e == i]:
                        valid = False
                    
                    if valid:
                        idle = 0
                        builtDict[location[1], location[0]] = (plotName+"R") if rotat else plotName
                        scoring += (buildingDict[plotName][0] * buildingDict[plotName][1]) ^ 2
                        occPlot += tempPlot
                        for key in localPosDict:
                            localPosDict[key] = [x for x in localPosDict[key] if x not in tempPlot]
                            localPosRDict[key] = [x for x in localPosRDict[key] if x not in tempPlot]
                        localPlotNumDict[plotName] -= 1
                        if localPlotNumDict[plotName] <= 0:
                            localPlotWeightingDict[plotName] = 0
                            localPosDict[plotName] = []
                            localPosRDict[plotName] = []
                    else:
                        for key in localPosDict:
                            if buildingDict[key][0] >= buildingDict[plotName][0] and buildingDict[key][1] >= buildingDict[plotName][1]:
                                localPosDict[key] = [x for x in localPosDict[key] if x is not location]
                                localPosRDict[key] = [x for x in localPosRDict[key] if x is not location]

                if len(localPosDict[plotName]) <=0 and len(localPosRDict[plotName]) <= 0:
                    localPlotWeightingDict[plotName] = 0
                    localPlotNumDict[plotName] = 0
                
                plotRemaining = 0
                for key in localPosDict:
                    plotRemaining += len(localPosDict[key]) + len(localPosRDict[key])
                # logger.info(u'{} - {} - {} - {}'.format(plotName, idle, prevPlotRemaining, plotRemaining))
                if prevPlotRemaining == plotRemaining:
                    idle += (sumPlotAvilable / 10)
                prevPlotRemaining = plotRemaining
                if (idle >= (sumPlotAvilable * 5)):
                    build = False
                    logger.info(u'{} - idleOut - {}'.format(index, plotRemaining))
                if plotRemaining <= 0:
                    build = False
                    logger.info(u'{} - outOut - {}'.format(index, plotRemaining))
            attemptBuildDict[index] = builtDict
            attemptOccDict[index] = occPlot
            attemptScoringDict[index] = round((scoring * (float(len(occPlot)) / float(sumPlotAvilable)))) if len(occPlot) > 1 else 0      
        
        best = max(attemptScoringDict, key=attemptScoringDict.get)

        totalPlot = [[x[1], x[0]] for x in gridPos]
        unOccPlot = [x for x in totalPlot if x not in attemptOccDict[best]]


        for cell in unOccPlot:
            target = "empty"
            placingBuild(level, target, (box.minx + (cell[0]*4) + startingPoint[0]), (heightMap[cell[0]*4 + startingPoint[0]][cell[1]*4 + startingPoint[1]] - 1), (box.minz + (cell[1]*4) + startingPoint[1]))

        for cell in attemptBuildDict[best]:
            placingBuild(level, attemptBuildDict[best][cell], (box.minx + (cell[0]*4) + startingPoint[0]), (heightMap[cell[0]*4 + startingPoint[0]][cell[1]*4 + startingPoint[1]] - 1), (box.minz + (cell[1]*4) + startingPoint[1]), attemptBuildDict[best][cell])

    except Exception as e:
        logger.error(e)

    
def fitting(size, posArray, gridArray):
    try:
        avaPlot = []
        for pos in posArray:
            if pos[0] + size[0] < len(gridArray) and pos[1] + size[1] < len(gridArray[0]):
                plotArea = list([gridArray[i][k] for i in range(pos[0], pos[0] + size[0]) for k in range(pos[1], pos[1] + size[1])])
                if len(set(plotArea)) == 1 and sum(plotArea) == (size[0] * size[1]):
                    avaPlot.append(pos)
        return avaPlot
    except Exception as e:
        logger.error(e)

def getBuildableplot(gridArray):
    try:
        posArray = []
        pos = np.where(gridArray == 1)
        for x, z in zip(pos[0], pos[1]):
            posArray.append([x,z])
        return (posArray)
    except Exception as e:
        logger.error(e)

def getRandomPlot(plotWeightingDict):
    try:
        randomWeighting = random.randint(0, sum(plotWeightingDict.values()))
        for key in plotWeightingDict:
            randomWeighting -= plotWeightingDict[key]
            if randomWeighting <= 0:
                return key
    except Exception as e:
        logger.error(e)

def placingBuild(level, building, x, y, z, folder = "1x1"):
    try:
        variation = {
            "simple_house" : 5,
            "stall": 4,
            "plot_tree": 12,
            "plant": 3,
            "bench": 3,
            "blacksmith": 2,
            "greenhouse": 2,
            "bakery": 2,
            "modern_house": 5,
            "tiny_house": 3
        }

        size = { # L W H
            "town_hall": [7,33,12],
            "simple_house": [3,6,3],
            "blacksmith": [2,15,3],
            "medium_house": [3,9,3],
            "small_library":[2,10,2],
            "library": [5,10,6],
            "tiny_house": [2,6,2],
            "notice_board":[2,5,1],
            "modern_house": [3,10,3],
            "empty": [1,1,1],
            "stall": [2,5,1],
            "empty": [1,5,1],
            "hay": [1,5,1],
            "plaza": [1,5,1],
            "bin": [1,5,1],
            "bench_1": [1,5,1],
            "lamp": [1,5,1],
            "enchantment": [1,5,1],
            "plot_tree":[2,20,2],
            "tower":[3,51,3],
            "portal":[3,11,2],
            "well": [3,12,3],
            "plant": [2,6,1],
            "bench": [2,6,1],
            "garden": [2,6,2],
            "greenhouse":[3,10,3],
            "bakery":[3,11,2]
        }

        tab = {
            "stall": -1,
            "well": -2
        }
        rotat = False
        
        if building.endswith('R') or folder.endswith("R"):
            building = building[:-1]
            folder = folder[:-1]
            rotat = True
            
        size = [size[building][i] * 4 if i != 1 else size[building][1] for i in range(len(size[building]))]

        y = y + tab[building] if building in tab else y

        if building in variation:
            randomIndex = random.randint(1, variation[building])
            filename = os.path.join(os.path.dirname(__file__), 'schematics', folder, building + '_{}.schematic'.format(randomIndex))
        else:
            filename = os.path.join(os.path.dirname(__file__), 'schematics', folder, building + '.schematic')
        schematic = MCSchematic(shape=(size[0], size[1], size[2]), filename=filename)
        
        if rotat:
            schematic.rotateLeft()

        level.copyBlocksFrom(schematic, schematic.bounds, Vector(x, y, z))
    except Exception as e:
        logger.error(e)