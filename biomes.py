from logger import Logger
import math
import collections
import numpy as np

logger = Logger('biomes')

def selectBiome(level, box, heightMap):
    try:
        biomeArray = np.array([])
        for z in range(0, box.length, 16):
            for x in range(0, box.width, 16):
                chunk = level.getChunk((box.minx + x)/16, (box.minz + z)/16)
                array = np.array(chunk.root_tag["Level"]["Biomes"].value)
                biomeArray = np.concatenate((biomeArray, array))
        biomeCounter = collections.Counter(biomeArray)
        biome = max(biomeArray, key = biomeCounter.get)
        return biome, isIsland(level, box, heightMap)
    except Exception as e:
        logger.error(e)

def isIsland(level, box, heightMap):
    try:
        waterBorderBlocks = 0
        for z in range(box.length):
            for x in range(box.width):
                if z == 0 or z == box.length - 1 or x == 0 or x == box.width - 1:
                    if heightMap[x][z] == -1:
                        waterBorderBlocks += 1
        # print(waterBorderBlocks)
        if waterBorderBlocks >= (((box.length + box.width) * 2) - 2) * 0.8:
            return True
        return False
    except Exception as e:
        logger.error(e)