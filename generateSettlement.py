from logger import Logger

from pymclevel import TAG_Compound, TAG_Int, TAG_Short, TAG_Byte, TAG_String, TAG_Float, TAG_Double, TAG_List

import os
import common
import heightmap
import generateStructure
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
        heightMap = heightmap.heightMap(level, box)

        # TODO: move to separate file
        # Read height map difference file to string array (replace with correct file path)
        with open('C:/Users/Rhys/Documents/coursework/Year 3/CO600 - Project/mcedit/stock-filters/HMD-145407.txt') as heightMapDiff:
            lines = [line.split() for line in heightMapDiff]
        # Convert string array to int
        heightMapDiffInt = [list(map(int,i)) for i in lines]

        # Edit terrain based on height map
        terrains.editTerrain(level, box, heightMap, heightMapDiffInt)

        # Generate simple house
        # generateStructure.generateSimpleHouse(level, box)

    except Exception as e:
        logger.error(e)