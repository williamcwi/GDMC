import numpy as np
import pandas as pd
import scipy as sp

import platform
import os.path
import datetime


heightmap = "/Users/hokiulam/Desktop/HM-154425.txt"
df = pd.read_csv('{}'.format(heightmap), header=None, delimiter=r'\s+')

data = df.to_numpy()
# print(data)

# Translates 2D array to 3D Binary array
def heightmap2binary(data):
    binary_heightmap = []
    for height in range(min(map(min, data)), max(map(max, data))+1): # for height in dataset
        new_heightmap = []
        for i in data: # row
            new_row = []
            for j in i:
                if (j == height): # if cell matches current height
                    new_row.append(1)
                else:
                    new_row.append(0)
            new_heightmap.append(new_row)
        binary_heightmap.append(new_heightmap)
    # print(binary_heightmap)
    return binary_heightmap

# Connected Component Labelling
def CCL(heightMap): ################# TODO:VERIFY #################
    region = 1 # region label
    minHM = min(map(min,heightMap)) # get lowerbound of level
    maxHM = max(map(max,heightMap)) # get upperbound of level
    maskedHM = [[[0 for k in range(len(heightMap))] for j in range(len(heightMap[0]))] for i in range((maxHM - minHM) + 1)] # initialse post-process HM

    for x in range(0, len(heightMap)): # for row
        for z in range(0, len(heightMap[x])): # for column
            upregion = leftregion = -1 # initalise neighbour region
            uplevel = leftlevel = 999 # initalise neighbour level
            level = heightMap[x][z]
            maskedlevel = level - minHM
            if level >= 0: # if not lava or water
                if x != 0:
                    if heightMap[x-1][z] == level:
                        upregion = maskedHM[maskedlevel][x-1][z]
                        uplevel = heightMap[x-1][z]
                if z != 0:
                    if heightmap[x][z-1] == level:
                        leftregion = maskedHM[maskedlevel][x][z-1]
                        leftlevel = heightMap[x][z-1]
                
                if level == uplevel or level == leftlevel:
                    if leftregion > 0 != upregion > 0:# if only one neighbour belongs to a region
                        maskedHM[maskedlevel][x][z] = max(leftregion, upregion)
                    elif (leftregion > 0 and upregion > 0) and (leftregion != upregion) and (level == leftlevel and level == uplevel):# if conflicts
                        min_region, max_region = min(leftregion, upregion), max(leftregion, upregion)
                        maskedHM[maskedlevel][x][z] = max_region
                        maskedHM[maskedlevel] = [[e if e!=max_region else min_region for e in r] for r in maskedHM[maskedlevel]]
                else: # if new region
                    maskedHM[maskedlevel][x][z] = region
                    region = region + 1
    #heightMap2File(maskedHM[0])
    return maskedHM

def heightMap2File(heightMap):
    if platform.system()==("Darwin") and int(platform.release()[:2]) >= 19:
        with open(os.path.join(os.path.expanduser("~/Desktop"),'HMS-'+ datetime.datetime.now().strftime('%H%M%S') +'.txt'), 'w+') as f:
            np.savetxt(f, heightMap, fmt='%s')
            f.close()
    else:
        with open(os.path.join(os.path.dirname(__file__),'heightmap','HMS-'+ datetime.datetime.now().strftime('%H%M%S') +'.txt'), 'w+') as f:
            np.savetxt(f, heightMap, fmt='%s')
            f.close()


    # # Sobel Operator
    # edge_map = []
    # for i in range(len(new_heightmap)): # row
    #     if i == 0:
    #         edge_map.append(np.zeros(256).astype(int).tolist())
    #     else:
    #         edge_row = []
    #         for j, k in zip(new_heightmap[i], new_heightmap[i-1]): # compare current row and previous row
    #             if j == k:
    #                 edge_row.append(0)
    #             else:
    #                 edge_row.append(1)
    #         edge_map.append(edge_row)
    # print(edge_map)

CCL(data)