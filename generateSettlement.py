from logger import Logger

from pymclevel import TAG_Compound, TAG_Int, TAG_Short, TAG_Byte, TAG_String, TAG_Float, TAG_Double, TAG_List

import os
import sys
import platform
import datetime
import common
import heightmap
import generateStructure
import generateWalls
import deforestation
import terrains
import cityPlanning
import biomes
import brush
import time
import numpy as np

inputs = [
    (
        ('Settlement Generator', 'title'),
        
        ('By William, Selina, Ho Kiu, Rhys', 'label'),
        ('', 'label'),

    ),
    (
        ('Settlement Settings', 'title'),
    )
]

name = 'generateSettlement'
logger = Logger(name)

def perform(level, box, options):
    start = time.time()
    try:
        # Expand box to include entire y-axis
        box = common.expandBoundingBox(box)

        # Deforestation
        deforestation.removeFoliage(level, box)

        # Create Height Map
        hm = heightmap.heightMap(level, box)
        whm = heightmap.waterHeightMap(level, box)
        lhm = heightmap.lavaHeightMap(level, box)
        ghm = heightmap.createHeightMap(level, box)

        # Select biome
        biome, isIsland = biomes.selectBiome(level, box, hm)

        # TODO: Add test of selected area size for wall generation
        alterDict, alterHeightDict = terrains.floodFill(hm, whm, 256, 7)

        # Edit terrain based on height map
        terrains.editTerrainFF(level, box, alterDict, alterHeightDict)

        # Generate afterHM after Editing the terrain
        afterHM = heightmap.heightMap(level, box)

        # Return combinedHM (water and processed heightmap)
        combinedHM = terrains.findWaterSurface(whm, afterHM)
        terrains.removeSurfaceWater(level, box, 9, afterHM, combinedHM)
        
        # Remove lava pools
        terrains.removeLava(level, box, lhm, ghm, afterHM)
        
        # Generate walls
        generateWalls.place_walls(level, box, afterHM, combinedHM)

        # Obtain new afterHM after placing walls
        afterHM = heightmap.heightMap(level, box)

        # Calculate best starting point and array of buildable 4x4 areas
        startingPoint, gridArray, innerGridArray, heightArray, innerHeightArray = cityPlanning.bestStartingPoint(box, afterHM)

        # Expand buildable areas
        gridArray, heightArray = cityPlanning.expandBuildableAreas(level, box, afterHM, gridArray, innerGridArray, heightArray, innerHeightArray, startingPoint[0], startingPoint[1])

        # Add border around buildable areas
        cityPlanning.addBorder(level, box, gridArray, heightArray, startingPoint[0], startingPoint[1])

        # Convert grid and height array to 1x1
        gridArray = common.mapArray(gridArray)
        heightArray = common.mapArray(heightArray)

        # Create buildable area array
        buildableAreaArray = cityPlanning.createBuildableAreaArray(level, box, afterHM, gridArray, heightArray, startingPoint[0], startingPoint[1])

        # gridArray = np.array(gridArray)
        # heightArray = np.array(heightArray)
        # if platform.system()==("Darwin") and int(platform.release()[:2]) >= 19:
            # with open(os.path.join(os.path.expanduser("~/Desktop"),'test-'+ datetime.datetime.now().strftime('%H%M%S') +'.txt'), 'w+') as f:
                # for z in range(buildableAreaArray.shape[0]):
                # for z in range(gridArray.shape[0]):
                    # for x in range(gridArray.shape[1]):
                        # print(level.blockAt(box.minx + x + startingPoint[0], afterHM[x][z] - 1, box.minz + z + startingPoint[1]))
                        # np.savetxt(f, level.blockAt(box.minx + x + startingPoint[0], afterHM[x][z] - 1, box.minz + z + startingPoint[1]), fmt='%3.0f', newline= " ")
                    # np.savetxt(f, buildableAreaArray[z], fmt='%2.0f', newline=" ")
            # f.close()
        # else:
            # with open(os.path.join(os.path.dirname(__file__),'test','test-'+ datetime.datetime.now().strftime('%H%M%S') +'.txt'), 'w+') as f:
                # for z in range(buildableAreaArray.shape[1]):
                # for z in range(gridArray.shape[0]):
                    # xlist = np.full(gridArray.shape[0], 0)
                    # for x in range(gridArray.shape[1]):
                        # xlist[x] = level.blockAt(box.minx + x + startingPoint[0], afterHM[x][z] - 1, box.minz + z + startingPoint[1])
                    # np.savetxt(f, xlist, fmt='%2.0f', newline= " ")
                    # np.savetxt(f, buildableAreaArray[z], fmt='%2.0f', newline=" ")
            # f.close()

        # Places trees down
        treePlacement.treePlacement(level, box, mapArr, afterHM)

        afterHM = heightmap.heightMap(level, box)
        brush.run(gridArray, afterHM, startingPoint, level, box)

        #---------->Experimential
        # incstart = time.time()
        # brush.CTPFF(afterHM, 9, 169, level, box)
        # incend = time.time()
        # logger.debug(u'{} sec used'.format(round(incend - incstart, 2)))

        #---------->Genetic A
        # # Determine plots
        # plots.run(gridArray)

        # # Generate simple house
        # generateStructure.generateSimpleHouse(level, box)
        
        # # Path finding algorithm
        # path.run()

    except Exception as e:
        logger.error(e)
    
    end = time.time()
    logger.debug(u'{} sec used'.format(round(end - start, 2)))