import os
import requests
from datetime import datetime
import pytz  # ใช้กำหนดโซนเวลาเป็น UTC+7

# โหลดค่าจาก GitHub Secrets
USER_REPO = os.getenv("USER_REPO")  # เช่น "kawin101/weather-update"
USER_USERNAME = os.getenv("USER_USERNAME")  # เช่น "kawin101"
USER_EMAIL = os.getenv("USER_EMAIL")  # เช่น "your_email@gmail.com"
LATITUDE = os.getenv("LATITUDE")  # ค่าพิกัด latitude
LONGITUDE = os.getenv("LONGITUDE")  # ค่าพิกัด longitude
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # GitHub Token (ใช้สำหรับ push)

def get_weather():
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "current_weather": True,
        "timezone": "Asia/Bangkok"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get("current_weather", {})
    else:
        print(f"Error fetching weather data: {response.status_code}")
        return None

def get_temperature_icon(temperature):
    if temperature < 0:
        return "❄️"
    elif temperature < 10:
        return "🥶"
    elif temperature < 20:
        return "🧥"
    elif temperature < 30:
        return "🌤️"
    else:
        return "🔥"

def update_readme(weather):
    # กำหนด timezone เป็น UTC+7 (Asia/Bangkok)
    bangkok_tz = pytz.timezone("Asia/Bangkok")
    current_time = datetime.now(bangkok_tz).strftime("%Y-%m-%d %H:%M:%S")

    temperature_icon = get_temperature_icon(weather['temperature'])

    weather_info = (
        f"### Weather\n"
        f"<!-- ใช้เวลา ประเทศไทย --> UTC +7\n"
        f"🕒 **Date/Time:** {current_time}<br>\n"
        f"🌡️ **Temperature:** {temperature_icon} {weather['temperature']}°C<br>\n"
        f"💨 **Wind Speed:** {weather['windspeed']} km/h<br>\n"
    )

    start_marker = "### Weather"
    end_marker = "<!--WEATHER_UPDATE-->"

    with open("README.md", "r", encoding="utf-8") as file:
        readme_content = file.readlines()

    start_index = None
    end_index = None

    for i, line in enumerate(readme_content):
        if start_marker in line and start_index is None:  # หาตำแหน่งของ Weather ที่ถูกต้อง
            start_index = i
        if end_marker in line:
            end_index = i
            break

    if start_index is not None and end_index is not None:
        readme_content[start_index:end_index+1] = [weather_info + "\n", end_marker + "\n"]
    else:
        readme_content.append("\n" + start_marker + "\n" + weather_info + "\n" + end_marker + "\n")

    with open("README.md", "w", encoding="utf-8") as file:
        file.writelines(readme_content)

def push_to_github():
    os.system(f"git config --global user.name '{USER_USERNAME}'")
    os.system(f"git config --global user.email '{USER_EMAIL}'")
    os.system("git add README.md")
    os.system("git commit -m 'Update weather information' || exit 0")
    os.system(f"git push https://x-access-token:{GITHUB_TOKEN}@github.com/{USER_REPO}.git || exit 0")

if __name__ == "__main__":
    weather = get_weather()
    if weather:
        update_readme(weather)
        push_to_github()
        print("README.md updated successfully")
