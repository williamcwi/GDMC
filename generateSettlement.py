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
import removeStructures
import terrains
import cityPlanning
import biomes
import treePlacement
import brush
import farm
import path
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

        # Remove existing man made structures
        removeStructures.removeManMadeBlocks(level, box)

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
        gate_pos_1, gate_pos_2, gate_pos_3, gate_pos_4, x_gate, z_gate = generateWalls.place_walls(level, box, afterHM, combinedHM)

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

        # Convert grid and height array to 1x1
        newGridArray = common.mapArray(gridArray, startingPoint[0], startingPoint[1], box)
        newHeightArray = common.mapArray(heightArray, startingPoint[0], startingPoint[1], box)
        
        # Create buildable area array
        buildableAreaArray = cityPlanning.createBuildableAreaArray(level, box, afterHM, newGridArray, newHeightArray, startingPoint[0], startingPoint[1])

        gridArray = np.array(gridArray)
        heightArray = np.array(heightArray)

        # if platform.system()==("Darwin") and int(platform.release()[:2]) >= 19:
        #     with open(os.path.join(os.path.expanduser("~/Desktop"),'test-'+ datetime.datetime.now().strftime('%H%M%S') +'.txt'), 'w+') as f:
        #         for z in range(buildableAreaArray.shape[0]):
        #             np.savetxt(f, buildableAreaArray[z], fmt='%2.0f', newline=" ")
        #     f.close()
        # else:
        #     with open(os.path.join(os.path.dirname(__file__),'test','test-'+ datetime.datetime.now().strftime('%H%M%S') +'.txt'), 'w+') as f:
        #         for z in range(buildableAreaArray.shape[0]):
        #             np.savetxt(f, buildableAreaArray[z], fmt='%2.0f', newline=" ")
        #     f.close()
        
        # Places trees down
        treeMap = treePlacement.treePlacement(level, box, buildableAreaArray, afterHM)

        brush.run(gridArray, afterHM, startingPoint, level, box)

        farm.init(level, box, afterHM, buildableAreaArray, treeMap)

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
        
        # Include gate pavement in AfterHM
        afterHM = common.mapGatePaveToHeightMap(box.minx, box.minz, afterHM, gate_pos_1, gate_pos_2, gate_pos_3, gate_pos_4, x_gate, z_gate)

        combinedHM = terrains.findWaterSurface(whm, afterHM)

        # Path finding algorithm
        path.generatePaths(level, box, buildableAreaArray, combinedHM)

    except Exception as e:
        logger.error(e)
    
    end = time.time()
    logger.debug(u'{} sec used'.format(round(end - start, 2)))