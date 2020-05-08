# sqlalchemy-challenge

Step 1 - Climate Analysis and Exploration
-
Do basic climate analysis with Python and SQLAlchemy in climate database provided (hawaii.sqlite). Connect to sqlite data base with 'create_engine'.
Use SQLAlchemy automap_base() to reflect your tables into classes and save a reference to those classes called Station and Measurement.

1. Precipitation Analysis
- Design a query to retrieve the last 12 months of precipitation data.
- Select only the date and prcp values.
- Load the query results into a Pandas DataFrame and set the index to the date column.
- Sort the DataFrame values by date.
- Plot the results.

2. Station Analysis
- Design a querries to calculate the total number of stations and most active stations.
- List the stations and observation counts in descending order. Which station has the highest number of observations?
- Design a query to retrieve the last 12 months of temperature observation data (TOBS). And filter by highest numbers of observations.
- Plot the results as a histogram.

Step 2 - Climate App
- 
Design a Flask API based on the queries that you have just developed. (flask to create routes)
Routes:
-/: Home page- List all routes that are available.
- /api/v1.0/precipitation: Convert the query results to a dictionary using date as the key and prcp as the value.
- /api/v1.0/stations: Return a JSON list of stations from the dataset.
- /api/v1.0/tobs: Query the dates and temperature observations of the most active station for the last year of data.Return a JSON list of temperature observations (TOBS) for the previous year.
- /api/v1.0/<start> and /api/v1.0/<start>/<end>: Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
  - When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
  - When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
