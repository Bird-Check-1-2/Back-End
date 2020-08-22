import pandas as pd

from flask import Flask, jsonify, request
from joblib import load

app = Flask(__name__)

birds = load('utils/birds_list.p')
seasons = load('utils/seasons_list.p')
states = load('utils/states.p')

state_counties = load('utils/state_counties.p')
cs2r = load('utils/counties_to_regions.joblib')

labels = {0: "Common", 1:"Uncommon", 2:"Rare"}

@app.route('/api/birds', methods=['GET'])
def get_birds():
    response = {
        "birds": sorted(birds)
    }
    return jsonify(response)


@app.route('/api/seasons', methods=['GET'])
def get_seasons():
    response = {
        "seasons": sorted(seasons)
    }
    return jsonify(response)


@app.route('/api/states', methods=['GET'])
def get_states():
    response = {
        "states": sorted(states)
    }
    return jsonify(response)


@app.route('/api/counties', methods=['POST'])
def get_county_from_state():
    data = request.get_json()
    state = data['state']
    counties = state_counties[state]
    response = {
        'counties': sorted(counties)
    }
    return jsonify(response)


@app.route('/api/results', methods=['POST'])
def predict_bird():
    data = request.get_json()

    # needed_keys = ['bird', 'season', 'state', 'county']
    # if not all(needed_keys) in data.keys():
    #     message = "Invalid keys. Need 'bird', 'season', 'state', and 'county'"
    #     return message, 400
    
    bird = data['bird']
    season = data['season']

    county_state = data['county'] + ',' + data['state']
    region = cs2r[county_state]

    # encode features
    X = pd.DataFrame({
        'name': [bird],
        'season': [season],
        'region': [region]
    })
    X_encoded = encoder.transform(X)
    # get prediction
    pred = model.predict(X_encoded)
    label = labels[pred[0]]

    response = {
        'prediction': label
    }
    return jsonify(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0")