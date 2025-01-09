import requests

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

def update_readme(weather):
    with open("README.md", "r") as file:
        readme_content = file.readlines()

    weather_info = (
        "## Weather in Takuapa, Phang Nga, Thailand\n"
        f"Temperature: {weather['temperature']}°C\n"
        f"Wind Speed: {weather['windspeed']} km/h\n"
        f"Weather Code: {weather['weathercode']}\n"
    )

    # Check if weather info already exists
    if any("## Weather in Takuapa, Phang Nga, Thailand" in line for line in readme_content):
        for i, line in enumerate(readme_content):
            if line.startswith("## Weather in Takuapa, Phang Nga, Thailand"):
                readme_content[i] = weather_info
                break
    else:
        readme_content.append("\n" + weather_info)

    with open("README.md", "w") as file:
        file.writelines(readme_content)

if __name__ == "__main__":
    weather = get_weather()
    update_readme(weather)