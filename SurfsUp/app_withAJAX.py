# Import necessary libraries
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from flask import Flask, jsonify, render_template
from sqlalchemy import create_engine, func

# Set up the database connection
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect the database schema using automap_base()
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save references to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a session link from Python to the database
session = Session(engine)

# Create a Flask app
app = Flask(__name__)

# Display available routes on the landing page
@app.route("/")
def welcome():
    """Display the welcome page."""
    return render_template("welcome.html")

# Precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return JSON with date as the key and precipitation as the value for the last year."""
    # Calculate the date one year ago from the last data point in the database
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    # Query precipitation data for the last year, including the corresponding station information
    precipitation_data = (
        session.query(Measurement.date, Measurement.prcp)
        .filter(Measurement.date >= last_year)
        .join(Station, Measurement.station == Station.station)  # Join the station table
        .all()
    )

    # Convert the result to a dictionary and return as JSON
    precipitation_dict = {date: prcp for date, prcp in precipitation_data}
    return jsonify(precipitation_dict)

# Stations route
@app.route("/api/v1.0/stations")
def stations():
    """Return JSONified data of all stations in the database."""
    # Query all stations and their names
    stations_data = session.query(Station.station, Station.name).all()
    
    # Convert the result to a list of dictionaries and return as JSON
    stations_list = [{"Station": station, "Name": name} for station, name in stations_data]
    return jsonify(stations_list)

# Tobs route
@app.route("/api/v1.0/tobs")
def tobs():
    """Return JSONified data for the most active station (USC00519281) for the last year."""
    # Calculate the date one year ago from the last data point in the database
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    # Query temperature data for the most active station in the last year, including station information
    most_active_station = (
        session.query(Measurement.station)
        .group_by(Measurement.station)
        .order_by(func.count().desc())
        .first()[0]
    )

    temperature_data = (
        session.query(Measurement.date, Measurement.tobs)
        .filter(Measurement.station == most_active_station, Measurement.date >= last_year)
        .join(Station, Measurement.station == Station.station)  # Join the station table
        .all()
    )

    # Convert the result to a list of dictionaries and return as JSON
    temperature_list = [{"Date": date, "Temperature": tobs} for date, tobs in temperature_data]
    return jsonify(temperature_list)

# Start route
@app.route("/api/v1.0/<start>")
def start_date_stats(start):
    """Return JSON with min, max, and average temperatures from the given start date to the end of the dataset."""
    # Convert the start date string to a datetime object
    start_date = dt.datetime.strptime(start, "%Y-%m-%d")

    # Query temperature statistics for the specified start date to the end of the dataset, including station information
    temperature_stats = (
        session.query(
            func.min(Measurement.tobs),
            func.avg(Measurement.tobs),
            func.max(Measurement.tobs),
        )
        .filter(Measurement.date >= start_date)
        .join(Station, Measurement.station == Station.station)  # Join the station table
        .all()
    )

    # Convert the result to a list of dictionaries and return as JSON
    stat_list = [
        {"Min Temperature": tmin, "Avg Temperature": tavg, "Max Temperature": tmax}
        for tmin, tavg, tmax in temperature_stats
    ]
    return jsonify(stat_list)

# Start/end route
@app.route("/api/v1.0/<start>/<end>")
def start_end_date_stats(start, end):
    """Return JSON with min, max, and average temperatures from the given start date to the given end date."""
    # Convert the start and end date strings to datetime objects
    start_date = dt.datetime.strptime(start, "%Y-%m-%d")
    end_date = dt.datetime.strptime(end, "%Y-%m-%d")

    # Query temperature statistics for the specified date range, including station information
    temperature_stats = (
        session.query(
            func.min(Measurement.tobs),
            func.avg(Measurement.tobs),
            func.max(Measurement.tobs),
        )
        .filter(Measurement.date.between(start_date, end_date))
        .join(Station, Measurement.station == Station.station)  # Join the station table
        .all()
    )

    # Convert the result to a list of dictionaries and return as JSON
    stats_list = [
        {"Min Temperature": tmin, "Avg Temperature": tavg, "Max Temperature": tmax}
        for tmin, tavg, tmax in temperature_stats
    ]
    return jsonify(stats_list)

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
