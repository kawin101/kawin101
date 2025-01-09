import requests
from datetime import datetime
import git
import os

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
    else:
        return "😎"  # Sunglasses for temperatures 20°C and above

def update_readme(weather_info):
    with open("README.md", "r") as file:
        readme_content = file.readlines()

    start_index = None
    end_index = None

    # Find the start and end index of the weather info
    for i, line in enumerate(readme_content):
        if line.startswith("## Weather in Takuapa, Phang Nga, Thailand"):
            start_index = i
            break

    weather_info_str = f"## Weather in Takuapa, Phang Nga, Thailand\nTemperature: {weather_info['temperature']}°C {get_temperature_icon(weather_info['temperature'])}\n"

    if start_index is not None:
        end_index = start_index + 4  # Assuming weather info block is 4 lines long
        readme_content[start_index:end_index] = [weather_info_str]
    else:
        readme_content.append(weather_info_str)

    with open("README.md", "w") as file:
        file.writelines(readme_content)

def push_to_github():
    repo_path = os.getenv('GITHUB_WORKSPACE', '/home/runner/work/kawin101/kawin101')
    repo = git.Repo(repo_path)
    repo.git.add('README.md')
    repo.index.commit('Update weather information')
    origin = repo.remote(name='origin')
    origin.push()

if __name__ == "__main__":
    weather = get_weather()
    update_readme(weather)
    push_to_github()