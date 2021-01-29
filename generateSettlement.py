from logger import Logger

from pymclevel import TAG_Compound, TAG_Int, TAG_Short, TAG_Byte, TAG_String, TAG_Float, TAG_Double, TAG_List

import os
import common
import heightmap
import generateStructure
import generateWalls
import deforestation
import terrains

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

    try:
        # Expand box to include entire y-axis
        box = common.expandBoundingBox(box)

        # Deforestation
        deforestation.removeTrees(level, box)

        # Create Height Map
        hm = heightmap.heightMap(level, box)
        whm = heightmap.waterHeightMap(level, box)

        # TODO: Add test of selected area size for wall generation
        alterDict, alterHeightDict = terrains.floodFill(hm, 169, 7)

        # Edit terrain based on height map
        terrains.editTerrainFF(level, box, alterDict, alterHeightDict)

        # Get new heightmap
        afterHM = heightmap.heightMap(level, box)

        # Return combinedHM (water and processed heightmap)
        combinedHM = terrains.findWaterSurface(whm, afterHM)

        # Generate walls
        generateWalls.place_walls(level, box, afterHM, combinedHM)

        # # Generate simple house
        # generateStructure.generateSimpleHouse(level, box)

    except Exception as e:
        logger.error(e)