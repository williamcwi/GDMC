from pymclevel import TAG_Compound, TAG_Int, TAG_Short, TAG_Byte, TAG_String, TAG_Float, TAG_Double, TAG_List, MCSchematic
from pymclevel.box import Vector

displayName = "600 Schematic Test"

inputs = (
	  ("To test placement of structure via schematics, initial hex at min x and minz", "label"),
)

def perform(level, box, options):
            filename = "./stock-filters/GDMC_Submission_Files/Schematics/House1.schematic"
            schematic = MCSchematic(shape="(17,11,13)", filename=filename)
            level.copyBlocksFrom(schematic, schematic.bounds, Vector(box.minx, box.miny, box.minz))
