from flask import Flask, url_for, request, render_template, jsonify, Markup, g

app = Flask(__name__)

@app.route('/', methods=['GET'])
def get_apps():
    markers = [
            {'name':'LBL', 'lat':37.877344, 'lng':-122.250694, 'details':"our future office with view"}, 
            {'name':'LBL Potter', 'lat':37.8488548, 'lng':-122.2956218, 'details':"We make awesome stuff."}
        ]
    # starting the map in the center of all of markers
    # it can't be done in the front end, but I think these things should be handled in back end. 
    lat_tot = 0
    lng_tot = 0
    for i in markers:
        lat_tot = lat_tot + i['lat']
        lng_tot = lng_tot + i['lng']

    center = {'lat': lat_tot/len(markers), 'lng': lng_tot/len(markers)}
    return render_template('map.html',  markers=markers, center=center)