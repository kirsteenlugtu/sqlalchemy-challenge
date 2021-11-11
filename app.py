import numpy as np
import pandas as pd
import datetime as dt
from datetime import datetime

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

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station


# Flask setup
app = Flask(__name__)


# Flask routes
@app.route("/")
def home():
    return (
        f"Welcome to the weather stations of Hawaii! <br/>"
        f" <br/>"
        f"Available routes: <br/>"
        f"/api/v1.0/precipitation <br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    ) 

# Precipitaton
@app.route("/api/v1.0/precipitation")
def precip():
    session = Session(engine)
    prev_yr = dt.date(2017,8,23)-dt.timedelta(days=365)
    precipResults = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= prev_yr).all()
    session.close()

    # yrPrecip = []
    # for date, precip in precipResults:
    #     precip_dict = {}
    #     precip_dict["date"] = 

    precipResults = dict(precipResults)

    return jsonify(precipResults)

# List of stations
@app.route("/api/v1.0/stations")
def stations():
    # query stations
    session = Session(engine)
    weather_stations = session.query(Station.station).all()
    session.close()

    # convert to list 
    weather_stations = list(np.ravel(weather_stations))
    
    return jsonify(weather_stations=weather_stations)

# Temperature
@app.route("/api/v1.0/tobs")
def temps():
    session = Session(engine)
    station_counts = session.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station).all()
    station_counts = pd.DataFrame(station_counts, columns=['station ID','counts'])
    station_counts = station_counts.sort_values('counts', ascending=False)
    active_station = station_counts.loc[station_counts.counts == station_counts.counts.max(), 'station ID'].values[0]

    prev_yr = dt.date(2017,8,18)-dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.tobs).\
                filter(Measurement.date >= prev_yr).\
                filter(Measurement.station == active_station)

    session.close()

    Temp_observations = dict(results)

    return jsonify(Temp_observations)



if __name__ == "__main__":
    app.run(debug = True) 