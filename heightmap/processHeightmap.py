import numpy as np
import pandas as pd
import scipy as sp

heightmap = input()
df = pd.read_csv('{}'.format(heightmap), header=None, delimiter=r'\s+')

data = df.to_numpy()
# print(data)

# Translates 2D array to 3D Binary array
def heightmap2binary(data):
    binary_heightmap = []
    for height in range(min(map(min, data))-1, max(map(max, data))+1): # for height in dataset
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
def CCL(binary_heightmap):
    maskedHM = []
    for level in binary_heightmap: # for every height level
        maskedLevel = [[0]*256]*256
        region = 1
        if sum(sum(level, []))>=1: # if there are blocks in the level
            area = sum(sum(level, [])) # calc the area in level
            #pos = zip(*np.where(level = 1)) # position of blocks
            #for item in pos:
            for x in range(0, len(level)-1): # row
                for y in range(0, len(level[x])-1): # cell
                    if level[x][y] == 1:
                        maskedLevel[x][y] = region
                        if not(y == 255):
                            if maskedLevel[x][y-1] != 0:
                                maskedLevel[x][y] = maskedLevel[x][y-1]
                        if not(x == 0):
                            if maskedLevel[x-1][y] != 0:
                                maskedLevel[x][y] = maskedLevel[x-1][y]
                        if (maskedLevel[x][y-1] != 0) and (maskedLevel[x-1][y] != 0):
                            min_region, max_region = min(maskedLevel[x][y-1], maskedLevel[x-1][y]), max(maskedLevel[x][y-1], maskedLevel[x-1][y])
                            maskedLevel = [[e if e!=max_region else min_region for e in r] for r in maskedLevel]
                        region = region + 1
        maskedHM.append(maskedLevel)
    print(maskedHM)
    return maskedHM

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

if __name__ == "__main__":
    CCL(heightmap2binary(data))