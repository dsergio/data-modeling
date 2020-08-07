# data-modeling

This project uses ETL to generate datasets from open-source weather and avalanche observation data sources from the Colorado Avalanche Information Center (CAIC)

One goal is to produce a data model that attempts to demonstrate relationships between avalanche characteristics, occurrences, and/or frequency and weather metrics, such as temperature and wind speed. I'm using some weather metrics out-of-the-box such as temperature and relative humidity, and I'm developing derived metrics, such as "days since storm event". It's worth noting that snow science is tricky and nuanced. However, the amount of data makes such a project a lot of fun and really interesting from a data science perspective. 

These datasets can also enable data characterization analyses and cluster analysis. For example, it's interesting to demonstrate how avalanche occurrences tend to cluster on specific aspects (N/S/E/W), and weather conditions. 

## Data Modeling Project: ETL

### Extract

See Java data collection app <a href = "https://github.com/dsergio/data-modeling/tree/master/datamodeling">here</a>

### Transform

See Python scripts <a href = "https://github.com/dsergio/data-modeling/tree/master/python">here</a>

### Load

The transformed data is <a href = "https://github.com/dsergio/data-modeling/tree/master/transform/stage6">here</a>

The data can then be imported into RapidMiner or R or Python for data modeling and analysis, such as
* Decision Tree
* Correlation matrix
* KMeans Clustering  

### Analysis

Observation Distribution Analysis (See also <a href = "https://github.com/dsergio/data-modeling/tree/master/python/plots">here</a>)

![](https://github.com/dsergio/data-modeling/blob/master/python/plots/aspect.png?raw=true)

![](https://github.com/dsergio/data-modeling/blob/master/python/plots/aspect_elev.png?raw=true)

<i>TL: Treeline, >TL: Elevation higher than Treeline, <TL: Elevation lower than Treeline</i>

### KMeans clusters with weather variables and 1 or more observations

![](https://github.com/dsergio/data-modeling/blob/master/python/plots/kmeansTempRH.png?raw=true)

![](https://github.com/dsergio/data-modeling/blob/master/python/plots/kmeansWindspeedDir.png?raw=true)

### Dashboard

The "Days Since Storm" metric shows a modest correlation with number of Observations, only for <TL (less than Treeline) elevation in this limited dataset

![](https://github.com/dsergio/data-modeling/blob/master/CAICDashboard.png?raw=true)