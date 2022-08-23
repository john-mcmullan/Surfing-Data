# Import 
import numpy as np
import datetime as dt
# Import Alchemy
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
# Import Flask
from flask import Flask, jsonify

# Set up engine
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

# Create Flask
app = Flask(__name__)

# Set Bases
station = Base.classes.station
measurement = Base.classes.measurement

# Home Page
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start> PRINT DATE: YYYY-MM-DD<br/>"
        f"/api/v1.0/<start/<end> PRINT START DATE YYYY-MM-DD/PRINT END DATE: YYYY-MM-DD"     
    )

#Precipitation app
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    fullyear = session.query(measurement.prcp, measurement.date).group_by(measurement.date).all()
    
    #Hold info
    pr = []

    # grap information in dictionary
    for prcp, date in fullyear:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        pr.append(prcp_dict)
    
    #Jsonify results
    return jsonify(pr)


#Station App
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    st = session.query(station.station).all()
    
    #list all stations in query
    allstation = list(np.ravel(st))

    #jsonify results
    return jsonify(allstation)


#Temperature app
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    Maxdate = session.query(func.max(measurement.date)).scalar()
    yearago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    temp = session.query(measurement.station, measurement.date, measurement.tobs)\
    .filter(measurement.station == "USC00519281")\
    .filter(measurement.date <= Maxdate)\
    .filter(measurement.date >= yearago).all()

    tp = []

    for station, date, tobs in temp:
        temp_dict = {}
        temp_dict["station"] = station 
        temp_dict["date"] = date
        temp_dict["tobs"] = tobs
        tp.append(temp_dict)
    
    #jsonify results
    return jsonify(tp)


#Start Date app
@app.route("/api/v1.0/<start>")
def start_date(start):
    session = Session(engine)
    
    temp = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs))\
    .filter(measurement.date >= start).all()
    
    
    alltemp=[]

    for min, max, avg in temp:
        tempdict = {}
        tempdict["Min"] = min
        tempdict["Max"] = max
        tempdict["Avg"] = avg
        alltemp.append(tempdict)

    return jsonify(alltemp)

#Start-End Date
@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    session = Session(engine)
    
    temperature = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs))\
    .filter(measurement.date >= start).filter(measurement.date <= end).all()
    
    
    temptime=[]
    for min, max, avg in temperature:
        temperaturedict = {}
        temperaturedict["Min"] = min
        temperaturedict["Max"] = max
        temperaturedict["Avg"] = avg
        temptime.append(temperaturedict)

    return jsonify(temptime)

if __name__ == '__main__':
    app.run(debug=True)