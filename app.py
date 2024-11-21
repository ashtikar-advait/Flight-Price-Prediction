from flask import Flask, request, render_template
from flask_cors import cross_origin
import sklearn
import pandas as pd
import pickle

app = Flask(__name__)
model = pickle.load(open("flight_rf.pkl", "rb"))


@app.route("/")
@cross_origin()
def home():
    return render_template("home.html")


@app.route("/predict", methods=["GET", "POST"])
@cross_origin()
def predict():
    if request.method == "POST":

        # Date of Journey:
        date_dep = request.form["Dep_Time"]
        Journey_day = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").day)
        Journey_month = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").month)

        # Departure
        Dep_hour = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").hour)
        Dep_min = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").minute)

        # Arrival
        date_arr = request.form["Arrival_Time"]
        Arrival_hour = int(pd.to_datetime(date_arr, format="%Y-%m-%dT%H:%M").hour)
        Arrival_min = int(pd.to_datetime(date_arr, format="%Y-%m-%dT%H:%M").minute)

        # Duration
        dur_hour = abs(Arrival_hour - Dep_hour)
        dur_min = abs(Arrival_min - Dep_min)

        # Total Stops
        Total_stops = int(request.form["stops"])

        # Airline
        airline = request.form["airline"]
        airlines = [
            "Jet Airways",
            "IndiGo",
            "Air India",
            "Multiple carriers",
            "SpiceJet",
            "Vistara",
            "GoAir",
            "Multiple carriers Premium economy",
            "Jet Airways Business",
            "Vistara Premium economy",
            "Trujet",
        ]
        values = {key: 0 for key in airlines}
        if airline in values:
            values[airline] = 1
        Jet_Airways = values["Jet Airways"]
        IndiGo = values["IndiGo"]
        Air_India = values["Air India"]
        Multiple_carriers = values["Multiple carriers"]
        SpiceJet = values["SpiceJet"]
        Vistara = values["Vistara"]
        GoAir = values["GoAir"]
        Multiple_carriers_Premium_economy = values["Multiple carriers Premium economy"]
        Jet_Airways_Business = values["Jet Airways Business"]
        Vistara_Premium_economy = values["Vistara Premium economy"]
        Trujet = values["Trujet"]

        # Source
        Source = request.form["Source"]
        sources = {"Delhi": 0, "Kolkata": 0, "Mumbai": 0, "Chennai": 0}
        if Source in sources:
            sources[Source] = 1
        s_Delhi = sources["Delhi"]
        s_Kolkata = sources["Kolkata"]
        s_Mumbai = sources["Mumbai"]
        s_Chennai = sources["Chennai"]

        # Destination
        Destination = request.form["Destination"]
        destinations = {
            "Cochin": 0,
            "Delhi": 0,
            "Bangalore": 0,
            "Hyderabad": 0,
            "Kolkata": 0,
        }
        if Destination in destinations:
            destinations[Destination] = 1
        d_Cochin = destinations["Cochin"]
        d_Delhi = destinations["Delhi"]
        d_Bangalore = destinations["Bangalore"]
        d_Hyderabad = destinations["Hyderabad"]
        d_Kolkata = destinations["Kolkata"]

        features = [ Total_stops, Journey_day, Journey_month, Dep_hour, Dep_min, Arrival_hour, Arrival_min, dur_hour, dur_min, Air_India, GoAir, IndiGo, Jet_Airways, Jet_Airways_Business, Multiple_carriers, SpiceJet, Vistara, Multiple_carriers_Premium_economy, Vistara_Premium_economy, Trujet, s_Chennai, s_Delhi, s_Kolkata, s_Mumbai, d_Cochin, d_Delhi, d_Bangalore, d_Hyderabad, d_Kolkata ]


        prediction = model.predict([features])
        output = round(prediction[0], 2)
        return render_template(
            "home.html", prediction_text=f"Your Filght Price is ₹{output}"
        )
    return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True, port=5000)

