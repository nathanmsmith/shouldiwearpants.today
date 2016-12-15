from flask import Flask, json, jsonify, render_template, request
import geocoder
import requests
import forecastio
import random
import os
from werkzeug.contrib.fixers import ProxyFix

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

forecastio_key = os.environ.get('FORECASTIO_API_KEY')


@app.route('/pant_results_user')
def shouldPantsShouldBeWornFromInput():
    input = request.args.get('input')

    print("input: " + input)

    location = geocoder.google(input)
    print(location)
    print("latitude: " + str(location.lat))
    print("latitude: " + str(location.lng))

    return shouldPantsBeWorn(latitude=location.lat,
                             longitude=location.lng,
                             location=location)


@app.route('/pant_results_location')
def shouldPantsShouldBeWornFromLocation():
    ip = request.remote_addr
    data = json.loads(requests.get('http://freegeoip.net/json/' + ip).text)

    print(data)

    return shouldPantsBeWorn(latitude=data['latitude'],
                             longitude=data['longitude'])


def shouldPantsBeWorn(latitude, longitude, location=None):
    forecast = forecastio.load_forecast(forecastio_key, latitude, longitude)
    temperature = forecast.currently().temperature
    minutelySummary = forecast.minutely().summary

    if forecast.json['flags']['units'] == "us":
        unit = "F"
    else:
        unit = "C"

    if location is None:
        location = geocoder.google([latitude, longitude], method="reverse")

    # Since a minutely summary may not be defined by Dark Sky, fallback on
    # currently summary if need be
    if minutelySummary is not None:
        detailsHTML = ("<p>Right now, it's "
                       + removePeriodAtEndOfString(minutelySummary.lower())
                       + " in " + location.city + ".</p>")
    elif location.city is not None:
        detailsHTML = ("<p>Right now, the forecast for " + location.city
                       + " is: " + forecast.currently().summary + ".</p>")
    else:
        detailsHTML = ("<p>Right now, the forecast is " + forecast.currently().summary + ".</p>")
    detailsHTML += ("<p>The temperature is currently "
                    + str(round(temperature)) + "&deg;" + unit + ".</p>")

    if unit == "C":
        temperature = (temperature*9/5)+32

    if temperature > 75:  # pants should not be worn
        answer = random_line("splashes/negative.txt")
        detailsHTML += "<p>It's too hot for pants.</p>"
    else:  # pants should be worn
        answer = random_line("splashes/positive.txt")
        detailsHTML += ("<p>You should really think about "
                        "keeping your legs warm.</p>")

    return jsonify(answer=answer, details=detailsHTML)


@app.route('/')
def pants():
    return render_template("main.html")


def random_line(file):
    return random.choice(open(file).readlines())


def removePeriodAtEndOfString(str):
    if str.endswith("."):
        return str[:-len(".")]
    return str

if __name__ == '__main__':
    app.run()
