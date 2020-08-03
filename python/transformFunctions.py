

import numpy as np
import pandas as pd
# import matplotlib as plt
import matplotlib.pyplot as plt
from numpy import nan

from os import listdir
from os.path import isfile, join

"""
Stage 1
Resolve missing values and group weather station values by mean
"""
def transformFileStage1(extractFile, extractPath, transformPath):

	fileName = extractPath + "\\" + extractFile
	fileNameOutput = transformPath + "\\" + extractFile
	weather_date_data = pd.read_csv(fileName)

	del weather_date_data['Station']
	del weather_date_data['Provider']

	for col in weather_date_data.columns: 
		weather_date_data[col] = weather_date_data[col].replace("", nan)
		weather_date_data[col] = weather_date_data[col].replace(" ", nan)
		weather_date_data[col] = weather_date_data[col].replace("NA", nan)
		weather_date_data[col] = weather_date_data[col].replace("?", nan)

	# print("weather_date_data missing data:")
	# print(weather_date_data.isnull().sum())
	# print("\n\n")

	# print(weather_date_data.head(10))
	# print("\n\n")

	weather_date_data.fillna(method='backfill', inplace=True)

	print(weather_date_data.head(10))
	print("\n\n")

	weather_date_data['Temp'] = pd.to_numeric(weather_date_data['Temp'])
	weather_date_data['MxTp'] = pd.to_numeric(weather_date_data['MxTp'])
	weather_date_data['MnTp'] = pd.to_numeric(weather_date_data['MnTp'])
	weather_date_data['DewP'] = pd.to_numeric(weather_date_data['DewP'])
	weather_date_data['RH'] = pd.to_numeric(weather_date_data['RH'])
	weather_date_data['Spd'] = pd.to_numeric(weather_date_data['Spd'])
	weather_date_data['Dir'] = pd.to_numeric(weather_date_data['Dir'])
	weather_date_data['Gst'] = pd.to_numeric(weather_date_data['Gst'])
	weather_date_data['Pcp1'] = pd.to_numeric(weather_date_data['Pcp1'])
	weather_date_data['Pcp24'] = pd.to_numeric(weather_date_data['Pcp24'])
	weather_date_data['PcpAc'] = pd.to_numeric(weather_date_data['PcpAc'])
	weather_date_data['Sno24'] = pd.to_numeric(weather_date_data['Sno24'])
	weather_date_data['SWE24'] = pd.to_numeric(weather_date_data['SWE24'])
	weather_date_data['SnoHt'] = pd.to_numeric(weather_date_data['SnoHt'])
	weather_date_data['SWE'] = pd.to_numeric(weather_date_data['SWE'])

	weather_date_zone = pd.DataFrame(data=None, columns=weather_date_data.columns)

	# print(weather_date_zone)
	# print("\n\n")

	grouped_data = weather_date_data.groupby(['BC Zone', 'ElevTL'])

	for name, group in grouped_data:
	   print(name)
	   # print(group)
	   # print(group.dtypes)
	   agg = group.agg(np.mean)
	   agg['CAIC_Weather_Date'] = group.iloc[0]['CAIC_Weather_Date']
	   agg['BC Zone'] = group.iloc[0]['BC Zone']
	   agg['ElevTL'] = group.iloc[0]['ElevTL']
	   weather_date_zone = weather_date_zone.append(agg, ignore_index=True)
	print("\n\n")

	# print(weather_date_zone)
	# print("\n\n")

	weather_date_zone.to_csv(fileNameOutput)


"""
Stage 2
Put all dates from stage1 into one CSV file
"""
def transformFileStage2(transformPathStage1, transformPathStage2):

	transformFilesStage1 = [f for f in listdir(transformPathStage1) if isfile(join(transformPathStage1, f))]

	i = 0;
	for file in transformFilesStage1:
		
		fileName = transformPathStage1 + "\\" + file
		print("fileName: " + fileName)

		if i == 0:
			weather_date_data = pd.read_csv(fileName)
			outputDataFrame = weather_date_data.copy()
			i = 1
		else:
			weather_date_data = pd.read_csv(fileName)
			outputDataFrame = outputDataFrame.append(weather_date_data)


	outputDataFrame = outputDataFrame.drop(outputDataFrame.columns[[0]], axis=1)
	fileNameOutput = transformPathStage2 + "\\all_dates.csv"
	outputDataFrame.to_csv(fileNameOutput)


"""
Stage 3
Separate - this time by Zone and Elevation
"""
def transformFileStage3(transformPathStage2, transformPathStage3):

	alldates_data = pd.read_csv(transformPathStage2 + "\\all_dates.csv")

	grouped_data = alldates_data.groupby(['BC Zone', 'ElevTL'])

	for name, group in grouped_data:
	   print(name)
	   print(group)
	   # print(group.dtypes)

	   zone = group.iloc[0]['BC Zone']
	   elev = group.iloc[0]['ElevTL']
	   elev = elev.replace(">", "greaterthan")
	   elev = elev.replace("<", "lessthan")
	   zone = zone.replace("/", "-")
	   group.to_csv(transformPathStage3 + "\\" + zone + "_" + elev + ".csv")


"""
Stage 4
Calculate 'storm' and 'days_since_storm' metrics and append to each CSV
"""
def transformFileStage4(transformPathStage3, transformPathStage4):

	transformFilesStage3 = [f for f in listdir(transformPathStage3) if isfile(join(transformPathStage3, f))]

	for fileName in transformFilesStage3:
		zone_elev_data = pd.read_csv(transformPathStage3 + "\\" + fileName)

		meanPcp24 = zone_elev_data['Pcp24'].mean()
		stdPcp24 = zone_elev_data['Pcp24'].std()

		storm_rows = []
		for index, row in zone_elev_data.iterrows():
			# print("date: " + row['CAIC_Weather_Date'] + " zone: " + row['BC Zone'] + " Sno24: " + str(row['Sno24']) + " row['Sno24'] > 0.5: " + str(row['Sno24'] > 0.5))
			
			if (row['Sno24'] > 0.99): # heuristic 'storm' threshold -- TODO find a better way to do this
				storm_rows.append("yes")
			else:
				storm_rows.append("no")

		days_since_storm = []
		days = 10;
		for i in storm_rows:
			if (i == "yes"):
				days = 0;
			else:
				days = days + 1
			days_since_storm.append(days)
		zone_elev_data['storm'] = storm_rows
		zone_elev_data['days_since_storm'] = days_since_storm

		zone = zone_elev_data.iloc[0]['BC Zone']
		elev = zone_elev_data.iloc[0]['ElevTL']
		elev = elev.replace(">", "greaterthan")
		elev = elev.replace("<", "lessthan")
		zone = zone.replace("/", "-")
		zone_elev_data.to_csv(transformPathStage4 + "\\" + zone + "_" + elev + ".csv")

"""
Stage 5a
Resolve differences in Zone names for observation data
"""
def transformFileStage5a(observationExtractStage1, transformPathStage4, transformPathStage5a):
	observation_data = pd.read_csv(observationExtractStage1)

	transformFilesStage4 = [f for f in listdir(transformPathStage4) if isfile(join(transformPathStage4, f))]

	weather_zones = []
	for fileName in transformFilesStage4:
		zone_elev_data = pd.read_csv(transformPathStage4 + "\\" + fileName)
		zone_name = zone_elev_data.iloc[0]['BC Zone']
		weather_zones.append(zone_name)

	# print("observation zones")
	# print(pd.unique(observation_zones))

	# print("weather zones")
	# print(pd.unique(weather_zones))


	observation_data = observation_data.replace("Northern San Juan", "North San Juan")
	observation_data = observation_data.replace("Sangre de Cristo", "Sangre")
	observation_data = observation_data.replace("Sawatch Range", "Sawatch")
	observation_data = observation_data.replace("Southern San Juan", "South San Juan")
	observation_data = observation_data.replace("Steamboat & Flat Tops", "Steamboat")
	observation_data = observation_data.replace("Vail & Summit County", "Vail/Summit")

	observation_zones = observation_data['BC Zone']
	for i in pd.unique(weather_zones):
		if (i not in pd.unique(observation_zones)):
			print("update observation zone " + i)

	observation_data.to_csv(transformPathStage5a + "\\observation_data.csv")

"""
Stage 5b
Using weather data, query observation data (similar to join except get count -- I'm not sure how to do this in Python)
"""
def transformFileStage5b(transformPathStage5a, transformPathStage4, transformPathStage5b):

	observation_data = pd.read_csv(transformPathStage5a + "\\observation_data.csv")

	transformFilesStage4 = [f for f in listdir(transformPathStage4) if isfile(join(transformPathStage4, f))]

	for fileName in transformFilesStage4:
		zone_elev_data = pd.read_csv(transformPathStage4 + "\\" + fileName)

		
		zone = zone_elev_data.iloc[0]['BC Zone']
		elev = zone_elev_data.iloc[0]['ElevTL']

		number_of_observations = []
		most_frequent_aspect_arr = []
		for index, row in zone_elev_data.iterrows():
			date = row['CAIC_Weather_Date']
			query = "`BC Zone` == '" + zone + "' and " + "ElevTL == '" + elev + "' and " + "CAIC_Weather_Date == '" + date + "'"
			

			query_result = observation_data.query(query)
			if (query_result["Asp"].mode().size > 0):
				most_frequent_aspect = query_result["Asp"].mode()[0]
			else:
				most_frequent_aspect = ''
			most_frequent_aspect_arr.append(most_frequent_aspect)
			number_of_observations.append(query_result.shape[0])
			# print("query: " + query + " numberObservations: " + str(query_result.shape[0]))
			# print(query_result)

		zone_elev_data['numberObservations'] = number_of_observations
		zone_elev_data['aspectMode'] = most_frequent_aspect_arr
		zone_elev_data.to_csv(transformPathStage5b + "\\" + fileName)

		# merged_data = pd.merge(zone_elev_data, observation_data, how='left', on=["CAIC_Weather_Date", "BC Zone", "ElevTL"])
		# merged_grouped_data = merged_data.groupby('CAIC_Weather_Date')
		# for name, group in merged_grouped_data:
		# 	print(name)
		# 	print(group)

		# merged_data.to_csv(transformPathStage5 + "\\" + fileName)


"""
Stage 6
Combine all data again into a single CSV file
"""
def transformFileStage6(transformPathStage5b, transformPathStage6):

	transformFilesStage5b = [f for f in listdir(transformPathStage5b) if isfile(join(transformPathStage5b, f))]

	i = 0;
	for fileName in transformFilesStage5b:
		

		if i == 0:
			zone_elev_weather_obs_data = pd.read_csv(transformPathStage5b + "\\" + fileName)
			outputDataFrame = zone_elev_weather_obs_data.copy()
			i = 1
		else:
			zone_elev_weather_obs_data = pd.read_csv(transformPathStage5b + "\\" + fileName)
			outputDataFrame = outputDataFrame.append(zone_elev_weather_obs_data)


	outputDataFrame = outputDataFrame.drop(outputDataFrame.columns[[0, 1, 2, 3]], axis=1)
	fileNameOutput = transformPathStage6 + "\\all_weather_obs_dates.csv"
	outputDataFrame.to_csv(fileNameOutput)
