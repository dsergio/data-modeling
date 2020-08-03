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

weather_observation_data["aspectMode"].fillna(0, inplace=True)
weather_observation_data["aspectMode"].replace("U", 0, inplace=True)
weather_observation_data["aspectMode"].replace("N", 0, inplace=True)
weather_observation_data["aspectMode"].replace("NE", 45, inplace=True)
weather_observation_data["aspectMode"].replace("E", 90, inplace=True)
weather_observation_data["aspectMode"].replace("SE", 135, inplace=True)
weather_observation_data["aspectMode"].replace("S", 180, inplace=True)
weather_observation_data["aspectMode"].replace("SW", 225, inplace=True)
weather_observation_data["aspectMode"].replace("W", 270, inplace=True)
weather_observation_data["aspectMode"].replace("NW", 315, inplace=True)


print("weather_observation_data missing data:")
print(weather_observation_data.isnull().sum())
print("\n\n")

query = "numberObservations > 0"
query_result = weather_observation_data.query(query)

col_list = ["aspectMode", "Temp"]
query_result = query_result[col_list]

print(query_result)

kmeans = KMeans(n_clusters=3).fit(query_result)
centroids = kmeans.cluster_centers_
print(centroids)

plt.scatter(query_result['aspectMode'], query_result['Temp'], c= kmeans.labels_.astype(float), s=50, alpha=0.5)
plt.scatter(centroids[:, 0], centroids[:, 1], c='red', s=50)
plt.xlabel("Aspect Mode")
plt.ylabel("Temp")
plt.title("KMeans Aspect Mode / Temp")
plt.savefig(".\\plots\\kmeansAspectModeTemp.png")