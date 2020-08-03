"""
Author: David Sergio

Perform transform operations on data from
Colorado Avalanche Information Center (CAIC) 
"""

import numpy as np
import pandas as pd
# import matplotlib as plt
import matplotlib.pyplot as plt
from numpy import nan

from os import listdir
from os.path import isfile, join

from transformFunctions import (
	transformFileStage1, 
	transformFileStage2, 
	transformFileStage3, 
	transformFileStage4, 
	transformFileStage5a,
	transformFileStage5b,
	transformFileStage6
)

# weather extract files/paths
extractPathStage1 = "..\\extract\\weather\\stage1"

# observations extract files/paths
observationExtractStage1File = "..\\extract\\observations\\stage1\\CAIC_avalanches_2008-10-01_2020-07-31.csv"

# transform stage files/paths
transformPathStage1 = "..\\transform\\stage1"
transformPathStage2 = "..\\transform\\stage2"
transformPathStage3 = "..\\transform\\stage3"
transformPathStage4 = "..\\transform\\stage4"
transformPathStage5 = "..\\transform\\stage5"
transformPathStage5a = "..\\transform\\stage5a"
transformPathStage5b = "..\\transform\\stage5b"
transformPathStage6 = "..\\transform\\stage6"

"""
Stage 1
Resolve missing values and group weather station values by mean
"""
extractFilesStage1 = [f for f in listdir(extractPathStage1) if isfile(join(extractPathStage1, f))]
for file in extractFilesStage1:
	print("file: " + file)
	transformFileStage1(file, extractPathStage1, transformPathStage1)

"""
Stage 2
Put all dates from stage1 into one CSV file
"""
transformFileStage2(transformPathStage1, transformPathStage2)


"""
Stage 3
Split into separate CSV files - this time by Zone and Elevation
"""
transformFileStage3(transformPathStage2, transformPathStage3)


"""
Stage 4
Calculate 'storm' and 'days_since_storm' metrics and append to each CSV
"""
transformFileStage4(transformPathStage3, transformPathStage4)


"""
Stage 5a
Resolve differences in Zone names for observation data
"""
transformFileStage5a(observationExtractStage1File, transformPathStage4, transformPathStage5a)


"""
Stage 5b
Using weather data, query observation data (similar to join except get count -- I'm not sure how to do this in Python)
"""
transformFileStage5b(transformPathStage5a, transformPathStage4, transformPathStage5b)


"""
Stage 6
Combine all data again into a single CSV file
"""
transformFileStage6(transformPathStage5b, transformPathStage6)