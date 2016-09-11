from flask import Flask, jsonify, render_template, request
import geocoder
import requests
import forecastio
import random
import os

app = Flask(__name__)

forecastio_key = os.environ.get('FORECASTIO_API_KEY')

@app.route('/pant_results_user')
def shouldPantsShouldBeWornFromInput():
    input = request.args.get('input')

    print("input: " + input)

    location = geocoder.google(input)
    print(location)
    print("latitude: " + str(location.lat))
    print("latitude: " + str(location.lng))

    return shouldPantsBeWorn(latitude=location.lat, longitude=location.lng, location=location)


@app.route('/pant_results_location')
def shouldPantsShouldBeWornFromLocation():
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')

    return shouldPantsBeWorn(latitude=latitude, longitude=longitude)



def shouldPantsBeWorn(latitude, longitude, location = None):
    forecast = forecastio.load_forecast(forecastio_key, latitude, longitude)
    temperature = forecast.currently().temperature

    if location is None:
        location = geocoder.google([latitude, longitude], method="reverse")

    detailsHTML = "<p>Right now, it's " + removePeriodAtEndOfString(forecast.minutely().summary.lower()) + " in " + location.city + ".</p>"
    detailsHTML += "<p>The temperature is currently " + str(round(temperature)) + "&deg;.</p>"

    if temperature > 75:  # pants should not be worn
        answer = random_line("splashes/negative.txt")
        detailsHTML += "<p>It's too hot for pants.</p>"
    else:  # pants should be worn
        answer=random_line("splashes/positive.txt")
        detailsHTML += "<p>You should really think about keeping your legs warm.</p>"

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
