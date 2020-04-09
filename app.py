import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

session=Session(engine)

# Save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station

app = Flask(__name__)

#Start defining app routes
@app.route("/")
def welcome():
    
    """List all available api routes."""
    print('Welcome to your trip planner')
    return (
        f"Welcome to your trip planner!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/yyyy-mm-dd;<br/>"
        f"returns TMIN, TAVG, TMAX for all dates starting with 'yyyy-mm-dd' </br>"
        f"/api/v1.0/yyyy-mm-dd/yyyy-mm-dd;<br/>"
        f"returns TMIN, TAVG, TMAX for all dates in range 'yyyy-mm-dd' to 'yyyy-mm-dd' </br>"
    )

@app.route('/api/v1.0/precipitation')
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
   
    rainfall = session.query(measurement.date, measurement.prcp).all()
    session.close()
    
    all_rainfall = []
    for date, prcp in rainfall:
        rainfall_dict = {}
        rainfall_dict["date"] = date
        rainfall_dict["prcp"] = prcp
        
        all_rainfall.append(rainfall_dict)

    
    return jsonify(all_rainfall)

@app.route('/api/v1.0/stations')
def stations():
    """Return a JSON list of stations from the dataset"""
    session = Session(engine)
    stations = session.query(station.name).all()

    session.close()

    """Convert list of tuples into normal list"""
    all_stations = list(np.ravel(stations))

    return jsonify(all_stations)

@app.route('/api/v1.0/tobs')
def tobs():
    """Return a list of tobs for the previous year"""
    session = Session(engine)
    """Query the dates and temperature observations of the most active station for the last year of data."""
    
    active_station = session.query(station.name, measurement.date, measurement.tobs).\
        filter(measurement.date >= "2016-08-24", measurement.date <= "2017-08-23").\
        all()
    session.close()
    
    # creates JSONified list of dictionaries
    """Return a JSON list of temperature observations (TOBS) for the previous year."""
    tobs_list = []
    for observation in active_station:
        row = {}
        row["station"] = observation[0]
        row["date"] = observation[1]
        row["temperature"] = int(observation[2])
        tobs_list.append(row)

    return jsonify(tobs_list)
@app.route('/api/v1.0/<date>')
def start(date):
    session=Session(engine)
    """When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date."""
    start_date = session.query(measurement.date, func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= date).\
        all()
    session.close()
    
    # creates JSONified list of dictionaries
    date_list = []
    for day in start_date:
        row = {}
        row['Date'] = day[0]
        row['TMIN'] = float(day[1])
        row['TAVG'] = float(day[2])
        row['TMAX'] = float(day[3])
        date_list.append(row)

    return jsonify(date_list)

# @app.route('/api/v1.0/<start>/<end>')
def range_dates(start_date, end_date):
    """Return the avg, max, min, temp over a specific time period"""
    date_range = session.query(measurement.date, func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start_date, measurement.date <= end_date).all()

    # creates JSONified list of dictionaries
    data_list = []
    for result in date_range:
        row = {}
        row['Date'] = result[0]
        row['TMIN'] = float(result[1])
        row['TAVG'] = float(result[2])
        row['TMAX'] = float(result[3])
        data_list.append(row)
    return jsonify(data_list)
# def end():

if __name__ == '__main__':
    app.run(debug=True)
