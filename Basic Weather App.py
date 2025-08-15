
import requests

# Replace with your own OpenWeatherMap API key
API_KEY = "30e1459bed658d56e918be559ba9f618"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather(city):
    try:
        params = {
            "q": city,
            "appid": API_KEY,
            "units": "metric"  # Change to "imperial" for Fahrenheit
        }
        response = requests.get(BASE_URL, params=params)
        data = response.json()

        if data.get("cod") != 200:
            print("❌ Error:", data.get("message", "Unknown error"))
            return

        city_name = data["name"]
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        condition = data["weather"][0]["description"]

        print(f"\n📍 Weather in {city_name}:")
        print(f"🌡 Temperature: {temp}°C")
        print(f"🤔 Feels Like: {feels_like}°C")
        print(f"💧 Humidity: {humidity}%")
        print(f"☁ Condition: {condition.capitalize()}")

    except requests.exceptions.RequestException as e:
        print("⚠ Network error:", e)

if __name__ == "__main__":
    print("=== Simple Weather App ===")
    city = input("Enter city name: ").strip()
    if city:
        get_weather(city)
    else:
        print("❌ Please enter a valid city name.")
