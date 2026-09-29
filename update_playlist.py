import requests

SOURCES = [
    "https://raw.githubusercontent.com/shibilvp862/shibilvpm3uplaylist/refs/heads/main/allSports.m3u8",
    "https://raw.githubusercontent.com/shibilvp862/shibilvpm3uplaylist/refs/heads/main/Malayalm%20channels.m3u8"
]

OUTPUT = "My_IPTV.m3u"

entries = []

for url in SOURCES:
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        lines = response.text.splitlines()

        for line in lines:
            if line.strip() and line.strip() != "#EXTM3U":

                # Fix FanCode EXTINF format
                if line.startswith("#EXTINF:-1, tvg-logo="):
                    line = line.replace("#EXTINF:-1, tvg-logo=", "#EXTINF:-1 tvg-logo=", 1)

                entries.append(line)

        print("Loaded:", url)

    except Exception as e:
        print("Failed:", url, e)

with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")
    f.write("\n".join(entries))

print("Created:", OUTPUT)
