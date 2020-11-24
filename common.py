from logger import Logger
from pymclevel.box import BoundingBox

name = 'common'
logger = Logger(name)

def expandBoundingBox(box):
    try: 
        # set miny to 0
        origin = box.origin - (0, box.miny, 0)
        # set box size (y) to 256
        size = box.size + (0, 256 - (box.maxy - box.miny), 0)

        return BoundingBox(origin, size)
    except Exception as e:
        logger.error(e)