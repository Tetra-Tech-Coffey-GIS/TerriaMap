import pandas as pd
import pymssql
import geojson
from geojson import Feature, FeatureCollection, Point
from flask import jsonify
from apiflask import APIFlask
from flask_cors import CORS
import getpass
import os

app = APIFlask(__name__,json_errors=True)
CORS(app)

app.config.from_pyfile('settings.py')

def df_to_geojson(df, properties, lat='Latitude', lon='Longitude'):
    features = []
    for _, row in df.iterrows():
        my_feature = Feature(geometry=Point([row[lon],row[lat]]))
        output = {}
        for prop in properties:
            output.update({prop: row[prop]})
        my_feature['properties'] = output
        features.append(my_feature)
    feature_collection = FeatureCollection(features)
    return jsonify(feature_collection)

def get_db():
    mssql_db = pymssql.connect(
        server=app.config['ESDAT_SERVER'],
        user=app.config['ESDAT_USER'],
        password=app.config['ESDAT_PWD'],
        database=app.config['ESDAT_DATABASE'])
    return mssql_db

@app.get('/')
def index():
    domain = os.environ['userdomain']
    username = getpass.getuser()
    return {'message': getpass.getuser() + '\\' + os.environ['userdnsdomain'] }

@app.get("/esdatlocations")
def get_esdatlocations(): 
    locations_query = pd.read_sql_query('SELECT Location_Code, s.Site_Name, Latitude, Longitude FROM Locations l inner join Sites s on s.ID = l.SID' \
    ' WHERE Latitude IS NOT NULL',get_db())
    df = pd.DataFrame(locations_query)
    return df_to_geojson(df, ['Location_Code', 'Site_Name'])


@app.get("/esdatlocations/<int:site_id>")
def get_esdatlocationsBySite(site_id): 
    locations_query = pd.read_sql_query('SELECT Location_Code, s.Site_Name, Latitude, Longitude FROM Locations l inner join Sites s on s.ID = l.SID' \
    ' WHERE Latitude IS NOT NULL AND SID ={0}'.format(site_id),get_db())
    df = pd.DataFrame(locations_query)
    return df_to_geojson(df, ['Location_Code', 'Site_Name'])

