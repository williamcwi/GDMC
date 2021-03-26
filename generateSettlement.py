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
        
        # Remove lava pools
        terrains.removeLava(level, box, lhm, ghm, hm)

        # Generate afterHM after Editing the terrain
        afterHM = heightmap.heightMap(level, box)

        terrains.execute(level, box, afterHM, whm, 256, 7)
        # Generate afterHM after Editing the terrain
        afterHM = heightmap.heightMap(level, box)

        # Return combinedHM (water and processed heightmap)
        combinedHM = terrains.findWaterSurface(whm, afterHM)
        
        # Generate walls
        generateWalls.place_walls(level, box, afterHM, combinedHM)

        # Obtain new afterHM after placing walls
        afterHM = heightmap.heightMap(level, box)

        # Calculate best starting point and array of buildable 4x4 areas
        startingPoint, gridArray, innerGridArray, heightArray, innerHeightArray = cityPlanning.bestStartingPoint(box, afterHM)

        # Expand buildable areas
        gridArray, heightArray = cityPlanning.expandBuildableAreas(level, box, afterHM, gridArray, innerGridArray, heightArray, innerHeightArray, startingPoint[0], startingPoint[1])

        # Remove buildable areas that is too small
        gridArray = cityPlanning.screening(gridArray)

        # Add border around buildable areas
        cityPlanning.addBorder(level, box, gridArray, heightArray, startingPoint[0], startingPoint[1])

        brush.run(gridArray, afterHM, startingPoint, level, box)

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
                    # np.savetxt(f, buildableAreaArray[z], fmt='%2.0f', newline=" ")
            # f.close()
        # else:
            # with open(os.path.join(os.path.dirname(__file__),'test','test-'+ datetime.datetime.now().strftime('%H%M%S') +'.txt'), 'w+') as f:
                    # np.savetxt(f, buildableAreaArray[z], fmt='%2.0f', newline=" ")
            # f.close()

        # Places trees down
        # treePlacement.treePlacement(level, box, mapArr, afterHM)

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