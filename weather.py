import os
import requests
from datetime import datetime

# ดึงค่า TOKEN และ REPO_URL จาก GitHub Secrets
GITHUB_REPO = os.getenv("GITHUB_REPO")
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def get_weather():
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 8.864,  # Latitude for Takuapa
        "longitude": 98.355,  # Longitude for Takuapa
        "current_weather": True,
        "timezone": "Asia/Bangkok"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()["current_weather"]
    else:
        print(f"Error fetching weather data: {response.status_code}")
        return None

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
    with open("README.md", "r", encoding="utf-8") as file:
        readme_content = file.readlines()

    temperature_icon = get_temperature_icon(weather['temperature'])
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    weather_info = (
        "### Weather in Takuapa, Phang Nga, Thailand\n"
        f"🕒 **Date/Time:** {current_time}<br>\n"
        f"🌡️ **Temperature:** {temperature_icon} {weather['temperature']}°C<br>\n"
        f"💨 **Wind Speed:** {weather['windspeed']} km/h<br>\n"
    )

    start_marker = "### Weather"
    end_marker = "<!--WEATHER_UPDATE-->"

    start_index = None
    end_index = None

    # หาตำแหน่งที่ต้องอัปเดตใน README.md
    for i, line in enumerate(readme_content):
        if line.strip() == start_marker:
            start_index = i
        if line.strip() == end_marker:
            end_index = i
            break

    if start_index is not None and end_index is not None:
        readme_content[start_index+1:end_index] = [weather_info + "\n"]
    else:
        readme_content.append("\n" + start_marker + "\n" + weather_info + "\n" + end_marker + "\n")

    with open("README.md", "w", encoding="utf-8") as file:
        file.writelines(readme_content)

def push_to_github():
    os.system("git config --global user.name 'github-actions'")
    os.system("git config --global user.email 'github-actions@github.com'")
    os.system("git add README.md")
    os.system("git commit -m 'Update weather information'")
    os.system(f"git push https://{GITHUB_USERNAME}:{GITHUB_TOKEN}@github.com/{GITHUB_REPO}.git")

if __name__ == "__main__":
    weather = get_weather()
    if weather:
        update_readme(weather)
        push_to_github()
        print("README.md updated successfully")
