import requests

SOURCES = [
    "https://raw.githubusercontent.com/Free-TV/IPTV/master/playlist.m3u8"
]

OUTPUT = "Movies_FAST.m3u"

MOVIE_GROUPS = [
    "Movies",
    "Films",
    "Film",
    "Cinema",
    "Hollywood",
    "Bollywood",
    "Action",
    "Comedy",
    "Drama",
    "Thriller",
    "Horror",
    "Sci-Fi",
    "Family"
]

with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write('#EXTM3U x-tvg-url="https://iptv-epg.org/files/epg-gb.xml.gz,https://iptv-epg.org/files/epg-us.xml.gz,https://iptv-epg.org/files/epg-ca.xml.gz,https://iptv-epg.org/files/epg-au.xml.gz"\n')

    seen = set()

    for url in SOURCES:
        try:
            lines = requests.get(url, timeout=30).text.splitlines()

            i = 0
            while i < len(lines):
                if lines[i].startswith("#EXTINF") and i + 1 < len(lines):
                    extinf = lines[i]
                    stream = lines[i + 1]

                    lower = extinf.lower()

                    if any(g.lower() in lower for g in MOVIE_GROUPS):
                        if stream not in seen:
                            seen.add(stream)
                            f.write(extinf + "\n")
                            f.write(stream + "\n")

                    i += 2
                else:
                    i += 1

            print("Loaded:", url)

        except Exception as e:
            print("Failed:", e)

print("Created:", OUTPUT)
