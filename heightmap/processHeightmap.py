import numpy as np
import pandas as pd
import scipy as sp

heightmap = input()
df = pd.read_csv('{}'.format(heightmap), header=None, delimiter=r'\s+')

data = df.to_numpy()
print(data)
#Translates 2D array to 3D Binary array
for height in range(50, 75): # for height in dataset
    new_heightmap = []
    for i in data: # row
        new_row = []
        for j in i:
            if (j == height): # if cell matches current height
                new_row.append(1)
            else:
                new_row.append(0)
        new_heightmap.append(new_row)
    # print(new_heightmap)

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