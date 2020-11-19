import os.path
from datetime import datetime as dt

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
        ('simple house design', (1, 1, 5)),
    )
]

name = 'generateSettlement'

def perform(level, box, options):

    building_type = 'simple house'
    selection = options['simple house design']
    building = '{} {}'.format(building_type, selection)

    filename = '{}\schematics\simple_house\simple_house_{}.schematic'.format(os.path.dirname(__file__), selection)
    schematic = MCSchematic(shape=(11,6,11), filename=filename)
    level.copyBlocksFrom(schematic, schematic.bounds, Vector(box.minx, box.miny+1, box.minz))
    
    print('{} {} INFO: Placing {} from {}'.format(dt.now(), name, building, filename))
