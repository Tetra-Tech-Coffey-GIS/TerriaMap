
import geojson
import json
import os
from geojson import Feature, Point, FeatureCollection
from bs4 import BeautifulSoup

html_property = '$(`<div'
pointsbefore = 'L.marker('
sydneygeojson = 'C://Dev//boreholemapV2//data//sydney.geojson'
sydneyjs = 'C://Dev//boreholemap//js//sydney.js'
brisbanegeojson = 'C://Dev//boreholemapV2//data//brisbane.geojson'
brisbanejs = 'C://Dev//boreholemap//js//brisbane.js'
melbournegeojson = 'C://Dev//boreholemapV2//data//melbourne.geojson'
melbournejs = 'C://Dev//boreholemap//js//melbourne.js'

if os.path.exists(sydneygeojson):
  os.remove(sydneygeojson)
if os.path.exists(brisbanegeojson):
  os.remove(brisbanegeojson)
if os.path.exists(melbournegeojson):
  os.remove(melbournegeojson)


def createGeoJSON(pointsbefore, filegeojson, filejs, gap):
    features = []

# Read the text back with UTF-8 encoding 
    with open(filejs, 'r', encoding = 'utf-8') as file: 
        lines = file.readlines()
        file.close()

    for k in range(len(lines)):
        if pointsbefore in lines[k]:
            points = lines[k+1]
            textarray = points.strip().rstrip('\r\n').rstrip(points[-2])
            data  = json.loads(textarray)
            my_feature = Feature(geometry=Point((data[1], data[0])))
            k=k+gap
            my_feature['properties'] = processProperties(lines[k])
            my_feature['id'] = len(my_feature)+1
            features.append(my_feature)

    feature_collection = FeatureCollection(features)
    dump = geojson.dumps(feature_collection, sort_keys=True)

    with open(filegeojson, 'x', encoding = 'utf-8') as file:
        file.write(dump)
        file.close()

def processProperties(htmlString):
    output = {}
    soup = BeautifulSoup(htmlString, 'html.parser')
    tables = soup.find_all('table', class_ = 'dataframe')
    if (len(tables) > 0):
        for header1 in tables[0].find_all('thead'):
            cells = header1.find_all('th')
            name = cells[1].contents[0]
            output.update({"NAME": name})
        for header1 in tables[0].find_all('tbody'):
            rows = header1.find_all('tr')
            for row in rows:
                prop = row.find_all('th')[0].text
                value = row.find_all('td')[0].text
                output.update({prop: value})
        if (len(tables) > 1):
            html = str(tables[1])
            output["Geology"]= html
    return output

createGeoJSON(pointsbefore, sydneygeojson, sydneyjs, 16)
createGeoJSON(pointsbefore, brisbanegeojson, brisbanejs, 24)
createGeoJSON(pointsbefore, melbournegeojson, melbournejs, 24)