from flask import Flask, request, render_template, url_for, render_template
import pickle
import logging
import numpy as np
import pandas as pd
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

model = pickle.load(open('dota_model.pkl','rb'))

sentry_sdk.init(
    dsn="https://343358c3f33744728f977a929a727af8@o401877.ingest.sentry.io/5262121",
    integrations=[FlaskIntegration()]
)
app = Flask(__name__)

@app.route('/',methods = ['POST','GET'])
def htmlreturn():
    return render_template('home.html') 

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

@app.route('/predict',methods = ['POST','GET'])
def predict():
    int_features = [0] * 20
    response = [int(x) for x in request.form.values()]
    if len(set(response)) == 10:
        for i in response:
            int_features[i]=1        
        non_zeroes = [x for x in response if x != 0]
        evens = [x for x in non_zeroes if x%2 == 0]
        for i in evens:
            if i+1 in non_zeroes:
                return render_template('home.html', prediction_text="Please choose different heroes for each team!")
            elif model.predict([int_features])==[1]:
                prediction = "Team 1"
                return render_template('home.html', prediction_text="Prediction: {} will win.".format(prediction))
            elif model.predict([int_features])==[0]:
                prediction = "Team 2"  
                return render_template('home.html', prediction_text="Prediction: {} will win.".format(prediction))   
    else:
        return render_template('home.html', prediction_text="Please choose different heores in each team slots!")

if __name__ == '__main__':
    app.run()
