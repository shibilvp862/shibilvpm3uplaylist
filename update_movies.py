import requests

SOURCES = [
    ("Tamil", "https://raw.githubusercontent.com/sayanpal514-hue/MINI-YT-HUB/refs/heads/main/movies/tamil/tamil.json"),
    ("English", "https://raw.githubusercontent.com/sayanpal514-hue/MINI-YT-HUB/refs/heads/main/movies/english/english.json"),
    ("Hindi", "https://raw.githubusercontent.com/sayanpal514-hue/MINI-YT-HUB/refs/heads/main/movies/hindi/hindi.json"),
    ("Hollywood", "https://raw.githubusercontent.com/sayanpal514-hue/MINI-YT-HUB/refs/heads/main/movies/hollywood/hollywood.json"),
    ("Other", "https://raw.githubusercontent.com/sayanpal514-hue/MINI-YT-HUB/refs/heads/main/movies/other/other.json")
]

OUTPUT = "Movies_All.m3u"

with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")

    for group, url in SOURCES:
        try:
            data = requests.get(url, timeout=30).json()

            for movie in data:
                title = movie.get("title") or movie.get("name") or "Unknown Movie"
                youtube = movie.get("url") or movie.get("youtube") or movie.get("link")
                poster = movie.get("poster") or movie.get("image") or movie.get("thumbnail") or ""

                if youtube:
                    extinf = f'#EXTINF:-1 tvg-logo="{poster}" group-title="{group}",{title}'
                    f.write(extinf + "\n")
                    f.write(youtube + "\n")

            print("Loaded:", group)

        except Exception as e:
            print("Failed:", group, e)

print("Created:", OUTPUT)
