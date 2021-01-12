from logger import Logger

from pymclevel import alphaMaterials as am

name = 'deforestation'
logger = Logger(name)

blocks = [
    #Leaves
    am.OakLeaves
    am.SpruceLeaves
    am.BirchLeaves
    am.JungleLeaves
    am.AcaciaLeaves
    am.DarkOakLeaves
    #Logs
    am.OakWood
    am.SpruceWood
    am.BirchWood
    am.JungleWood
    am.AcaciaWood
    am.DarkOakWood
]

blocktypes = [b.ID for b in blocks]
# print(blocktypes)

def setBoundingBox (box):
    # TODO: smaller bounding box
    try:
        pass
    except Exception as e:
        logger.error(e)

def removeTrees (level, box):
    try:
        pass
        # for (chunk, slices, point) in level.getChunkSlices(box):
        #     blocks = chunk.Blocks[slices]
        #     blocks[blocks == 2] = 41

            # chunk.chunkChanged()

    except Exception as e:
        logger.error(e)

def removeLogs (level, box):
    try:
        pass
        # for (chunk, slices, point) in level.getChunkSlices(box):
        #     blocks = chunk.Blocks[slices]
        #     blocks[blocks == 2] = 41

            # chunk.chunkChanged()

    except Exception as e:
        logger.error(e)