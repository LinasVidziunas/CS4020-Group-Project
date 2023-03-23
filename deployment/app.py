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
model_path: pathlib.Path = pathlib.Path('../models/random_forest_regressor.pkl').absolute()
assert model_path.is_file(), f'Model file not found under {model_path}'
with open(model_path, 'rb') as f:
    model = pickle.load(f)

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
    input_sequence = ['Airline', 
                      'Year', 
                      'Distance', 
                      'DestState', 
                      'OriginState', 
                      'DestCityName', 
                      'CRSArrTime', 
                      'DayOfWeek', 
                      'OriginCityName', 
                      'Month', 
                      'CRSDepTime', 
                      'DayofMonth']

    input: Dict = {}

    req = request.form.to_dict()

    for key, value in req.items():
        if key in label_encoders.keys():
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
    print(input)

    predicted = model.predict(input)[0]
        
    return jsonify({'predicted': predicted})

@app.route('/get_category_values/<category>', methods=['GET'])
def get_category_values(category: str):
    return jsonify(label_encoders[category].classes_.tolist())

if __name__ == '__main__':
    app.run(port=8090, debug=True)