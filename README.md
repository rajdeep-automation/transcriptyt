# TranscriptYT: YouTube Transcript API clients and examples

Official JavaScript and Python clients for the [TranscriptYT YouTube Transcript API](https://transcript-yt.com), plus examples.

Get the transcript of any public YouTube video as timestamped JSON, plain text, SRT, VTT, CSV, or Markdown, in 150+ languages. Videos without captions are transcribed with AI. Free tier: 100 transcripts, no card. [Get an API key →](https://transcript-yt.com/login)

- [API docs](https://transcript-yt.com/docs) · [OpenAPI spec](https://transcript-yt.com/openapi.json) · [Pricing](https://transcript-yt.com/#pricing)
- [MCP server](https://transcript-yt.com/docs#mcp) for Claude Code, Claude Desktop, Cursor, Codex, and VS Code
- [Free web tool](https://transcript-yt.com/youtube-transcript) (no code)

## JavaScript / TypeScript

```bash
npm install transcriptyt
```

```js
import { TranscriptYT } from "transcriptyt";

const client = new TranscriptYT({ apiKey: process.env.TRANSCRIPTYT_API_KEY });
const transcript = await client.getTranscript("https://youtu.be/dQw4w9WgXcQ");
console.log(transcript.title, transcript.segments.length);

const srt = await client.getTranscript("dQw4w9WgXcQ", { format: "srt" });
```

See [js/README.md](js/README.md).

## Python

```bash
pip install transcriptyt
```

```python
from transcriptyt import TranscriptYT

client = TranscriptYT()  # reads TRANSCRIPTYT_API_KEY
transcript = client.get_transcript("https://youtu.be/dQw4w9WgXcQ")
print(transcript["title"], len(transcript["segments"]))

srt = client.get_transcript("dQw4w9WgXcQ", format="srt")
```

See [python/README.md](python/README.md).

## cURL

```bash
curl "https://transcript-yt.com/v1/transcript?url=dQw4w9WgXcQ&format=text" \
  -H "Authorization: Bearer $TRANSCRIPTYT_API_KEY"
```

## Use it from an AI agent (MCP)

```bash
claude mcp add --transport http transcriptyt https://transcript-yt.com/mcp \
  --header "Authorization: Bearer $TRANSCRIPTYT_API_KEY"
```

Then paste a YouTube link into the chat. Setup for other clients: [docs](https://transcript-yt.com/docs#mcp). Also on the [official MCP Registry](https://registry.modelcontextprotocol.io/v0/servers?search=transcriptyt) as `io.github.rajdeep-automation/transcriptyt`.

## Examples

- [examples/summarize.py](examples/summarize.py): summarize a video with Claude
- [examples/rag_langchain.py](examples/rag_langchain.py): load videos into LangChain documents with timestamp links
- [examples/download_subtitles.mjs](examples/download_subtitles.mjs): save SRT files for a list of videos

## Errors

Errors raise `TranscriptYTError` with `status` and `code`. Retry `BLOCKED`, `RATE_LIMITED`, and `UPSTREAM_ERROR` with backoff; `VIDEO_UNAVAILABLE`, `NO_CAPTIONS`, and `LANGUAGE_NOT_AVAILABLE` are final; `QUOTA_EXCEEDED` (HTTP 402) means you're out of credits. Failed requests are never billed. [Full list](https://transcript-yt.com/docs#errors).

## License

MIT
