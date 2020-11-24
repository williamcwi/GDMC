import os.path
import random
import numpy
from numpy import zeros

from logger import Logger

from pymclevel import TAG_Compound, TAG_Int, TAG_Short, TAG_Byte, TAG_String, TAG_Float, TAG_Double, TAG_List
from pymclevel import MCSchematic
from pymclevel import alphaMaterials
from pymclevel.level import extractHeights
from pymclevel.box import Vector

#Export
import datetime

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

am = alphaMaterials

#naturally occuring materials
blocks = [
  am.Grass,
  am.Dirt,
  am.Stone,
  am.Bedrock,
  am.Sand,
  am.Gravel,
  am.GoldOre,
  am.IronOre,
  am.CoalOre,
  am.LapisLazuliOre,
  am.DiamondOre,
  am.RedstoneOre,
  am.RedstoneOreGlowing,
  am.Netherrack,
  am.SoulSand,
  am.Clay,
  am.Glowstone
]
blocktypes = [b.ID for b in blocks]



def createHeightMap(level, box):
    blockmask = zeros((256,), dtype='bool')
    blockmask[blocktypes] = True

    for chunk, slices, point in level.getChunkSlices(box):
            blocks = chunk.Blocks[slices]
            data = chunk.Data[slices]

            maskedBlocks = blockmask[blocks]
    
    heightMap = extractHeights(maskedBlocks)

    logger.info(heightMap)

    heightMap2File(heightMap)


    # return heightMap

def heightMap2File(heightMap):
    #TODO[Windows]:Check File Path 
    try:
        with open(os.path.join(os.path.expanduser("~/Desktop"),"HM-"+ datetime.datetime.now().strftime("%H%M%S") +".txt"), 'w+') as f:
            numpy.savetxt(f, numpy.column_stack(heightMap), fmt='%s')
            f.close()

    except Exception as e:
        logger.error(e)

def perform(level, box, options):

    try:

        # createHeightMap(level, box)

        # building_type = 'simple house'
        # randomHouse = random.randint(1, 5)
        # building = '{} {}'.format(building_type, randomHouse)

        # filename = os.path.join(os.path.dirname(__file__), 'schematics', 'simple_house', 'simple_house_{}.schematic'.format(randomHouse))
        # schematic = MCSchematic(shape=(11,6,11), filename=filename)
        # level.copyBlocksFrom(schematic, schematic.bounds, Vector(box.minx, box.miny+1, box.minz))
        
        # logger.info('Placing {} from {}'.format(building, filename))
        

    except Exception as e:
        logger.error(e)