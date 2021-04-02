from logger import Logger

from pymclevel import alphaMaterials as am

name = 'deforestation'
logger = Logger(name)

foliage = [
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
    # Other foliage
    am.Cactus,
    am.TallGrass,
    am.UnusedShrub,
    am.Shrub,
    am.DesertShrub2,
    am.Flower,
    am.Rose,
    am.TallFlowers,
    am.BrownMushroom,
    am.RedMushroom,
    am.HugeBrownMushroom,
    am.HugeRedMushroom,
    am.Vines,
    am.SugarCane,
    am.Pumpkin,
    am.CocoaPlant,
    # Other
    am.SnowLayer,
    am.Snow
]

foliageID = [f.ID for f in foliage]

def removeFoliage(level, box):
    try:
        for (chunk, slices, point) in level.getChunkSlices(box):
            blocks = chunk.Blocks[slices]
            # Change blocks to air
            for f in foliageID:
                blocks[blocks == f] = 0
            chunk.dirty = True
        
        logger.info('Removing foliage...')

    except Exception as e:
        logger.error(e)