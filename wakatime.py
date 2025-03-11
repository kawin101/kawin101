import os
import requests
from datetime import datetime

# ดึง API Key จาก GitHub Secrets
WAKATIME_API_KEY = os.getenv("WAKATIME_API_KEY")

# URL สำหรับเรียกข้อมูลจาก Wakatime API
API_URL = f"https://wakatime.com/api/v1/users/current/stats/all_time?api_key={WAKATIME_API_KEY}"

def fetch_wakatime_data():
    """ดึงข้อมูลสถิติการเขียนโค้ดจาก Wakatime API"""
    response = requests.get(API_URL)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data: {response.status_code}")
        return None

def format_wakatime_data(data):
    """แปลงข้อมูลจาก API เป็นข้อความที่จะแสดงใน README.md"""
    if not data or "data" not in data:
        return "Error retrieving data."

    total_seconds = data["data"]["total_seconds"]
    languages = data["data"]["languages"]

    # แปลงวินาทีเป็น ชั่วโมง และ นาที
    total_hours = int(total_seconds // 3600)
    total_minutes = int((total_seconds % 3600) // 60)

    formatted_data = (
        f"```txt\n"
        f"From: {data['data']['start']} - To: {datetime.utcnow().strftime('%d %B %Y')}\n\n"
        f"Total Time: {total_hours} hrs {total_minutes} mins\n\n"
    )

    for lang in languages:
        lang_hours = int(lang["total_seconds"] // 3600)
        lang_minutes = int((lang["total_seconds"] % 3600) // 60)
        percentage = lang["percent"]
        formatted_data += f"{lang['name']:<25} {lang_hours} hrs {lang_minutes} mins {percentage:>5.2f} %\n"

    formatted_data += "```\n"
    return formatted_data

def update_readme(content):
    """อัปเดตข้อมูลสถิติ Wakatime ลงใน README.md"""
    with open("README.md", "r", encoding="utf-8") as file:
        readme_content = file.readlines()

    start_marker = "<!--START_SECTION:waka-->"
    end_marker = "<!--END_SECTION:waka-->"

    start_index = None
    end_index = None

    for i, line in enumerate(readme_content):
        if start_marker in line:
            start_index = i
        if end_marker in line:
            end_index = i
            break

    if start_index is not None and end_index is not None:
        readme_content[start_index+1:end_index] = [content + "\n"]
    else:
        readme_content.append("\n" + start_marker + "\n" + content + "\n" + end_marker + "\n")

    with open("README.md", "w", encoding="utf-8") as file:
        file.writelines(readme_content)

def push_to_github():
    """Push ไฟล์ README.md ที่อัปเดตกลับไปที่ GitHub"""
    os.system("git config --global user.name 'github-actions'")
    os.system("git config --global user.email 'github-actions@github.com'")
    os.system("git add README.md")
    os.system("git commit -m 'Update Wakatime Stats' || exit 0")
    os.system("git push")

if __name__ == "__main__":
    data = fetch_wakatime_data()
    if data:
        formatted_content = format_wakatime_data(data)
        update_readme(formatted_content)
        push_to_github()
        print("README.md updated successfully")
