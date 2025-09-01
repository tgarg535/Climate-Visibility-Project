import pickle
import os
import pandas as pd
from flask_app.services.weather_service import WeatherService

# Paths to the .pkl files
scaler_path = os.path.join('flask_app/models', 'scaler2.pkl')
model_path = os.path.join('flask_app/models', 'trained_model2.pkl')

# Load scaler
with open(scaler_path, 'rb') as f:
    scaler = pickle.load(f)

# Load trained model
with open(model_path, 'rb') as f:
    trained_model = pickle.load(f)

def predict_visibility_from_weather(lat, lon):
    """
    Predict visibility (meters) using weather data from OpenWeatherMap.
    """
    try:
        # Fetch weather
        weather_service = WeatherService()
        weather_data = weather_service.get_weather(lat, lon)

        # Extract raw values
        temp_k = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        wind_speed_mps = weather_data['wind']['speed']
        wind_deg = weather_data['wind']['deg']
        sea_level_hpa = weather_data['main'].get('sea_level', 0)  # fallback 0 if missing

        # Convert units to model input
        DRYBULBTEMPF = (temp_k - 273.15) * 9/5 + 32       # Kelvin → °F
        RelativeHumidity = humidity                        # %
        WindSpeed = wind_speed_mps * 2.23694              # m/s → mph
        WindDirection = wind_deg                           # degrees
        SeaLevelPressure = sea_level_hpa * 0.02953        # hPa → inHg

        # Create DataFrame with correct column names
        feature_names = ['DRYBULBTEMPF', 'RelativeHumidity', 'WindSpeed', 'WindDirection', 'SeaLevelPressure']
        X = pd.DataFrame([[DRYBULBTEMPF, RelativeHumidity, WindSpeed, WindDirection, SeaLevelPressure]],
                         columns=feature_names)

        # Scale features
        X_scaled = scaler.transform(X)

        # Predict visibility (model output in miles)
        predicted_visibility_miles = trained_model.predict(X_scaled)[0]

        # Convert miles → meters
        predicted_visibility_meters = abs(predicted_visibility_miles * 1609.34)

        print(f"Predicted visibility (meters) for ({lat}, {lon}): {predicted_visibility_meters:.2f}")
        return predicted_visibility_meters

    except Exception as e:
        print(f"Error predicting visibility: {e}")
        return None
