# transcriptyt

Python client for the [TranscriptYT YouTube Transcript API](https://transcript-yt.com). No dependencies; Python 3.8+.

```bash
pip install transcriptyt
```

```python
from transcriptyt import TranscriptYT, TranscriptYTError

client = TranscriptYT(api_key="ts_live_...")  # or set TRANSCRIPTYT_API_KEY

# Timestamped JSON (default)
t = client.get_transcript("https://youtu.be/dQw4w9WgXcQ")
t["segments"]  # [{"start", "duration", "text"}, ...]

# Files: text, srt, vtt, csv, md return a string
srt = client.get_transcript("dQw4w9WgXcQ", format="srt")

# Translate (150+ languages), merge cues into paragraphs, add timestamps
md = client.get_transcript("dQw4w9WgXcQ", translate_to="es", format="md", paragraphs=True, timestamps=True)

# Free calls
client.list_languages("dQw4w9WgXcQ")
client.get_usage()

try:
    client.get_transcript("not-a-video")
except TranscriptYTError as e:
    print(e.status, e.code, e)
```

Get a free API key (100 transcripts) at [transcript-yt.com](https://transcript-yt.com/login). Docs: [transcript-yt.com/docs](https://transcript-yt.com/docs).
