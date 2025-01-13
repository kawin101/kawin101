import requests
from datetime import datetime
import git

def get_weather():
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 8.864,  # Latitude for Takuapa
        "longitude": 98.355,  # Longitude for Takuapa
        "current_weather": True,
        "timezone": "Asia/Bangkok"
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data['current_weather']

def get_temperature_icon(temperature):
    if temperature < 0:
        return "❄️"  # Snowflake for temperatures below 0°C
    elif temperature < 10:
        return "🥶"  # Cold face for temperatures below 10°C
    elif temperature < 20:
        return "🧥"  # Coat for temperatures below 20°C
    elif temperature < 30:
        return "🌤️"  # Sun behind small cloud for temperatures below 30°C
    else:
        return "🔥"  # Fire for temperatures 30°C and above

def get_weather_icon(weather_code):
    weather_icons = {
        0: "☀️",  # Clear sky
        1: "🌤️",  # Mainly clear
        2: "⛅",  # Partly cloudy
        3: "☁️",  # Overcast
        45: "🌫️",  # Fog
        48: "🌫️",  # Depositing rime fog
        51: "🌦️",  # Drizzle: Light
        53: "🌦️",  # Drizzle: Moderate
        55: "🌦️",  # Drizzle: Dense intensity
        56: "🌧️",  # Freezing Drizzle: Light
        57: "🌧️",  # Freezing Drizzle: Dense intensity
        61: "🌧️",  # Rain: Slight
        63: "🌧️",  # Rain: Moderate
        65: "🌧️",  # Rain: Heavy intensity
        66: "🌨️",  # Freezing Rain: Light
        67: "🌨️",  # Freezing Rain: Heavy intensity
        71: "🌨️",  # Snow fall: Slight
        73: "🌨️",  # Snow fall: Moderate
        75: "🌨️",  # Snow fall: Heavy intensity
        77: "🌨️",  # Snow grains
        80: "🌧️",  # Rain showers: Slight
        81: "🌧️",  # Rain showers: Moderate
        82: "🌧️",  # Rain showers: Violent
        85: "🌨️",  # Snow showers slight
        86: "🌨️",  # Snow showers heavy
        95: "⛈️",  # Thunderstorm: Slight or moderate
        96: "⛈️",  # Thunderstorm with slight hail
        99: "⛈️",  # Thunderstorm with heavy hail
    }
    return weather_icons.get(weather_code, "❓")  # Default to question mark if code is unknown

def update_readme(weather):
    with open("README.md", "r") as file:
        readme_content = file.readlines()

    temperature_icon = get_temperature_icon(weather['temperature'])
    weather_icon = get_weather_icon(weather['weathercode'])
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    weather_info = (
        "## Weather in Takuapa, Phang Nga, Thailand\n"
        f"🕒 Date/Time: {current_time}<br>\n"
        f"🌡️ Temperature: {temperature_icon} {weather['temperature']}°C<br>\n"
        f"💨 Wind Speed: {weather['windspeed']} km/h<br>\n"
        f"🌦️ Weather: {weather_icon}<br>\n"
    )

    start_index = None
    end_index = None

    # Find the start and end index of the weather info
    for i, line in enumerate(readme_content):
        if line.startswith("## Weather in Takuapa, Phang Nga, Thailand"):
            start_index = i
            break

    if start_index is not None:
        end_index = start_index + 5  # Assuming weather info block is 5 lines long
        readme_content[start_index:end_index] = [weather_info]
    else:
        readme_content.append(weather_info)

    with open("README.md", "w") as file:
        file.writelines(readme_content)

def push_to_github():
    repo = git.Repo('/Users/kawin101/Desktop/kawin101')
    repo.git.add('README.md')
    repo.index.commit('Update weather information')
    origin = repo.remote(name='origin')
    origin.push()

if __name__ == "__main__":
    weather = get_weather()
    update_readme(weather)
    push_to_github()