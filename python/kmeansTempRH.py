"""
Author: David Sergio

KMeans Clustering
"""

import numpy as np
import pandas as pd
# import matplotlib as plt
import matplotlib.pyplot as plt
from numpy import nan

from sklearn.cluster import KMeans


weather_observation_data_file = "..\\transform\\stage6\\all_weather_obs_dates.csv"
weather_observation_data = pd.read_csv(weather_observation_data_file)

for col in weather_observation_data.columns: 
	weather_observation_data[col] = weather_observation_data[col].replace("", nan)
	weather_observation_data[col] = weather_observation_data[col].replace(" ", nan)
	weather_observation_data[col] = weather_observation_data[col].replace("NA", nan)
	weather_observation_data[col] = weather_observation_data[col].replace("?", nan)


query = "numberObservations > 0"
query_result = weather_observation_data.query(query)

col_list = ["Temp", "RH"]
query_result = query_result[col_list]

print(query_result)

kmeans = KMeans(n_clusters=3).fit(query_result)
centroids = kmeans.cluster_centers_
print(centroids)

plt.scatter(query_result['Temp'], query_result['RH'], c= kmeans.labels_.astype(float), s=50, alpha=0.5)
plt.scatter(centroids[:, 0], centroids[:, 1], c='red', s=50)
plt.xlabel("Temperature")
plt.ylabel("Relative Humidity")
plt.title("KMeans Temp / RH")
plt.savefig(".\\plots\\kmeansTempRH.png")