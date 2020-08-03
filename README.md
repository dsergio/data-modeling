# data-modeling

This project is ongoing. The purpose is to use ETL techniques with open-source weather and avalanche datasets from the Colorado Avalanche Information Center (CAIC), and produce a data model that attempts to demonstrate relationships between avalanche characteristics, occurrences, and/or frequency and weather metrics, such as temperature and wind speed. I'm using some weather metrics out-of-the-box such as temperature and relative humidity, and I'm working on developing derived metrics, such as "days since storm event". It should be noted that snow science is tricky and nuanced, and it's not feasible (or prudent) to attempt to predict avalanches accurately. However, the amount of data makes such a project a lot of fun and really interesting from a data science perspective. I also hope to use these datasets to do data characterization analyses and cluster analysis. For exampole, it's interesting to demonstrate how avalanche occurrences tend to cluster on specific aspects (N/S/E/W). 

## Data Modeling Project: ETL

### Extract

See Java data collection app <a href = "https://github.com/dsergio/data-modeling/tree/master/datamodeling">here</a>

### Transform

See Python scripts <a href = "https://github.com/dsergio/data-modeling/tree/master/python">here</a>

### Load

The transformed data is <a href = "https://github.com/dsergio/data-modeling/tree/master/transform/stage6">here</a>

The data can then be imported into RapidMiner or R/Python for
* decision tree analysis
* correlation matrix
* other data analysis  

### Analysis

TBD