from flask import Flask, jsonify
from joblib import load

app = Flask(__name__)

birds = load('utils/birds_list.joblib')
seasons = load('utils/seasons_list.joblib')
states = load('utils/states.joblib')

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


if __name__ == "__main__":
    app.run(debug=True)