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
  am.Glowstone,
  am.Sandstone
]
blocktypes = [b.ID for b in blocks]

water = [
    am.Water,
    am.WaterActive,
    am.Bedrock
]
waterID = [w.ID for w in water]

lava = [
    am.Lava,
    am.LavaActive,
    am.Bedrock
]
lavaID = [l.ID for l in lava]

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

        # logger.info('Heightmap: \n{}'.format(heightMap))

        # heightMap2File(heightMap)

        return heightMap

    except Exception as e:
        logger.error(e)

# Gets the height of the water
def waterHeightMap(level, box):
    try:
        blockmask = zeros((256,), dtype='bool')
        blockmask[waterID] = True

        schema = level.extractSchematic(box)
        schema.removeEntitiesInBox(schema.bounds)
        schema.removeTileEntitiesInBox(schema.bounds)

        maskedBlocks = blockmask[schema.Blocks]

        waterHeightMap = extractHeights(maskedBlocks)
        # Row: -x to +x
        # Column: -z to +z

        # logger.info('Water Heightmap: \n{}'.format(waterHeightMap))

        # heightMap2File(waterHeightMap)

        return waterHeightMap
        
    except Exception as e:
        logger.error(e)

# Gets the height of the lava
def lavaHeightMap (level, box):
    try:
        blockmask = zeros((256,), dtype='bool')
        blockmask[lavaID] = True

        schema = level.extractSchematic(box)
        schema.removeEntitiesInBox(schema.bounds)
        schema.removeTileEntitiesInBox(schema.bounds)

        maskedBlocks = blockmask[schema.Blocks]

        lavaHeightMap = extractHeights(maskedBlocks)
        # Row: -x to +x
        # Column: -z to +z


        # logger.info('Lava Heightmap: \n{}'.format(lavaHeightMap))

        # heightMap2File(lavaHeightMap)

        return lavaHeightMap
    except Exception as e:
        logger.error(e)

def heightMap(level, box):
    try:
        ground_heightmap = createHeightMap(level, box)
        water_heightmap = waterHeightMap(level, box)
        lava_heightmap = lavaHeightMap(level, box)

        heightmap = []
        for ga, wa, la in zip(ground_heightmap, water_heightmap, lava_heightmap):
            row = []
            for g, w, l in zip(ga, wa, la):
                if g > w and g > l:
                    row.append(g)
                elif w > l:
                    row.append(-1) # water
                else:
                    row.append(-2) # lava
            heightmap.append(row)
        
        logger.info('Generating heightmap...')

        # heightMap2File(heightmap)

        return heightmap
    except Exception as e:
        logger.error(e)

def heightMap2File(heightMap):
    try:
        if platform.system()==("Darwin") and platform.release()[:2] >= 19:
                with open(os.path.join(os.path.expanduser("~/Desktop"),'HM-'+ datetime.datetime.now().strftime('%H%M%S') +'.txt'), 'w+') as f:
                    numpy.savetxt(f, numpy.column_stack(heightMap), fmt='%s')
                    f.close()
        else:
            with open(os.path.join(os.path.dirname(__file__),'heightmap','HM-'+ datetime.datetime.now().strftime('%H%M%S') +'.txt'), 'w+') as f:
                numpy.savetxt(f, numpy.column_stack(heightMap), fmt='%s')
                f.close()

    except Exception as e:
        logger.error(e)