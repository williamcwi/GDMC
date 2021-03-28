from logger import Logger
from pymclevel.box import BoundingBox
import numpy as np

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

def mapArray(array, xoffset, zoffset, box):
    try:
        mapArr = []
        for z in array:
            row = []
            for x in z:
                block = [x] * 4
                row.extend(block)
            for i in range(4):
                mapArr.append(row)
        mapArr = np.array(mapArr)
        mapArr = np.pad(mapArr, ((zoffset, 0), (xoffset, 0)), 'constant')
        if xoffset > 0:
            for i in range(xoffset):
                mapArr = np.delete(mapArr, (mapArr.shape[1] - 1), axis = 1)
        if zoffset > 0:
            for i in range(zoffset):
                mapArr = np.delete(mapArr, (mapArr.shape[0] - 1), axis = 0)
        while mapArr.shape[0] > box.length:
            mapArr = np.delete(mapArr, (mapArr.shape[0] - 1), axis = 0)
        while mapArr.shape[1] > box.width:
            mapArr = np.delete(mapArr, (mapArr.shape[1] - 1), axis = 1)
        return mapArr
    except Exception as e:
        logger.error(e)