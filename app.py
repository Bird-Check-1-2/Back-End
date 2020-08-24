import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
load_dotenv()

db_url = os.getenv("DATABASE_URL")
pg_user = os.getenv("DATABASE_USER")
pg_pass = os.getnev("DATABASE_PW")
db_name = os.getenv("DATABASE_NAME")


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql+psycopg2://{pg_user}:{pg_pass}@{db_url}/{db_name}"
db = SQLAlchemy(app)


# @app.route('/api/birds', methods=['GET'])
# def get_birds():
#     response = {
#         "birds": sorted(birds)
#     }
#     return jsonify(response)


# @app.route('/api/seasons', methods=['GET'])
# def get_seasons():
#     response = {
#         "seasons": sorted(seasons)
#     }
#     return jsonify(response)


# @app.route('/api/states', methods=['GET'])
# def get_states():
#     response = {
#         "states": sorted(states)
#     }
#     return jsonify(response)


# @app.route('/api/counties', methods=['POST'])
# def get_county_from_state():
#     data = request.get_json()
#     state = data['state']
#     counties = state_counties[state]
#     response = {
#         'counties': sorted(counties)
#     }
#     return jsonify(response)


# @app.route('/api/results', methods=['POST'])
# def predict_bird():
#     data = request.get_json()

#     # needed_keys = ['bird', 'season', 'state', 'county']
#     # if not all(needed_keys) in data.keys():
#     #     message = "Invalid keys. Need 'bird', 'season', 'state', and 'county'"
#     #     return message, 400
    
#     bird = data['bird']
#     season = data['season']

#     county_state = data['county'] + ',' + data['state']
#     region = cs2r[county_state]

#     # encode features
#     X = pd.DataFrame({
#         'name': [bird],
#         'season': [season],
#         'region': [region]
#     })
#     X_encoded = encoder.transform(X)
#     # get prediction
#     pred = model.predict(X_encoded)
#     label = labels[pred[0]]

#     response = {
#         'prediction': label
#     }
#     return jsonify(response)

# if __name__ == "__main__":
#     app.run(host="0.0.0.0")