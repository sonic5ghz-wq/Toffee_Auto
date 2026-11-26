import requests
import json

# Toffee public channel list / API endpoint (requires Bangladesh IP or BD proxy)
API_URL = "https://toffeelive.com/api/v1/channels" 
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 Chrome/120.0.0.0 Mobile Safari/537.36",
    "Accept": "application/json"
}

def generate_m3u():
    try:
        response = requests.get(API_URL, headers=HEADERS, timeout=15)
        data = response.json()
    except Exception as e:
        print(f"Failed to fetch channel data: {e}")
        return

    m3u_lines = ["#EXTM3U\n"]

    for ch in data.get("channels", []):
        name = ch.get("name", "Unknown Channel")
        logo = ch.get("logo_url", "")
        category = ch.get("category", "Live TV")
        stream_url = ch.get("stream_url", "")
        cookie = ch.get("cookie", "") # Edge-Cache-Cookie token

        if not stream_url:
            continue

        m3u_lines.append(f'#EXTINF:-1 tvg-logo="{logo}" group-title="{category}",{name}\n')
        m3u_lines.append(f'#EXTVLCOPT:http-user-agent={HEADERS["User-Agent"]}\n')
        if cookie:
            http_header = json.dumps({"Cookie": cookie})
            m3u_lines.append(f'#EXTHTTP:{http_header}\n')
        m3u_lines.append(f'{stream_url}\n\n')

    with open("toffee_auto.m3u", "w", encoding="utf-8") as f:
        f.writelines(m3u_lines)
    print("Playlist updated successfully.")

if __name__ == "__main__":
    generate_m3u()
  
