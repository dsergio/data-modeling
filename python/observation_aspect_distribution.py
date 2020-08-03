"""
Author: David Sergio

Aspect Distribution Analysis
"""

import numpy as np
import pandas as pd
# import matplotlib as plt
import matplotlib.pyplot as plt
from numpy import nan

from os import listdir
from os.path import isfile, join


observationExtractStage1 = "..\\extract\\observations\\stage1\\CAIC_avalanches_2008-10-01_2020-07-31.csv"
observation_data = pd.read_csv(observationExtractStage1)

for col in observation_data.columns: 
	observation_data[col] = observation_data[col].replace("", nan)
	observation_data[col] = observation_data[col].replace(" ", nan)
	observation_data[col] = observation_data[col].replace("NA", nan)
	observation_data[col] = observation_data[col].replace("?", nan)

aspect_counts = observation_data['Asp'].value_counts()

print(aspect_counts.index)
print(aspect_counts.values)

# Bar Graph Aspect
# 
plt.bar(aspect_counts.index, aspect_counts.values)
plt.title("Aspect/Observations Bar Chart")
plt.xlabel("Aspect")
plt.ylabel("Observations")
plt.savefig(".\\plots\\aspect.png")

