from logger import Logger

from pymclevel import alphaMaterials as am
from pymclevel.box import Vector
from pymclevel.box import BoundingBox

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

logs = [
    am.Wood,
    am.PineWood,
    am.BirchWood,
    am.JungleWood,
    am.Wood2,
]

treeID = [t.ID for t in tree]
logsID = [l.ID for l in logs]

# Creates a smaller box within selection to get rid of trees 
def setBoundingBox(box):
    # TODO: smaller bounding box
    try:
        # Starts 3 blocks inside selection 
        origin = Vector((box.minx+3), box.miny, (box.minz+3))
        # Makes box selection smaller
        size =  Vector((box.maxx-box.minx-6), (box.maxy - box.miny), (box.maxz-box.minz-6))

        return BoundingBox(origin, size)

    except Exception as e:
        logger.error(e)

def removeTrees(level, box):
    try:
        for (chunk, slices, point) in level.getChunkSlices(box):
            blocks = chunk.Blocks[slices]
        #     Change blocks to air
            for t in treeID:
                blocks[blocks == t] = 0
                #logger.info("Going through loop")
        # chunk.chunkChanged()

    except Exception as e:
        logger.error(e)

def removeLogs(level, box):
    try:
        
        for (chunk, slices, point) in level.getChunkSlices(box):
            blocks = chunk.Blocks[slices]
        #     Change blocks to air
            for l in logsID:
                blocks[blocks == l] = 0
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