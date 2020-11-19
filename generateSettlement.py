import os.path
import random

from logger import Logger

from pymclevel import TAG_Compound, TAG_Int, TAG_Short, TAG_Byte, TAG_String, TAG_Float, TAG_Double, TAG_List
from pymclevel import MCSchematic
from pymclevel.box import Vector

inputs = [
    (
        ('Settlement Generator', 'title'),
        
        ('By William, Selina, Ho Kiu, Rhys', 'label'),
        ('', 'label'),

    ),
    (
        ('Settlement Settings', 'title'),
    )
]

name = 'generateSettlement'
logger = Logger(name)

def perform(level, box, options):

    building_type = 'simple house'
    randomHouse = random.randint(1, 5)
    building = '{} {}'.format(building_type, randomHouse)

    filename = '{}\schematics\simple_house\simple_house_{}.schematic'.format(os.path.dirname(__file__), randomHouse)
    schematic = MCSchematic(shape=(11,6,11), filename=filename)
    level.copyBlocksFrom(schematic, schematic.bounds, Vector(box.minx, box.miny+1, box.minz))
    
    logger.info('Placing {} from {}'.format(building, filename))