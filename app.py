import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
# How to run Flask
#################################################
# export FLASK_APP=app.py
# flask run
#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available API routes"""
    # text = (”Available Routes: < br/>”+
    #     ”/ api/v1.0/precipitation < br/>”+
    #     ”/ api/v1.0/stations < br/>”+
    #     ”/ api/v1.0/tobs < br/>”+
    #     ”/ api/v1.0/<start > <br/>”+
    #     ”/ api/v1.0/<start_date > / < end_date > /“)
    text="asdf"
    return (text)


# Convert the query results to a dictionary using `date` as the key and `prcp` as th
@app.route("/api/v1.0/precipitation")
def names():
    # Calculate date one year ago
    last_year_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    result = session.query(Measurement.date, Measurement.prcp).filter(
        Measurement.date >= last_year_date).order_by(Measurement.date).all()

    # Create the dictionary
    precipitation_data = []
    for date, prcp in result:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        precipitation_data.append(precipitation_dict)

    return jsonify(precipitation_data)

#  Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    stations_list = session.query(
        Station.station, Station.name, Station.latitude, Station.elevation).all()
    return jsonify(stations_list)

# #Query the dates and temperature observations of the most active station for the last year of data.
@app.route("/api/v1.0/tobs")
def tobs():
    temp_observation_data = session.query(Measurement.tobs).filter(
        Measurement.date >= '2016--08-23').filter(Measurement.station == 'USC00519281').all()

    tobs_list = []
    for date, tobs in temp_observation_data:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        tobs_list.append(tobs_dict)
    return jsonify(tobs_list)

# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
@app.route("/api.v1.0/<start>")
def end(start, end):
    tobs = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(and_(Measurement.date >= '2013-01-01', Measurement.date <= '2013-01-10')).\
        group_by(Measurement.date).all()
    
    tob_dict = []
    for date, min, max, avg in tobs:
        tobs_close={}
        tobs_close["min"]=min
        tobs_close["max"]=max
        tobs_close["avg"]=avg
        tobs_close["date"]=date
        tob_dict.append(tobs_close)
    return jsonify(tob_dict)


if __name__ == '__main__':
    app.run(debug=True)
