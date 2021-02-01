from logger import Logger

logger = Logger('biomes')

def selectBiome(level, box, heightMap):
    try:
        if island(level, box, heightMap):
            return "island"
        else:
            return "default"
    except Exception as e:
        logger.error(e)

def island(level, box, heightMap):
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