import requests
import os


class WeatherService:
    
    def __init__(self, api_key=None):
        # You can set your API key as an environment variable or pass it directly
        self.api_key = os.getenv("OPENWEATHER_API_KEY")

    def get_weather(self, lat, lon):
        """
        Fetch current weather directly using latitude & longitude.
        """
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={self.api_key}&units=metric"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    

    def air_pollution(self, lat, lon):
        """
        Fetch air pollution data using latitude & longitude.
        """
        url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={self.api_key}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def get_forecast(self, lat, lon):
        """
        Fetches 5-day/3-hour forecast and returns a neat JSON-serializable dict.
        """
        url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={self.api_key}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        forecast = []
        for entry in data["list"]:
            dt = entry["dt_txt"]
            weather_info = entry["weather"][0]

            forecast.append({
                "datetime": dt,
                "weather": weather_info["description"].capitalize(),
                "icon_url": f"http://openweathermap.org/img/wn/{weather_info['icon']}@2x.png",
                "temperature_C": round(entry["main"]["temp"] - 273.15, 1),
                "feels_like_C": round(entry["main"]["feels_like"] - 273.15, 1),
                "humidity_%": entry["main"]["humidity"],
                "pressure_hPa": entry["main"]["pressure"],
                "wind_speed_mps": entry["wind"]["speed"],
                "wind_direction_deg": entry["wind"]["deg"],
                "visibility_m": entry.get("visibility", None),
                "rain_mm": entry.get("rain", {}).get("3h", 0),
                "snow_mm": entry.get("snow", {}).get("3h", 0)
            })

        return {"forecast": forecast}  # JSON-serializable dict

    def manual_weather_request(self, city=None, state=None, country=None):
        """
        Fetch latitude and longitude based search data using manual API request.
        Accepts city, state, and/or country. Returns results if any match.
        """
        if not city and not state and not country:
            raise ValueError("At least one of city, state, or country must be provided.")

        # Build query dynamically
        query_parts = [part for part in [city, state, country] if part]
        query = ",".join(query_parts)

        url = f"http://api.openweathermap.org/geo/1.0/direct?q={query}&limit=5&appid={self.api_key}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()