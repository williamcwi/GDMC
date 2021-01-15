from logger import Logger

from pymclevel import alphaMaterials as am

name = 'deforestation'
logger = Logger(name)

tree = [
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

logs = [
    am.OakWood
    am.SpruceWood
    am.BirchWood
    am.JungleWood
    am.AcaciaWood
    am.DarkOakWood
]

treeID = [t.ID for t in tree]
logsID = [l.ID for l in logs]
# print(blocktypes)

def setBoundingBox(box):
    # TODO: smaller bounding box
    try:
        pass
    except Exception as e:
        logger.error(e)

def removeTrees(level, box):
    try:
        pass
        # for (chunk, slices, point) in level.getChunkSlices(box):
        #     blocks = chunk.Blocks[slices]
        #     Change blocks to air
        #     blocks[blocks == 2] = 0

            # chunk.chunkChanged()

    except Exception as e:
        logger.error(e)

def removeLogs(level, box):
    try:
        pass
        # for (chunk, slices, point) in level.getChunkSlices(box):
        #     blocks = chunk.Blocks[slices]
        #     blocks[blocks == 2] = 41

            # chunk.chunkChanged()

    except Exception as e:
        logger.error(e)

def deforestation(level, box):
    try:

        big_box = box
        small_box = setBoundingBox(box)

        removeTrees(level, small_box)
        removeLogs(level, big_box)

    except Exception as e:
        logger.error(e)