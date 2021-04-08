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

# np.set_printoptions(threshold=sys.maxsize)

inputs = [
    (
        ('2021 Settlement Generation Challenge', 'title'),
        
        ('By William, Selina, Ho Kiu, Rhys', 'label'),
        ('University of Kent - CO600 submission', 'label'),
        ('', 'label'),
        ('Installation: ', 'label'),
        ('1. Drop all files in MCEdit filters folder, including the schematics folder', 'label'),
        ('2. Make a selection of where to generate the settlement', 'label'),
        ('The filter script will automatically select 1 to 256 for y-axis', 'label'),
        ('3. Click on filter -> filter', 'label'),
        ('4. Wait for settlement to generate', 'label'),
        ('Generation time may vary depending of the selection', 'label'),
        ('Check terminal for information on generation progress', 'label'),

    )# ,
    # (
    #     ('Settlement Settings', 'title'),
    # )
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

        # Convert grid and height array to 1x1
        newGridArray = common.mapArray(gridArray, startingPoint[0], startingPoint[1], box)
        newHeightArray = common.mapArray(heightArray, startingPoint[0], startingPoint[1], box)
        
        # Create buildable area array
        buildableAreaArray = cityPlanning.createBuildableAreaArray(level, box, afterHM, newGridArray, newHeightArray, startingPoint[0], startingPoint[1])

        gridArray = np.array(gridArray)
        heightArray = np.array(heightArray)
        
        # Include gate pavement in AfterHM
        afterHM = common.mapGatePaveToHeightMap(box.minx, box.minz, afterHM, gate_pos_1, gate_pos_2, gate_pos_3, gate_pos_4, x_gate, z_gate)
        whm = heightmap.waterHeightMap(level, box)

        combinedHM = terrains.findWaterSurface(whm, afterHM)
        
        # Places trees down and return treeMap
        treeMap = treePlacement.treePlacement(level, box, buildableAreaArray, afterHM)

        # Add border around buildable areas
        cityPlanning.addBorder(level, box, gridArray, heightArray, startingPoint[0], startingPoint[1])

        # Building Allocation
        brush.run(gridArray, afterHM, startingPoint, level, box)

        # Constructing Farm
        farm.init(level, box, afterHM, buildableAreaArray, treeMap)

        # Path finding algorithm
        path.generatePaths(level, box, buildableAreaArray, treeMap, combinedHM)

    except Exception as e:
        logger.error(e)
    
    end = time.time()
    logger.debug(u'{} sec used'.format(round(end - start, 2)))