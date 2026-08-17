import requests

SOURCES = [
    "https://raw.githubusercontent.com/sportlive18/Sonyliv-Playlist-Autoupdate/refs/heads/main/sonyliv.m3u",
    "https://raw.githubusercontent.com/drmlive/fancode-live-events/refs/heads/main/fancode.m3u",
    "https://raw.githubusercontent.com/srhady/willow-event/refs/heads/main/live_sports.m3u"
]

OUTPUT = "Events_All.m3u"

entries = []

for url in SOURCES:
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        lines = response.text.splitlines()

        # Remove the source playlist header
        for line in lines:
            if line.strip() and line.strip() != "#EXTM3U":
                entries.append(line)

        print("Loaded:", url)

    except Exception as e:
        print("Failed:", url, e)

with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")
    f.write("\n".join(entries))

print("Created:", OUTPUT)
