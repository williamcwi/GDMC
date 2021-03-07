import math
from logger import Logger

name = 'treePlacement'
logger = Logger(name)

def treePlacement(level, box):
    try:
        trees = []
        start = [box.minx, box.minz]
       
        # loops through the z-axis within the box selection and dividing it into 11 sections |
        for z in range(int(math.ceil((box.maxz-(box.minz))/11))):
            tempStart = [start[0]-z, start[1]+(11*z)]
            if z == 1:
                bottomStart = trees[len(trees)-1]
            # checks if the start is within the box x-axis selection and z-axis selection
            if box.minx <= tempStart[0] <= box.maxx and box.minz <= tempStart[1] <= box.maxz:
                trees.append(tempStart)
            # loops through the x-axis within the box selection and dividing it into 11 sections
            for x in range(int(math.ceil((box.maxx-(box.minx-z))/11))):
                position = [tempStart[0]+(11*x), tempStart[1]+x]
                # checks if the position is within the box x-axis selection and box z-axis selection
                if box.minx <= position[0] <= box.maxx and box.minz <= position[1] <= box.maxz:
                    trees.append(position)
                else:
                    if position[0] <= box.maxx and position[1] <= box.maxz:
                        continue
                    else:
                        break
        
        for z in range(int(math.ceil((box.maxz-(box.minz))/11))):
            tempStart = [bottomStart[0]+z, bottomStart[1]-(11*z)]
            if z == 0:
                pass
            if box.minx <= tempStart[0] <= box.maxx and box.minz <= tempStart[1] <= box.maxz:
                trees.append(tempStart)
            for x in range(int(math.ceil((box.maxx-(box.minx-z))/11))):
                position = [tempStart[0]-(11*x), tempStart[1]-x]
                if box.minx <= position[0] <= box.maxx and box.minz <= position[1] <= box.maxz:
                    trees.append(position)
                else: 
                    if position[0] >= box.minx and position[1] >= box.minz:
                        continue
                    else:
                        break
        #print(trees)
    
    except Exception as e:
        logger.error(e)