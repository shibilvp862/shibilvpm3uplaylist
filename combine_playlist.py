import requests

SOURCES = [
    "https://raw.githubusercontent.com/shibilvp862/shibilvpm3uplaylist/refs/heads/main/allSports.m3u8",
    "https://raw.githubusercontent.com/shibilvp862/shibilvpm3uplaylist/refs/heads/main/Malayalm%20channels.m3u8"
]

OUTPUT = "My_IPTV.m3u"

entries = []

for url in SOURCES:
    try:
        response = requests.get(
            url,
            timeout=30,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )
        response.raise_for_status()

        lines = response.text.splitlines()

        for line in lines:
            line = line.strip()

            if not line or line == "#EXTM3U":
                continue

            # Fix FanCode EXTINF format
            if line.startswith("#EXTINF:-1, tvg-logo="):
                line = line.replace(
                    "#EXTINF:-1, tvg-logo=",
                    "#EXTINF:-1 tvg-logo=",
                    1
                )

            entries.append(line)

        print("Loaded:", url)

    except Exception as e:
        print("Failed:", url, e)

# Create combined playlist
with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")
    f.write("\n".join(entries))
    f.write("\n")

print("Created:", OUTPUT)
print("Total lines:", len(entries))
