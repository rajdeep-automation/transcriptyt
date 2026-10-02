"""Summarize a YouTube video with Claude.

pip install transcriptyt anthropic
export TRANSCRIPTYT_API_KEY=ts_live_... ANTHROPIC_API_KEY=...
python summarize.py https://youtu.be/dQw4w9WgXcQ
"""

import sys

import anthropic
from transcriptyt import TranscriptYT

transcript = TranscriptYT().get_transcript(sys.argv[1], format="md", paragraphs=True, timestamps=True)

message = anthropic.Anthropic().messages.create(
    model="claude-sonnet-5",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": "Summarize this YouTube transcript in 5 bullet points, each with the [HH:MM:SS] "
                   "timestamp where it is discussed.\n\n" + transcript,
    }],
)
print(message.content[0].text)
