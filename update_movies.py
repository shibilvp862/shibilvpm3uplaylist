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

            # JSON has a "movies" array
            movies = data.get("movies", [])

            for movie in movies:
                title = movie.get("title", "Unknown Movie")
                youtube = movie.get("url")
                poster = movie.get("thumbnail", "")

                if youtube:
                    f.write(
                        f'#EXTINF:-1 tvg-logo="{poster}" group-title="{group}",{title}\n'
                    )
                    f.write(youtube + "\n")

            print("Loaded:", group, len(movies))

        except Exception as e:
            print("Failed:", group, e)

print("Created:", OUTPUT)
