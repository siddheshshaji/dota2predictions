# IMPORTING THE NECESSARY LIBRARIES
from flask import Flask, request, render_template
import pickle
import logging
import numpy as np
import pandas as pd
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

# IIMPORTING THE MODEL
model = pickle.load(open('dota_model.pkl','rb'))

# INITIALIZING SENTRY(FOR LOGGING)
sentry_sdk.init(
    dsn="https://343358c3f33744728f977a929a727af8@o401877.ingest.sentry.io/5262121",
    integrations=[FlaskIntegration()]
)

# INITIALIZING THE APP
app = Flask(__name__)

# LANDING PAGE
@app.route('/',methods = ['POST','GET'])
def htmlreturn():
    return render_template('home.html') 

# 404 PAGE HANDLER
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

# PREDICTION ROUTE
@app.route('/predict',methods = ['POST','GET'])
def predict():
    int_features = [0] * 220        # THE MODEL NEEDS AN INPUT OF AN ARRAY OF LENGTH 220 (SINCE THERE ARE 220 FEATURES)
    response = [int(x) for x in request.form.values()]   # COLLECTING THE INPUT AFTER THE USER PRESSES THE PREDICT BUTTON
    if len(set(response)) == 10:    # EXCEPTION HANDLING CONDITION 1: TO CHECK WHETHER A SINGLE HERO HAS BEEN SELECTED BY MORE THAN ONE PLAYERS IN THE SAME TEAM
        for i in response:
            int_features[i]=1       # SETTING CORRESPONDING INDICES OF THE ARRAY(AS VALUES RECEIVED FROM THE DROP DOWN INPUT VALUES, SET IN THE HTML INPUT FORM RESPONSE) AS 1 
        non_zeroes = [x for x in response if x != 0] # EXCEPTION HANDLING CONDITION 1: TO CHECK WHETHER A SINGLE HERO HAS BEEN SELECTED BY MORE THAN ONE PLAYERS FROM DIFFERENT TEAMS
        evens = [x for x in non_zeroes if x%2 == 0]
        for i in evens:
            if i+1 in non_zeroes:
                return render_template('home.html', prediction_text="Please choose different heroes for each team!")   # EXCEPTION HANDLING CONDITION 2 FAILURE POINT
            elif model.predict([int_features])==[1]:
                prediction = "Team 1"
                return render_template('home.html', prediction_text="Prediction: {} will win.".format(prediction))
            elif model.predict([int_features])==[0]:
                prediction = "Team 2"  
                return render_template('home.html', prediction_text="Prediction: {} will win.".format(prediction))   
    else:
        return render_template('home.html', prediction_text="Please choose different heores in each team slots!") # EXCEPTION HANDLING CONDITION 1 FAILURE POINT

if __name__ == '__main__':
    app.run()
