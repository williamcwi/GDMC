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
        # TODO: Add test of selected area size for wall generation
        alterDict, alterHeightDict = terrains.floodFill(hm, 169, 9)
        # Read height map difference file to string array (replace with correct file path)
        # with open('C:/Users/Rhys/Documents/coursework/Year 3/CO600 - Project/mcedit/stock-filters/HMD-145407.txt') as heightMapDiff:
        #     lines = [line.split() for line in heightMapDiff]
        # Convert string array to int
        # heightMapDiffInt = [list(map(int,i)) for i in lines]
        # Edit terrain based on height map
        terrains.editTerrainFF(level, box, alterDict, alterHeightDict)
        # terrains.editTerrain(level, box, hm, diffHM)

        # # Generate simple house
        # generateStructure.generateSimpleHouse(level, box)
        # Generate walls
        generateWalls.place_walls(level, box, hm)

    except Exception as e:
        logger.error(e)