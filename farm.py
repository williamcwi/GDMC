import operator
from logger import Logger
import random
from copy import deepcopy

logger = Logger("farm")

def init(level, box, heightMap, buildMap, treeMap):
    tempHM = deepcopy(buildMap)

    # Flood fill method to find area for farm
    def FFFF (x, y, area, limit):
        area.append([x,y])
        stonks = []
        stonks.append([x,y])
        length = len(stonks)
        tempHM[x][y] = 999

        while length > 0 and len(area) < limit:
            x = stonks[0][0]
            y = stonks[0][1]
            stonks.pop(0)
            if ((y - 3) > (8)) and ((x + 1) < (len(tempHM) - 8)) and ((x - 1) > (8)): # go to east
                if tempHM[x][y - 1] == 0 and ((tempHM[x][y - 3] == 0 and tempHM[x + 1][y - 3] == 0 and tempHM[x - 1][y - 3] == 999) or (tempHM[x][y - 3] == 999 and tempHM[x + 1][y - 3] == 999 and tempHM[x - 1][y - 3] == 999)) and heightMap[y - 1][x] != -1 and treeMap[x][y - 1] != 2:
                    stonks.append([x, y - 1])
                    area.append([x, y - 1])
                    tempHM[x][y - 1] = 999
            if ((y + 3) < (len(tempHM[x]) - 8)) and ((x + 1) < (len(tempHM) - 8)) and ((x - 1) > (8)): # go to west
                if tempHM[x][y + 1] == 0 and ((tempHM[x][y + 3] == 0 and tempHM[x + 1][y + 3] == 0 and tempHM[x - 1][y + 3] == 0) or (tempHM[x][y + 3] == 999 and tempHM[x + 1][y + 3] == 999 and tempHM[x - 1][y + 3] == 999)) and heightMap[y + 1][x] != -1 and treeMap[x][y + 1] != 2:
                    stonks.append([x, y + 1])
                    area.append([x, y + 1])
                    tempHM[x][y + 1] = 999
            if ((x + 3) < (len(tempHM) - 8)) and ((y + 1) < (len(tempHM[x]) - 8)) and ((y - 1) > (8)): # go to north
                if tempHM[x + 1][y] == 0 and ((tempHM[x + 3][y] == 0 and tempHM[x + 3][y + 1] == 0 and tempHM[x + 3][y - 1] == 0) or (tempHM[x + 3][y] == 999 and tempHM[x + 3][y + 1] == 999 and tempHM[x + 3][y - 1] == 999)) and heightMap[y][x + 1] != -1 and treeMap[x + 1][y] != 2:
                    stonks.append([x + 1, y])
                    area.append([x + 1, y])
                    tempHM[x + 1][y] = 999
            if ((x - 3) > (8)) and ((y + 1) < (len(tempHM[x]) - 8)) and ((y - 1) > (8)): # go to south
                if tempHM[x - 1][y] == 0 and ((tempHM[x - 3][y] == 0 and tempHM[x - 3][y + 1] == 0 and tempHM[x - 3][y - 1] == 0) or (tempHM[x - 3][y] == 999 and tempHM[x - 3][y + 1] == 999 and tempHM[x - 3][y - 1] == 999)) and heightMap[y][x - 1] != -1 and treeMap[x - 1][y] != 2:
                    stonks.append([x - 1, y])
                    area.append([x - 1, y])
                    tempHM[x - 1][y] = 999
            length = len(stonks)
        return area

    # --->Survey and Filter possible plot
    areaDict = dict()
    for x in range(10, len(heightMap[0]) - 10, 16):
        for y in range(10, len(heightMap) - 10, 16):
            tempPlot = [1 if int(buildMap[m][k]) > 0 else 0 for k in range(y, min(y + 16, len(buildMap[0]))) for m in range(x, min(x + 16, len(buildMap)))]
            if sum(tempPlot) < 40:
                areaDict[x, y] = len(tempPlot)

    sorted_x = sorted(areaDict.keys(), key=operator.itemgetter(0), reverse = True)

    # --->Get Number of plot to build
    randomNumPlot = min(max(random.randint(int(len(sorted_x) * 0.4), int(len(sorted_x) * 0.8)), 2), len(sorted_x) - 1) if len(sorted_x) > 1 else 1
    plotList = sorted_x[:randomNumPlot]
    if len(plotList) >= 1:
        logger.info("Building {} farm".format(len(plotList)))
        for plot in plotList: #Getting area for build
            valid = False
            i = 0
            while valid == False: # get random location in chunks size to start surveying
                ranLocat = [min(random.randint(plot[0], plot[0] + 16), len(heightMap[0]) - 13), min(random.randint(plot[1], plot[1] + 16), len(heightMap) - 13)]
                valid = True if tempHM[ranLocat[0]][ranLocat[1]] == 0 else False
                i += 1 
                if i > 256: break

            if valid:
                ranSize = min(max(random.randint(int(((box.width + box.length / 2)) * 0.7), int(((box.width + box.length / 2)) * 0.9)), 50), 200) #get random size of farm
                area = FFFF(ranLocat[0], ranLocat[1], [], ranSize) #survey for continous area form farm placement
                for cell in area: # --->Placing Wheat and farmland
                    level.setBlockAt(box.minx + cell[1] , heightMap[cell[1]][cell[0]] - 1, box.minz + cell[0], 60)
                    level.setBlockDataAt(box.minx + cell[1] , heightMap[cell[1]][cell[0]] - 1, box.minz + cell[0], random.randint(3, 7))
                    level.setBlockAt(box.minx + cell[1] , heightMap[cell[1]][cell[0]], box.minz + cell[0], 59)
                    level.setBlockDataAt(box.minx + cell[1] , heightMap[cell[1]][cell[0]], box.minz + cell[0], random.randint(0, 6))

                for cell in area: # --->Placing Water Block
                    surrounding = set([heightMap[cell[1] + 1][cell[0]], heightMap[cell[1] - 1][cell[0]], heightMap[cell[1]][cell[0] + 1], heightMap[cell[1]][cell[0] - 1]])
                    surrounding_x = list(set([tempHM[cell[0] + 1][cell[1]], tempHM[cell[0] - 1][cell[1]], tempHM[cell[0]][cell[1] + 1], tempHM[cell[0]][cell[1] - 1]]))
                    if (min(surrounding) >= heightMap[cell[1]][cell[0]]) and (len(surrounding_x) == 1 and surrounding_x[0] == 999): # if surrounding is not higher than water blocks and buildable
                        level.setBlockAt(box.minx + cell[1] , heightMap[cell[1]][cell[0]] - 1, box.minz + cell[0], 9)
                        level.setBlockDataAt(box.minx + cell[1] , heightMap[cell[1]][cell[0]], box.minz + cell[0], 0)
                        level.setBlockAt(box.minx + cell[1] , heightMap[cell[1]][cell[0]], box.minz + cell[0], 0)
                        break
    else:
        logger.info("No farm")