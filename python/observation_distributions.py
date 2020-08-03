"""
Author: David Sergio

Elevation/Aspect/Rsize/Type Distribution Analysis
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

# observation_data.groupby(['Asp','Rsize']).size().unstack().plot(kind='bar',stacked=True, ylabel='Observations')
# plt.savefig(".\\plots\\" + "aspect_Rsize.png")

# observation_data.groupby(['ElevTL','Rsize']).size().unstack().plot(kind='bar',stacked=True, ylabel='Observations')
# plt.savefig(".\\plots\\" + "elev_Rsize.png")

# observation_data.groupby(['Asp','Type']).size().unstack().plot(kind='bar',stacked=True, ylabel='Observations')
# plt.savefig(".\\plots\\" + "aspect_type.png")

# observation_data.groupby(['Asp','ElevTL']).size().unstack().plot(kind='bar',stacked=True, ylabel='Observations')
# plt.savefig(".\\plots\\" + "aspect_elev.png")

observation_data.groupby(['ElevTL','Type']).size().unstack().plot(kind='bar',stacked=True, ylabel='Observations')
plt.savefig(".\\plots\\" + "elev_type.png")