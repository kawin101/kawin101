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

def update_readme(weather):
    with open("README.md", "r") as file:
        readme_content = file.readlines()

    temperature_icon = get_temperature_icon(weather['temperature'])
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    weather_info = (
        "## Weather in Takuapa, Phang Nga, Thailand\n"
        f"Date/Time: {current_time}<br>\n"
        f"Temperature: {temperature_icon} {weather['temperature']}°C<br>\n"
        f"Wind Speed: {weather['windspeed']} km/h<br>\n"
    )

    start_index = None
    end_index = None

    # Find the start and end index of the weather info
    for i, line in enumerate(readme_content):
        if line.startswith("## Weather in Takuapa, Phang Nga, Thailand"):
            start_index = i
            break

    if start_index is not None:
        end_index = start_index + 4  # Assuming weather info block is 4 lines long
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