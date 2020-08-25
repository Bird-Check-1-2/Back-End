import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
load_dotenv()

db_url = os.getenv("DATABASE_URL")
pg_user = os.getenv("DATABASE_USER")
pg_pass = os.getenv("DATABASE_PW")
db_name = os.getenv("DATABASE_NAME")


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql+psycopg2://{pg_user}:{pg_pass}@{db_url}/{db_name}"
db = SQLAlchemy(app)

from models import Bird, County, State, Region, Season, Lookup

@app.route('/api/birds', methods=['GET'])
def get_birds():
    birds = Bird.query.all()
    response = {
        "birds": [bird.name for bird in birds]
    }
    return jsonify(response)


@app.route('/api/seasons', methods=['GET'])
def get_seasons():
    seasons = Season.query.all()
    response = {
        "seasons": [season.name for season in seasons]
    }
    return jsonify(response)


@app.route('/api/states', methods=['GET'])
def get_states():
    states = State.query.all()
    response = {
        "states": [state.name for state in states]
    }
    return jsonify(response)


@app.route('/api/counties', methods=['POST'])
def get_county_from_state():
    data = request.get_json()
    state = data['state']
    state_id = State.query.filter_by(name=state).first()
    counties = County.query.filter_by(state_id=state_id).all()
    response = {
        'counties': [county.county_name for county in counties]
    }
    return jsonify(response)


def lookup_result(bird, season, region):
    # get pct of total from lookup table
    lookup = Lookup.query.filter_by(region=region, season=season, bird=bird).first()

    # if elif to decide string output
    if lookup.pct_of_total > 0.005:
        return "Common"
    elif lookup.pct_of_total > 0.001:
        return "Uncommon"
    else:
        return "Rare"


@app.route('/api/results', methods=['POST'])
def predict_bird():
    data = request.get_json()

    bird = data['bird']
    season = data['season']
    
    state = State.query.filter_by(name=data['state']).first()
    county = County.query.filter_by(county_name=data['county'], state_id=state).first()
    region = Region.query.filter_by(county_id=county).first()

    result = lookup_result(bird, season, region)

    response = {
        'result': result
    }
    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True)