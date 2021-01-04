import os.path
import platform
import numpy
from numpy import zeros, array
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

        schema = level.extractSchematic(box)
        schema.removeEntitiesInBox(schema.bounds)
        schema.removeTileEntitiesInBox(schema.bounds)

        maskedBlocks = blockmask[schema.Blocks]

        heightMap = extractHeights(maskedBlocks)
        # Row: -x to +x
        # Column: -z to +z

        logger.info('Heightmap: \n{}'.format(heightMap))

        heightMap2File(heightMap)

        return heightMap

    except Exception as e:
        logger.error(e)

def heightMap2File(heightMap):
    try:
        if platform.system()==("Darwin") and platform.release()[:2] > 19:
                with open(os.path.join(os.path.expanduser("~/Desktop"),'HM-'+ datetime.datetime.now().strftime('%H%M%S') +'.txt'), 'w+') as f:
                    numpy.savetxt(f, numpy.column_stack(heightMap), fmt='%s')
                    f.close()
        else:
            with open(os.path.join(os.path.dirname(__file__),'heightmap','HM-'+ datetime.datetime.now().strftime('%H%M%S') +'.txt'), 'w+') as f:
                numpy.savetxt(f, numpy.column_stack(heightMap), fmt='%s')
                f.close()

    except Exception as e:
        logger.error(e)