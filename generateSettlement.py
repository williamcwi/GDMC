from logger import Logger

from pymclevel import TAG_Compound, TAG_Int, TAG_Short, TAG_Byte, TAG_String, TAG_Float, TAG_Double, TAG_List

import os
import common
import heightmap
import generateStructure
import generateWalls
import deforestation
import terrains
import cityPlanning
import biomes
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
        alterDict, alterHeightDict = terrains.floodFill(hm, 169, 7)

        # Edit terrain based on height map
        terrains.editTerrainFF(level, box, alterDict, alterHeightDict)

        # Generate afterHM after Editing the terrain
        afterHM = heightmap.heightMap(level, box)

        # Return combinedHM (water and processed heightmap)
        combinedHM = terrains.findWaterSurface(whm, afterHM)

        # Remove lava pools
        terrains.removeLava(level, box, lhm, ghm, afterHM)

        # Generate walls
        generateWalls.place_walls(level, box, afterHM, combinedHM)

        # Calculate best starting point and array of buildable 4x4 areas
        startingPoint, gridArray = cityPlanning.bestStartingPoint(box, afterHM)

        # # Generate simple house
        # generateStructure.generateSimpleHouse(level, box)

    except Exception as e:
        logger.error(e)
    
    end = time.time()
    logger.debug(u'{} sec used'.format(round(end - start, 2)))