from logger import Logger
import numpy as np
import random
from copy import deepcopy
import os
import datetime
import time
# import heightmap

logger = Logger("Brush")

def run(gridArray, heightMap, startingPoint, level, box):
    buildingDict = {
        "towncentre": [12,7],
        "simplehouse": [3,3],
        "complexhouse": [4,5]
    }

    plotNumDict = {
        "towncentre": 1,
        "simplehouse": 9999,
        "complexhouse": 20
    }

    plotWeightingDict = {
        "towncentre": 1000,
        "simplehouse": 50,
        "complexhouse": 50
    }

    posFFDict = dict()
    posFFRDict = dict()

    attemptBuildDict = dict()
    attemptOccDict = dict()
    attemptScoringDict = dict()

    gridPos = getBuildableplot(gridArray)

    for key in buildingDict:
        posFFDict[key] = fitting(buildingDict[key], gridPos, gridArray)
        posFFRDict[key] = fitting([buildingDict[key][1], buildingDict[key][0]], gridPos, gridArray)

    # with open(os.path.join(os.path.expanduser("~/Desktop"),'posFF-'+ datetime.datetime.now().strftime('%H%M%S') +'.txt'), 'w+') as f:
    #     f.write(str(posFFDict))

    # with open(os.path.join(os.path.expanduser("~/Desktop"),'posFFR-'+ datetime.datetime.now().strftime('%H%M%S') +'.txt'), 'w+') as f:
    #     f.write(str(posFFRDict))

    plotRemaining = 0
    for key in posFFDict:
        plotRemaining += (len(posFFDict[key]) + len(posFFRDict[key])) / 2
    sumPlotAvilable = plotRemaining
    prevPlotRemaining = plotRemaining
    for index in range(10):
        logger.info(plotRemaining)
        build = True
        localPlotWeightingDict = plotWeightingDict.copy()
        localPlotNumDict = plotNumDict.copy()
        localPosDict = posFFDict.copy()
        localPosRDict = posFFRDict.copy()
        occPlot = []
        scoring = 0
        builtDict = dict()
        while build:
            plotName = getRandomPlot(localPlotWeightingDict)
            plot = buildingDict[plotName]
            rotat = True if random.randint(1, 3) % 2 == 0 else False
            pDict = localPosRDict if rotat else localPosDict
            idle = 0
            if len(pDict[plotName]) >= 1:
                location = pDict[plotName][random.randint(0, len(pDict[plotName]) - 1)]
                tempPlot = []
                valid = True
                x = plot[1] if rotat else plot[0]
                z = plot[0] if rotat else plot[1]

                tempPlot = list([[m, k] for k in range(location[0], location[0] + x) for m in range(location[1], location[1] + z)])

                if [i for e in tempPlot for i in occPlot if e == i]:
                    valid = False
                # logger.info(u'{}, {} - {}'.format(location, plotName, valid))
                if valid:
                    idle = 0
                    builtDict[location[1], location[0]] = (plotName+"R") if rotat else plotName
                    scoring += (buildingDict[plotName][0] * buildingDict[plotName][1]) ^ 2
                    occPlot += tempPlot
                    for key in localPosDict:
                        localPosDict[key] = [x for x in localPosDict[key] if x not in occPlot]
                        localPosRDict[key] = [x for x in localPosRDict[key] if x not in occPlot]
                    localPlotNumDict[plotName] -= 1
                    if localPlotNumDict[plotName] <= 0:
                        localPlotWeightingDict[plotName] = 0
                else:
                    idle += (sumPlotAvilable / 15)
                    for key in localPosDict:
                        if buildingDict[key][0] >= buildingDict[plotName][0] and buildingDict[key][1] >= buildingDict[plotName][1]:
                            localPosDict[key] = [x for x in localPosDict[key] if x is not location]
                            localPosRDict[key] = [x for x in localPosRDict[key] if x is not location]
            else:
                localPlotWeightingDict[plotName] = 0
                localPlotNumDict[plotName] = 0
                idle += (sumPlotAvilable / 10)
            
            plotRemaining = 0
            for key in localPosDict:
                plotRemaining += len(localPosDict[key]) + len(localPosRDict[key])
            if prevPlotRemaining == plotRemaining:
                idle += (sumPlotAvilable / 4)
            prevPlotRemaining = plotRemaining
            if (idle >= (sumPlotAvilable)):
                build = False
                logger.info(u'{} - idleOut'.format(index))
            if plotRemaining <= 0:
                build = False
                logger.info(u'{} - outOut'.format(index))
        attemptBuildDict[index] = builtDict
        attemptOccDict[index] = occPlot
        attemptScoringDict[index] = round((scoring * (float(len(occPlot)) / float(sumPlotAvilable)))) if len(occPlot) > 1 else 0      
    
    best = max(attemptScoringDict, key=attemptScoringDict.get)
    # logger.info(best)
    # logger.info(u'{}, {}'.format(len(heightMap), len(heightMap[0])))
    for cell in attemptOccDict[best]:
        level.setBlockAt(box.minx + (cell[0]*4) + startingPoint[0], heightMap[cell[0]*4 + startingPoint[0]][cell[1]*4 + startingPoint[1]], box.minz + (cell[1]*4) + startingPoint[1], 57)

    for cell in attemptBuildDict[best]:
        level.setBlockAt(box.minx + (cell[0]*4 + startingPoint[0]), heightMap[cell[0]*4 + startingPoint[0]][cell[1]*4 + startingPoint[1]] + 1, box.minz + (cell[1]*4) + startingPoint[1], 133)

    # with open(os.path.join(os.path.expanduser("~/Desktop"),'ABD-'+ datetime.datetime.now().strftime('%H%M%S') +'.txt'), 'w+') as f:
    #     f.write(str(attemptBuildDict))

    
def fitting(size, posArray, gridArray):
    avaPlot = []
    for pos in posArray:
        if pos[0] + size[0] < len(gridArray) and pos[1] + size[1] < len(gridArray[0]):
            plotArea = list([gridArray[i][k] for i in range(pos[0], pos[0] + size[0]) for k in range(pos[1], pos[1] + size[1])])
            if len(set(plotArea)) == 1 and sum(plotArea) == (size[0] * size[1]):
                avaPlot.append(pos)
    return avaPlot

def getBuildableplot(gridArray):
    posArray = []
    pos = np.where(gridArray == 1)
    for x, z in zip(pos[0], pos[1]):
        posArray.append([x,z])
    return (posArray)

def getRandomPlot(plotWeightingDict):
    randomWeighting = random.randint(0, sum(plotWeightingDict.values()))
    for key in plotWeightingDict:
        randomWeighting -= plotWeightingDict[key]
        if randomWeighting <= 0:
            return key


def CTPFF(heightMap, exclusion, size, level, box):
    
    buildingDict = {
        "towncentre": [44,20],
        "simplehouse": [12,12],
        "complexhouse": [16,20]
    }

    plotNumDict = {
        "towncentre": 1,
        "simplehouse": 9999,
        "complexhouse": 20
    }

    plotWeightingDict = {
        "towncentre": 10000,
        "simplehouse": 50,
        "complexhouse": 50
    }

    # posDict = dict()
    # posRDict = dict()
    posFFDict = dict()
    posFFRDict = dict()
    attemptBuildDict = dict()
    attemptOccDict = dict()
    attemptScoringDict = dict()

    # def getPlot(heightmap, size):
    #     avaPlot = []
    #     for x in range(0 + exclusion, len(heightmap) - (exclusion) - size[0]):
    #         for y in range(0 + exclusion, len(heightmap[0]) - (exclusion) - size[1]):
    #             level = heightmap[x][y]
    #             plotArea = list([heightmap[i][k] for i in range(x, x + size[0]) for k in range(y, y + size[1])])
    #             if len(set(plotArea)) == 1 and list(set(plotArea))[0] == level and plotArea.count(level) == (size[0] * size[1]) and sum(plotArea) / len(plotArea) == level:
    #                 avaPlot.append([x,y])
    #     return avaPlot

    def getFFPlot(heightmap, size):
        avaPlot = []
        for x in range(0 + exclusion, len(heightmap) - (exclusion) - size[0]):
            for y in range(0 + exclusion, len(heightmap[0]) - (exclusion) - size[1]):
                level = heightmap[x][y]
                plotArea = list([heightmap[i][k] for i in range(x, x + size[0]) for k in range(y, y + size[1])])
                if len(set(plotArea)) == 1 and list(set(plotArea))[0] == level and plotArea.count(level) == (size[0] * size[1]) and sum(plotArea) / len(plotArea) == level:
                    avaPlot.append([x,y])
                else:
                    y += size[1]
        return avaPlot

    # def surface(x, z, cell, plotMap):
    #     plotArea = [plotMap[i][k] for i in range(cell[0], cell[0] + x) for k in range(cell[1], cell[1] + z)]
    #     if sum(plotArea) == (x * z):
    #         return True
    #     else:
    #         return False

    def getRandomPlot(plotWeightingDict):
        randomWeighting = random.randint(0, sum(plotWeightingDict.values()))
        for key in plotWeightingDict:
            randomWeighting -= plotWeightingDict[key]
            if randomWeighting <= 0:
                return key

    # areaDict, heightDict, borderDict, sizeDict, plotDict = getBuildableArea(heightMap, exclusion, size, level, box)

    # for bKey in buildingDict:
    #     plotlist = []
    #     plotRlist = []
    #     buildSize = buildingDict[bKey]
    #     for key in areaDict:
    #         area = areaDict[key]
    #         plot = plotDict[key]
    #         minx = sizeDict[key][0]
    #         miny = sizeDict[key][1]
    #         for cell in area:
    #             localCell = [cell[0] - minx, cell[1] - miny]
    #             if(localCell[0] + buildSize[0] <= len(plot) and localCell[1] + buildSize[1] <= len(plot[0])):
    #                 if surface(buildSize[0], buildSize[1], localCell, plot):
    #                     plotlist.append(cell)
    #             if(localCell[0] + buildSize[1] <= len(plot) and localCell[1] + buildSize[0] <= len(plot[0])):
    #                 if surface(buildSize[1], buildSize[0], localCell, plot):
    #                     plotRlist.append(cell)

    #     posDict[bKey] = plotlist
    #     posRDict[bKey] = plotRlist


    x_gate_width = (len(heightMap) - 16) % 8
    while x_gate_width < 6:
        x_gate_width += 4
    
    z_gate_width = (len(heightMap[0]) - 16) % 8
    while z_gate_width < 6:
        z_gate_width += 4
    
    x_left = 0
    z_left = 0
    x_length = len(heightMap) - 16
    z_length = len(heightMap[0]) - 16

    if (x_length - x_gate_width) / 4 % 2 == 0:
        x_left = (x_length - x_gate_width) / 8
    else:
        x_left = (((x_length - x_gate_width) - 4) / 8)

    if (z_length - z_gate_width) / 4 % 2 == 0:
        z_left = (z_length - z_gate_width) / 8
    else:
        z_left = (((z_length - z_gate_width) - 4) / 8)

    x_gate_Pos = 6 + (x_left *4)
    z_gate_Pos = 6 + (z_left *4)

    for i in range(7, 14):
        for c in range(x_gate_width + 4):
            heightMap[x_gate_Pos + c][i] = 0
            heightMap[x_gate_Pos + c][len(heightMap[0]) - i - 1] = 0

        for c in range(z_gate_width + 4):
            heightMap[i][z_gate_Pos + c] = 0
            heightMap[len(heightMap) - i - 1][z_gate_Pos + c] = 0

    for x in range(0, exclusion):
        for y in range(0, len(heightMap[0])):
            heightMap[x][y] = 0
            heightMap[len(heightMap) - x - 1][y] = 0
        for y in range(0, len(heightMap)):
            heightMap[y][x] = 0
            heightMap[y][len(heightMap[0]) - x - 1] = 0

    with open(os.path.join(os.path.expanduser("~/Desktop"),'HM-'+ datetime.datetime.now().strftime('%H%M%S') +'.txt'), 'w+') as f:
        np.savetxt(f, np.column_stack(heightMap), fmt='%s')
        f.close()

    # incstart = time.time()
    # for key in buildingDict:
    #     posDict[key] = getPlot(heightMap, buildingDict[key])
    #     posRDict[key] = getPlot(heightMap, [buildingDict[key][1], buildingDict[key][0]])
    # incend = time.time()
    # logger.debug(u'{} sec used'.format(round(incend - incstart, 2)))

    incstart = time.time()
    for key in buildingDict:
        posFFDict[key] = getFFPlot(heightMap, buildingDict[key])
        posFFRDict[key] = getFFPlot(heightMap, [buildingDict[key][1], buildingDict[key][0]])
    incend = time.time()
    logger.debug(u'{} sec used'.format(round(incend - incstart, 2)))

    for index in range(10):
        build = True
        scoring = 0
        idle = 0
        plotRemaining = 0
        for key in posFFDict:
            plotRemaining += (len(posFFDict[key]) + len(posFFRDict[key])) / 2
        sumPlotAvilable = plotRemaining
        localPlotWeightingDict = plotWeightingDict.copy()
        localPlotNumDict = plotNumDict.copy()
        localPosDict = posFFDict.copy()
        localPosRDict = posFFRDict.copy()
        occPlot = []
        builtDict = dict()
        while build:
            plotName = getRandomPlot(localPlotWeightingDict)
            plot = buildingDict[plotName]
            rotat = True if random.randint(1, 3) % 2 == 0 else False
            pDict = localPosRDict if rotat else localPosDict

            if len(pDict[plotName]) >= 1: 
                location = pDict[plotName][random.randint(0, len(pDict[plotName]) - 1)]
                tempPlot = []
                valid = True
                x = plot[1] if rotat else plot[0]
                z = plot[0] if rotat else plot[1]

                tempPlot = list([[k, m] for k in range(location[0], location[0] + x) for m in range(location[1], location[1] + z)])

                if [i for e in tempPlot for i in occPlot if e == i]:
                    valid = False

                if valid:
                    idle = 0
                    builtDict[location[0], location[1]] = (plotName+"R") if rotat else plotName
                    scoring += (buildingDict[plotName][0] * buildingDict[plotName][1]) ^ 2
                    occPlot += tempPlot
                    for key in localPosDict:
                        localPosDict[key] = [x for x in localPosDict[key] if x not in occPlot]
                        localPosRDict[key] = [x for x in localPosRDict[key] if x not in occPlot]
                    localPlotNumDict[plotName] -= 1
                    if localPlotNumDict[plotName] <= 0:
                        localPlotWeightingDict[plotName] = 0
                else:
                    idle += (sumPlotAvilable / 15)
                    for key in localPosDict:
                        if buildingDict[key][0] >= buildingDict[plotName][0] and buildingDict[key][1] >= buildingDict[plotName][1]:
                            localPosDict[key] = [x for x in localPosDict[key] if x is not location]
                            localPosRDict[key] = [x for x in localPosRDict[key] if x is not location]
            else:
                localPlotWeightingDict[plotName] = 0
                localPlotNumDict[plotName] = 0
                idle += (sumPlotAvilable / 10)
            prevPlotRemaining = plotRemaining
            plotRemaining = 0
            for key in localPosDict:
                plotRemaining += len(localPosDict[key]) + len(localPosRDict[key])
            if prevPlotRemaining == plotRemaining:
                idle += (sumPlotAvilable / 3)
            if (idle >= (sumPlotAvilable / 2)):
                build = False
                logger.info(u'{} - idleOut'.format(index))
            if plotRemaining <= 0:
                build = False
                logger.info(u'{} - outOut'.format(index))

        attemptBuildDict[index] = builtDict
        attemptOccDict[index] = occPlot
        attemptScoringDict[index] = round((scoring * (float(len(occPlot)) / float(sumPlotAvilable)))) if len(occPlot) > 1 else 0
    with open(os.path.join(os.path.expanduser("~/Desktop"),'ABD-'+ datetime.datetime.now().strftime('%H%M%S') +'.txt'), 'w+') as f:
        f.write(str(attemptBuildDict))
    
    with open(os.path.join(os.path.expanduser("~/Desktop"),'AOD-'+ datetime.datetime.now().strftime('%H%M%S') +'.txt'), 'w+') as f:
        f.write(str(attemptOccDict))

    with open(os.path.join(os.path.expanduser("~/Desktop"),'ASD-'+ datetime.datetime.now().strftime('%H%M%S') +'.txt'), 'w+') as f:
        f.write(str(attemptScoringDict))

    best = max(attemptScoringDict, key=attemptScoringDict.get)
    for cell in attemptOccDict[best]:
        level.setBlockAt(box.minx + cell[0], heightMap[cell[0]][cell[1]], box.minz + cell[1], 57)

    for key in attemptBuildDict[best]:
        level.setBlockAt(box.minx + key[0], heightMap[key[0]][key[1]] + 1, box.minz + key[1], 133)

    logger.info(u'<<<<<<<<{}'.format(best))

# def getBuildableArea(heightMap, exclusion, size, level, box):
#     tempHM = deepcopy(heightMap)

#     x_gate_width = (len(tempHM) - 16) % 8
#     while x_gate_width < 6:
#         x_gate_width += 4
    
#     z_gate_width = (len(tempHM[0]) - 16) % 8
#     while z_gate_width < 6:
#         z_gate_width += 4
    
#     x_left = 0
#     z_left = 0
#     x_length = len(tempHM) - 16
#     z_length = len(tempHM[0]) - 16

#     if (x_length - x_gate_width) / 4 % 2 == 0:
#         x_left = (x_length - x_gate_width) / 8
#     else:
#         x_left = (((x_length - x_gate_width) - 4) / 8)

#     if (z_length - z_gate_width) / 4 % 2 == 0:
#         z_left = (z_length - z_gate_width) / 8
#     else:
#         z_left = (((z_length - z_gate_width) - 4) / 8)
    
#     # logger.info(u'{}-{}'.format(x_length, z_length))
#     # logger.info(u'{}-{}'.format(x_gate_width, z_gate_width))
#     # logger.info(u'{}-{}'.format(x_left, z_left))

#     x_gate_Pos = 6 + (x_left *4)
#     z_gate_Pos = 6 + (z_left *4)

#     excludedArea = []
#     for i in range(7, 14):
#         for c in range(x_gate_width + 4):
#             excludedArea.append([x_gate_Pos + c, i])
#             excludedArea.append([x_gate_Pos + c, len(tempHM[0]) - i - 1])
#             tempHM[x_gate_Pos + c][i] = 0
#             tempHM[x_gate_Pos + c][len(tempHM[0]) - i - 1] = 0

#         for c in range(z_gate_width + 4):
#             excludedArea.append([i, z_gate_Pos + c])
#             excludedArea.append([len(tempHM) - i - 1, z_gate_Pos + c])
#             tempHM[i][z_gate_Pos + c] = 0
#             tempHM[len(tempHM) - i - 1][z_gate_Pos + c] = 0

#     for x in range(0, exclusion):
#         for y in range(0, len(tempHM[0])):
#             tempHM[x][y] = 0
#             tempHM[len(tempHM) - x - 1][y] = 0
#             excludedArea.append ([x, y])
#             excludedArea.append ([len(tempHM) - x - 1, y])
#         for y in range(0, len(heightMap)):
#             tempHM[y][x] = 0
#             tempHM[y][len(tempHM) - x - 1] = 0
#             excludedArea.append ([y, x])
#             excludedArea.append ([y, len(tempHM) - x - 1])


#     # numhm = np.asarray(heightMap)
#     # hmLevel = np.unique(numhm)
#     # logger.info(hmLevel)
#     areaDict = dict()
#     heightDict = dict()
#     borderDict = dict()
#     sizeDict = dict()
#     plotDict = dict()

#     # x_gate_pos_low = x_gate_Pos
#     # x_gate_pos_high = x_gate_Pos + x_gate_width + 4
#     # z_gate_pos_low = z_gate_Pos
#     # z_gate_pos_high = z_gate_Pos + z_gate_width + 4

#     def FF(x, y, area, border, minx, miny, maxx, maxy):
#         tempHM[x][y] = 999
#         # if not((x >= x_gate_pos_low and x <= x_gate_pos_high) and (y >= z_gate_pos_low and y <= z_gate_pos_high)):
#         #     if not((x >= len(tempHM) - 14 and x <= len(tempHM))):
#         #         if (x >= x_gate_pos_low and x <= x_gate_pos_high) or (x >= 0 and x <= 14):
#         #             if (y >= 0 and y <= 14) or (y >= z_gate_pos_low and y <= z_gate_pos_high):
#         #                     return area, border, minx, miny, maxx, maxy
#         #         if (x >= x_gate_pos_low and x <= x_gate_pos_high) or (x >= len(tempHM) - 14 and x <= len(tempHM)):
#         #             if (y >= len(tempHM) - 14 and y <= len(tempHM)) or (y >= z_gate_pos_low and y <= z_gate_pos_high):
#         #                     return area, border, minx, miny, maxx, maxy
#         if [x, y] in excludedArea:
#             return area, border, minx, miny, maxx, maxy
#         area.append([x,y])
#         if x < minx:
#             minx = x
#         if y < miny:
#             miny = y
#         if x > maxx:
#             maxx = x
#         if y > maxy:
#             maxy = y
#         if len(area) <= 10000:
#             borderFlag = 0
#             if ((y - 1) >= (0 + exclusion)):  # go to west
#                 if heightMap[x][y - 1] == currentLevel:
#                     borderFlag += 1
#                 if tempHM[x][y - 1] == currentLevel:
#                     area, border, minx, miny, maxx, maxy = FF(x, y - 1, area, border, minx, miny, maxx, maxy)

#             if ((y + 1) < (len(tempHM[x]) - exclusion)): # go to east
#                 if heightMap[x][y + 1] == currentLevel:
#                     borderFlag += 1
#                 if tempHM[x][y + 1] == currentLevel:
#                     area, border, minx, miny, maxx, maxy = FF(x, y + 1, area, border, minx, miny, maxx, maxy)

#             if ((x + 1) < (len(tempHM) - exclusion)): # go to south
#                 if heightMap[x + 1][y] == currentLevel:
#                     borderFlag += 1
#                 if tempHM[x + 1][y] == currentLevel:
#                     area, border, minx, miny, maxx, maxy = FF(x + 1, y, area, border, minx, miny, maxx, maxy)

#             if ((x - 1) >= (0 + exclusion)): # go to north
#                 if heightMap[x - 1][y] == currentLevel:
#                     borderFlag += 1
#                 if tempHM[x - 1][y] == currentLevel:
#                     area, border, minx, miny, maxx, maxy = FF(x - 1, y, area, border, minx, miny, maxx, maxy)

#             if ((y + 1) < (len(tempHM[x]) - exclusion)):#east
#                 if ((x + 1) < (len(tempHM) - exclusion)):#southeast
#                     if heightMap[x + 1][y + 1] == currentLevel:
#                         borderFlag += 1
#                 if ((x - 1) >= (0 + exclusion)):#northeast
#                     if heightMap[x - 1][y + 1] == currentLevel:
#                         borderFlag += 1

#             if ((y - 1) >= (0 + exclusion)):#west
#                 if ((x + 1) < (len(tempHM) - exclusion)):#southwest
#                     if heightMap[x + 1][y - 1] == currentLevel:
#                         borderFlag += 1
#                 if ((x - 1) >= (0 + exclusion)):#northwest
#                     if heightMap[x - 1][y - 1] == currentLevel:
#                         borderFlag += 1
            
#             if borderFlag < 8 and (x > exclusion and x < (len(tempHM) - exclusion - 1)) and (y > exclusion and y < (len(tempHM[0]) - exclusion - 1)):
#                 border.append([x,y])
#         return area, border, minx, miny, maxx, maxy

#     areaInd = 100
#     for x in range(0 + exclusion, len(tempHM) - (2 * exclusion)):
#         for y in range(0 + exclusion, len(tempHM[0]) - (2 * exclusion)):
#             if tempHM[x][y] != 999 or tempHM[x][y] < 0:
#                 currentLevel = tempHM[x][y]
#                 area, border, minx, miny, maxx, maxy = FF(x, y, [], [], x, y, x, y)
#                 if len(area) >= size:
#                     areaDict[areaInd] = area
#                     heightDict[areaInd] = currentLevel
#                     borderDict[areaInd] = border
#                     sizeDict[areaInd] = [minx, miny, maxx, maxy]
#                     # logger.info(u'{} - {} - {}'.format("ara", areaInd, (len(area))))
#                     # logger.info(u'{} - {} - {}'.format("bor", areaInd, (len(border))))
#                     # logger.info(u'{} - {} - {}, {}, {}, {}'.format("siz", areaInd, minx, miny, maxx, maxy))
#                     # if areaInd == 103:
#                     #     for cell in border:
#                     #         level.setBlockAt(box.minx + cell[0], currentLevel - 1, box.minz + cell[1], 57)
#                     # else:
#                     for cell in border:
#                         level.setBlockAt(box.minx + cell[0], currentLevel - 1, box.minz + cell[1], 41)
#                     # for cell in area:
#                     #     level.setBlockAt(box.minx + cell[0], currentLevel - 1, box.minz + cell[1], 57)
                    
#                     areaPlot = [[0 for j in range(maxy - miny + 1)] for k in range(maxx - minx + 1)]
#                     for cell in area:
#                         areaPlot[cell[0] - minx][cell[1] - miny] = 1
                    
#                     plotDict[areaInd] = areaPlot

#                     # if areaInd == 104:
#                     #     with open(os.path.join(os.path.expanduser("~/Desktop"),'plot-'+ datetime.datetime.now().strftime('%H%M%S') +'.txt'), 'w+') as f:
#                     #         np.savetxt(f, areaPlot, fmt='%s')
#                     #         f.close()
#                     #     for row in range(len(areaPlot)):
#                     #         for cell in range(len(areaPlot[0])):
#                     #             if areaPlot[row][cell] == 1:
#                     #                 level.setBlockAt(box.minx + minx + cell, currentLevel + 3, box.minz + miny + row, 133)
#                     areaInd += 1

#                 # else:
#                     # logger.info(u'{} - {} - {}'.format("araexc", 999, (len(area))))
#                     # logger.info(u'{} - {} - {}'.format("borexc", 999, (len(border))))
#                     # logger.info(u'{} - {} - {}, {}, {}, {}'.format("sizexc", 999, minx, miny, maxx, maxy))
#                     # for cell in area:
#                     #     level.setBlockAt(box.minx + cell[0], currentLevel - 1, box.minz + cell[1], 57)
#     return areaDict, heightDict, borderDict, sizeDict, plotDict