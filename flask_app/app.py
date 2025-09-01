from flask import Flask, render_template, session, request, jsonify
import requests
from .services.weather_service import WeatherService
from .services.prediction_service import predict_visibility_from_weather
import os


app = Flask(__name__)
app.secret_key = "fjhbsfhjbargfjhbaerjhbqwrhj2bmensf"  # Use a long, random string in production

weather_service_instance = WeatherService()


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/set_location')
def set_location():
    lat = request.args.get("lat")
    lon = request.args.get("lon")
    session["lat"] = lat
    session["lon"] = lon
    return jsonify({"status": "ok", "lat": lat, "lon": lon})


@app.route('/weather')
def get_weather():
    lat = session.get("lat")
    lon = session.get("lon")
    if not lat or not lon:
        return jsonify({"error": "Location not set"}), 400
    data = weather_service_instance.get_weather(lat, lon)
    return jsonify(data)


@app.route('/forecast')
def get_forecast():
    lat = request.args.get("lat") or session.get("lat")
    lon = request.args.get("lon") or session.get("lon")
    if not lat or not lon:
        return jsonify({"error": "Location not provided"}), 400
    data = weather_service_instance.get_forecast(lat, lon)
    return jsonify(data)


@app.route('/air_pollution')
def get_air_pollution():
    lat = session.get("lat")
    lon = session.get("lon")
    if not lat or not lon:
        return jsonify({"error": "Location not set"}), 400
    data = weather_service_instance.air_pollution(lat, lon)
    return jsonify(data)


@app.route('/manual_search', methods=['POST'])
def manual_search():
    """
    Search weather by city/state/country manually.
    Stores first result's lat/lon in session and returns location info.
    """
    data = request.get_json()
    city = data.get("city")
    state = data.get("state")
    country = data.get("country")

    if not city:
        return jsonify({"error": "City is required"}), 400

    try:
        results = weather_service_instance.manual_weather_request(city, state, country)
        if not results:
            return jsonify({"error": "No results found"}), 404

        # Take the first matching location
        loc = results[0]
        session["lat"] = loc.get("lat")
        session["lon"] = loc.get("lon")

        return jsonify({
            "status": "ok",
            "location": {
                "name": loc.get("name"),
                "lat": loc.get("lat"),
                "lon": loc.get("lon"),
                "country": loc.get("country"),
                "state": loc.get("state")
            }
        })

    except requests.HTTPError as e:
        return jsonify({"error": str(e)}), 500
    


@app.route("/predicted_visibility")
def predicted_visibility():
    try:
        lat = float(request.args.get('lat'))
        lon = float(request.args.get('lon'))
        predicted_vis = predict_visibility_from_weather(lat, lon)

        print(f"Predicted visibility for ({lat},{lon}): {predicted_vis}")  # Debug

        if predicted_vis is None:
            return jsonify({"error": "Prediction failed"}), 500

    
        return jsonify({"predicted_visibility": round(predicted_vis, 1)})  # meters
    except Exception as e:
        print(f"Error in /predicted_visibility route: {e}")
        return jsonify({"predicted_visibility": 0.0})  # fallback
    

@app.route('/climate_news')
def get_climate_news():
    api_key = os.getenv('NEWSAPI_KEY') 
    city = "New Delhi"  # optionally pass via query param

    url = f"https://newsapi.org/v2/everything?q=climate OR weather AND {city}&language=en&sortBy=publishedAt&pageSize=6&apiKey={api_key}"
    res = requests.get(url)
    data = res.json()
    return jsonify(data)  # send JSON to frontend


if __name__ == '__main__':
    app.run(debug=True)
