# Import dependencies
import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy as db
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Set access to query the database
engine = create_engine("sqlite:///hawaii.sqlite")

# Reflect the database into classes
Base = automap_base()

# Reflect the database
Base.prepare(engine, reflect=True)

# Create a variable for each of the classes to reference later
Measurement = Base.classes.measurement
Station = Base.classes.station


# Create a session link from Python to the database 
session = Session(engine)

# Create a Flask app
app = Flask(__name__)

# Define the welcome route 
@app.route("/")

# Create function to add routing info for ea. route
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')

# Query date + precipitation for prev year
@app.route("/api/v1.0/precipitation")    
def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
       filter(Measurement.date >= prev_year).all()
   return

# Query for all stations in db
@app.route("/api/v1.0/stations")

def stations():
    reults = session.query(Stations.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

# Create the temperature observations route --calculates the date one year ago 
# from the last date in the database;  primary station for all the temperature 
# observations from the previous year; unravel the results into a one-dimensional 
# array and convert that array into a list
@app.route("/api/v1.0/tobs")

def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

# Ccreate a route for summary statistics report w/both a starting and ending date parameters  
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).filter(Measurement.date <= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)
        