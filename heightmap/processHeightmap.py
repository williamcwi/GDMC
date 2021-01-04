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