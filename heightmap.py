import os.path
import numpy
from numpy import zeros
import datetime

from logger import Logger

from pymclevel import alphaMaterials
from pymclevel.level import extractHeights

name = 'heightmap'
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
    try:
        blockmask = zeros((256,), dtype='bool')
        blockmask[blocktypes] = True

        for chunk, slices, point in level.getChunkSlices(box):
            blocks = chunk.Blocks[slices]
            data = chunk.Data[slices]

            maskedBlocks = blockmask[blocks]

            heightMap = extractHeights(maskedBlocks)

            logger.info('Heightmap: \n{}'.format(heightMap))

            # heightMap2File(heightMap)

        # return heightMap

    except Exception as e:
        logger.error(e)

def heightMap2File(heightMap):
    #TODO[Windows]:Check File Path 
    try:
        with open(os.path.join(os.path.expanduser("~/Desktop"),"HM-"+ datetime.datetime.now().strftime("%H%M%S") +".txt"), 'ab') as f:
            f.write(b"\n")
            numpy.savetxt(f, numpy.column_stack(heightMap), fmt='%s')
            f.close()

    except Exception as e:
        logger.error(e)