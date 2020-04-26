import pandas as pd
from boto.s3.key import Key
from boto.s3.connection import S3Connection
from flask import Flask, jsonify, request
from joblib import load

BUCKET_NAME = 'ebird-pickle-files'
LOCAL_PATH = '/tmp/'
ENCODER_FILE = 'cat_boost.joblib'
MODEL_FILE = 'rf.joblib'
BIRDS_FILE = 'birds_list.joblib'
SEASONS_FILE = 'seasons_list.joblib'
STATES_FILE = 'states.joblib'
COUNTIES_FILE = 'state_counties.joblib'
REGIONS_FILE = 'counties_to_regions.joblib'

app = Flask(__name__)

conn = S3Connection()
bucket = conn.create_bucket(BUCKET_NAME)
key_obj = Key(bucket)

encoder = load('utils/cat_boost.joblib')
model = load('utils/rf.joblib')

birds = load('utils/birds_list.joblib')
seasons = load('utils/seasons_list.joblib')
states = load('utils/state_counties.joblib')

state_counties = load('PATH_TO_FILE')
cs2r = load('PATH_TO_FILE')

labels = {0: "Common", 1:"Uncommon", 2:"Rare"}

@app.route('/api/birds', methods=['GET'])
def get_birds():
    key_obj.key = BIRDS_FILE
    contents = key_obj.get_contents_to_filename(LOCAL_PATH + BIRDS_FILE)
    birds = joblib.load(LOCAL_PATH + BIRDS_FILE)
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
    app.run(debug=True)