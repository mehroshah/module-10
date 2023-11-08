import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
Measurement = Base.classes.measurement
Stations = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

##flask routes
@app.route("/")
def welcome():
    """List all avaialble api routes."""
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )
@app.route("/api/v1.0/precipitation")
def precipitation():

    #create session link from py to db
    session = Session(engine)

    """Return a list of all prec and date"""
    # Calculate the date one year from the last date in data set.
    results_date=session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    str_date=list(np.ravel(results_date))[0]
    latest_date=dt.datetime.strptime(str_date,"%Y-%m-%d")
    year_back=latest_date-dt.timedelta(days=366)

    # Perform a query to retrieve the data and precipitation scores
    results=session.query(Measurement.date,Measurement.prcp).order_by(Measurement.date.asc()).\
    filter(Measurement.date>=year_back).all()

    #query all stations
    #results = session.query(Measurement.date,Measurement.prcp).all()
    session.close()
    all_station=[]
    for date,precipitation in results:
        station_dict={}
        station_dict['date']=date
        station_dict['precipitation']=precipitation
       
        all_station.append(station_dict)
    return jsonify(all_station)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all passengers
    results = session.query(Stations.station).all()

    session.close()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))

    return jsonify(all_names)

@app.route("/api/v1.0/tobs")
def tempartureobs():
   
   #create link from py to db
    session = Session(engine)

    """Return a list of all temparture observation"""
    #calculate the date 1 year ago,from ast time
    results_date=session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    str_date=list(np.ravel(results_date))[0]
    latest_date=dt.datetime.strptime(str_date,"%Y-%m-%d")
    year_back=latest_date-dt.timedelta(days=366)
    #perform query to retrieve the data & precipitation
    results=session.query(Measurement.date,Measurement.tobs).order_by(Measurement.date.desc()).\
    filter(Measurement.date>=year_back).filter(Measurement.station=='USC00519281').all()
    session.close()
    all_temperature=[]
    for tobs,date in results:
        tobs_dict={}
        tobs_dict['date']=date
        tobs_dict['tobs']=tobs
        all_temperature.append(tobs_dict)
    return jsonify(all_temperature)
# This function called `calc_temps` will accept start date and end date in the format '%Y-%m-%d' 
# and return the minimum, average, and maximum temperatures for that range of dates
@app.route("/api/v1.0/<start>/<end>")
def calc_temps(start, end):
  # Create our session (link) from Python to the DB
    session = Session(engine)
    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
        """

    results=session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.close()
    temp_obs={}
    temp_obs["Min_Temp"]=results[0][0]
    temp_obs["avg_Temp"]=results[0][1]
    temp_obs["max_Temp"]=results[0][2]
    return jsonify(temp_obs)

@app.route("/api/v1.0/<start>")
def calc_temps_sd(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """
    
    results=session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).all()
    session.close()
    temp_obs={}
    temp_obs["Min_Temp"]=results[0][0]
    temp_obs["avg_Temp"]=results[0][1]
    temp_obs["max_Temp"]=results[0][2]
    return jsonify(temp_obs)
if __name__ == '__main__':
    app.run(debug=True)









    
   
   








