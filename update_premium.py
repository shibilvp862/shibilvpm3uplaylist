import requests
import re

SOURCES = [
    "https://raw.githubusercontent.com/doctor-8trange/zyphora/refs/heads/main/data/sony.m3u",
    "https://raw.githubusercontent.com/drmlive/fancode-live-events/refs/heads/main/fancode.m3u",
    "https://raw.githubusercontent.com/srhady/willow-event/refs/heads/main/live_sports.m3u",
    "https://raw.githubusercontent.com/srhady/crichd-speical-live-event/refs/heads/main/playlist.m3u",
    "https://raw.githubusercontent.com/srhady/bingstream/refs/heads/main/playlist.m3u",
    "https://jhsevetns-fhd.rtxcric.workers.dev/playlist.m3u",
    "https://raw.githubusercontent.com/srhady/crichd-speical-live-event/refs/heads/main/Footy_Live.m3u",
    "https://raw.githubusercontent.com/srhady/willow-event/refs/heads/main/primevideo_sports.m3u"
]

OUTPUT = "Events_Premium.m3u"

events = {}

def quality_score(text):
    text = text.lower()
    if "2160" in text or "4k" in text:
        return 5
    if "1080" in text or "fhd" in text:
        return 4
    if "720" in text:
        return 3
    if "480" in text:
        return 2
    if "360" in text:
        return 1
    return 0

def category(name):
    n = name.lower()
    if any(x in n for x in ["ipl","cricket","odi","t20","test","bbl","cpl","psl","mavericks","kings","willow"]):
        return "🏏 Live Cricket"
    if any(x in n for x in ["football","fc","league","laliga","premier","uefa","champions","arsenal","barcelona","madrid","footy"]):
        return "⚽ Live Football"
    if "tennis" in n:
        return "🎾 Live Tennis"
    if any(x in n for x in ["nba","basketball"]):
        return "🏀 Live Basketball"
    return "📺 Other Live Events"

for source in SOURCES:
    try:
        text = requests.get(source, timeout=30).text
        lines = text.splitlines()

        i = 0
        while i < len(lines):
            line = lines[i].strip()

            if line.startswith("#EXTINF") and i + 1 < len(lines):
                extinf = line

                # FanCode fix
                extinf = extinf.replace("#EXTINF:-1, tvg-logo=", "#EXTINF:-1 tvg-logo=")

                name = extinf.split(",",1)[1].strip()

                stream = lines[i+1].strip()

                score = quality_score(extinf + stream)

                key = re.sub(r"\s+\(?(2160p|1080p|720p|480p|360p|fhd|hd)\)?","",name,flags=re.I)

                if key not in events or score > events[key]["score"]:
                    events[key] = {
                        "extinf": extinf,
                        "stream": stream,
                        "score": score,
                        "category": category(name),
                        "name": name
                    }

                i += 2
            else:
                i += 1

        print("Loaded:", source)

    except Exception as e:
        print("Failed:", source, e)

groups = {}

for e in events.values():
    groups.setdefault(e["category"], []).append(e)

for g in groups:
    groups[g].sort(key=lambda x: x["name"].lower())

order = [
    "🏏 Live Cricket",
    "⚽ Live Football",
    "🎾 Live Tennis",
    "🏀 Live Basketball",
    "📺 Other Live Events"
]

with open(OUTPUT,"w",encoding="utf-8") as f:

    f.write('#EXTM3U x-tvg-url="https://epgshare01.online/epgshare01/epg_ripper_ALL_SOURCES1.xml.gz"\n')

    for cat in order:
        if cat not in groups:
            continue

        f.write(f"\n#EXTINF:-1 group-title=\"════ {cat} ════\",{cat}\n")
        f.write("https://example.com/blank.ts\n")

        for e in groups[cat]:
            f.write(e["extinf"]+"\n")
            f.write(e["stream"]+"\n")

print("Created:",OUTPUT)
