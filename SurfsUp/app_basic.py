# Import necessary modules
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from flask import Flask, jsonify
from sqlalchemy import create_engine, func

# Function to set up the database and return relevant classes and a session
def setup_database(db_path):
    # Create a SQLAlchemy engine for the specified database path
    engine = create_engine(f"sqlite:///{db_path}")
    
    # Create an automap base and reflect the tables from the database
    base = automap_base()
    base.prepare(engine, reflect=True)
    
    # Return the relevant classes and a session object
    return base.classes.measurement, base.classes.station, Session(engine)

# Function to convert date string to datetime object
def convert_to_datetime(date_string):
    return dt.datetime.strptime(date_string, "%Y-%m-%d")

# Function to query temperature data based on specified conditions
def query_temperature_data(query, *filter_conditions):
    return query.filter(*filter_conditions).join(station, measurement.station == station.station).all()

# Function to format temperature stats response
def get_temperature_stats_response(temperature_stats):
    return [
        {"Min Temperature": tmin, "Avg Temperature": tavg, "Max Temperature": tmax}
        for tmin, tavg, tmax in temperature_stats
    ]

# Set up the database and get classes and a session
measurement, station, session = setup_database("Resources/hawaii.sqlite")

# Create a Flask app
app = Flask(__name__)

# Define the home route
@app.route("/")
def home():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;"
    )

# Define the precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Query last year's precipitation data
    last_year_data = query_temperature_data(
        session.query(measurement.date, measurement.prcp),
        measurement.date >= get_last_year_date()
    )
    # Convert the result to a dictionary and return as JSON
    precipitation_dict = {date: prcp for date, prcp in last_year_data}
    return jsonify(precipitation_dict)

# Define the stations route
@app.route("/api/v1.0/stations")
def stations():
    # Query all stations and their names
    stations_data = session.query(station.station, station.name).all()
    # Convert the result to a list of dictionaries and return as JSON
    stations_list = [{"Station": station, "Name": name} for station, name in stations_data]
    return jsonify(stations_list)

# Define the tobs (temperature observations) route
@app.route("/api/v1.0/tobs")
def tobs():
    # Get the last year's date
    last_year_date = get_last_year_date()

    # Query the most active station for temperature data in the last year
    most_active_station = (
        session.query(measurement.station)
        .group_by(measurement.station)
        .order_by(func.count().desc())
        .first()[0]
    )

    # Query temperature data for the most active station in the last year
    temperature_data = query_temperature_data(
        session.query(measurement.date, measurement.tobs),
        measurement.station == most_active_station,
        measurement.date >= last_year_date
    )

    # Convert the result to a list of dictionaries and return as JSON
    temperature_list = [{"Date": date, "Temperature": tobs} for date, tobs in temperature_data]
    return jsonify(temperature_list)

# Define the temperature stats route with optional start and end parameters
@app.route("/api/v1.0/<start>/<end>")
@app.route("/api/v1.0/<start>")
def temperature_stats(start, end=None):
    # Convert start and end dates to datetime objects
    start_date = convert_to_datetime(start)
    end_date = convert_to_datetime(end) if end else None

    # Query temperature statistics (min, avg, max) for the specified date range
    query = (
        session.query(
            func.min(measurement.tobs),
            func.avg(measurement.tobs),
            func.max(measurement.tobs),
        )
        .join(station, measurement.station == station.station)
    )

    # Apply date filters to the query
    query = filter_dates(query, start_date, end_date)

    # Execute the query and format the result for JSON response
    temperature_stats = query.all()
    return jsonify(get_temperature_stats_response(temperature_stats))

# Helper function to filter dates in a query
def filter_dates(query, start_date, end_date):
    query = query.filter(measurement.date >= start_date)
    if end_date:
        query = query.filter(measurement.date <= end_date)
    return query

# Helper function to get the last year's date
def get_last_year_date():
    last_date = session.query(func.max(measurement.date)).scalar()
    return convert_to_datetime(last_date) - dt.timedelta(days=365)

# Run the Flask app if the script is executed
if __name__ == "__main__":
    app.run(debug=True)
