import pathlib
import pickle
from typing import Generator, Dict # For type hinting
from datetime import date

import numpy as np
from flask import Flask, request, jsonify, render_template
import pandas as pd

# Define the flask app
app = Flask(__name__)

# Load the random forest model
model = {}
model_path: pathlib.Path = pathlib.Path('../models/random_forest_regressor.pkl').absolute()
assert model_path.is_file(), f'Model file not found under {model_path}'
with open(model_path, 'rb') as f:
    model['Random Forest'] = pickle.load(f)

# Read the neural network model
model_path: pathlib.Path = pathlib.Path('../models/nn.pkl').absolute()
assert model_path.is_file(), f'Model file not found under {model_path}'
with open(pathlib.Path(model_path), 'rb') as f:
    model['NN'] = pickle.load(f)

# Load saveds label encoders
label_paths: Generator = pathlib.Path('../datasets/processed/').glob('label_encoder_*.pkl')
label_encoders: Dict = {}
for label_path in label_paths:
    with open(label_path, 'rb') as f:
        label_encoder_name: str = str(label_path.stem).replace('label_encoder_', '')
        label_encoders[label_encoder_name] = pickle.load(f)

assert pathlib.Path('templates/index.html').is_file(), 'Template file not found.'

@app.route('/',methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    input_sequence = ['DayOfWeek',
                      'DayofMonth',
                      'CRSDepTime',
                      'Airline',
                      'Distance',
                      'OriginCityName',
                      'OriginState',
                      'DestCityName',
                      'Month',
                      'DestAirport',
                      'DestState',
                      'OriginAirport',
                      'Year',
                      'CRSArrTime']

    input: Dict = {}

    req = request.form.to_dict()

    for key, value in req.items():
        if key in label_encoders.keys():
            print(key)
            value = label_encoders[key].transform([value])
        elif 'Time' in key:
            value = int(value.replace(':', ''))

        if key in input_sequence and key != 'flight_date':
            input[key] = value

    flight_date = date.fromisoformat(req['flight_date'])
    input['Month'] = flight_date.month
    input['DayofMonth'] = flight_date.day
    input['DayOfWeek'] = flight_date.weekday()
    input['Year'] = flight_date.year

    input = pd.DataFrame(input)
    input = input[input_sequence]

    predicted = 0
    if req['model'] == 'Random Forest':
        predicted = model[req['model']].predict(input)[0]
    elif req['model'] == 'NN':
        predicted = model[req['model']].predict(np.asarray(input).astype('float32'))[0][0]
        

    print(predicted)
    return jsonify({'predicted': float(predicted)})


@app.route('/get_category_values/<category>', methods=['GET'])
def get_category_values(category: str):
    return jsonify(label_encoders[category].classes_.tolist())

if __name__ == '__main__':
    app.run(port=8090, debug=True)