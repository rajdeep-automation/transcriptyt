# transcriptyt

JavaScript/TypeScript client for the [TranscriptYT YouTube Transcript API](https://transcript-yt.com). Zero dependencies; works in Node.js 18+, Bun, Deno, and edge runtimes.

```bash
npm install transcriptyt
```

```js
import { TranscriptYT, TranscriptYTError } from "transcriptyt";

const client = new TranscriptYT({ apiKey: process.env.TRANSCRIPTYT_API_KEY });

// Timestamped JSON (default)
const t = await client.getTranscript("https://youtu.be/dQw4w9WgXcQ");
t.segments; // [{ start, duration, text }, ...]

// Files: "text" | "srt" | "vtt" | "csv" | "md" return a string
const srt = await client.getTranscript("dQw4w9WgXcQ", { format: "srt" });

// Translate (150+ languages), merge cues into paragraphs, add timestamps
const md = await client.getTranscript("dQw4w9WgXcQ", { translateTo: "es", format: "md", paragraphs: true, timestamps: true });

// Free calls
await client.listLanguages("dQw4w9WgXcQ");
await client.getUsage();

try {
  await client.getTranscript("not-a-video");
} catch (e) {
  if (e instanceof TranscriptYTError) console.log(e.status, e.code, e.message);
}
```

Get a free API key (100 transcripts) at [transcript-yt.com](https://transcript-yt.com/login). Docs: [transcript-yt.com/docs](https://transcript-yt.com/docs).
