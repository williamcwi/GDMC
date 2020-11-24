import os.path
import random

from logger import Logger

from pymclevel import MCSchematic
from pymclevel.box import Vector

name = 'generateStructure'
logger = Logger(name)

def generateSimpleHouse(level, box):
    try:
        building_type = 'simple house'
        randomHouse = random.randint(1, 5)
        building = '{} {}'.format(building_type, randomHouse)

        filename = os.path.join(os.path.dirname(__file__), 'schematics', 'simple_house', 'simple_house_{}.schematic'.format(randomHouse))
        schematic = MCSchematic(shape=(11,6,11), filename=filename)
        level.copyBlocksFrom(schematic, schematic.bounds, Vector(box.minx, box.miny+1, box.minz))
        
        logger.info('Placing {} from {}'.format(building, filename))

    except Exception as e:
        logger.error(e)