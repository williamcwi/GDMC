import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('HM-135951.txt', header=None, delimiter=r'\s+')

fig, ax = plt.subplots(figsize=(12, 7))
title = 'Heightmap of Box Selection'

plt.title(title, fontsize=13)
ttl = ax.title
ttl.set_position([0.5, 1.05])

ax.set_xticks([])
ax.set_yticks([])

ax.axis('off')

sns.heatmap(df, annot=None, fmt='', cmap='RdYlGn', linewidths=0.30, ax=ax)
plt.show()