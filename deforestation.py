from logger import Logger

from pymclevel import alphaMaterials as am

name = 'deforestation'
logger = Logger(name)

tree = [
    #Leaves
    am.Leaves,
    am.PineLeaves,
    am.BirchLeaves,
    am.JungleLeaves,
    am.AcaciaLeaves,
    am.DarkOakLeaves,
    #Logs
    am.Wood,
    am.PineWood, #Spruce
    am.BirchWood,
    am.JungleWood,
    am.Wood2, #Acacia and dark oak wood
]

treeID = [t.ID for t in tree]

def removeTrees(level, box):
    try:
        for (chunk, slices, point) in level.getChunkSlices(box):
            blocks = chunk.Blocks[slices]
        #     Change blocks to air
            for t in treeID:
                blocks[blocks == t] = 0
            chunk.dirty = True

    except Exception as e:
        logger.error(e)