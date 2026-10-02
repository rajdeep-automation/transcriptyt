// Save SRT subtitles for a list of YouTube videos.
// npm install transcriptyt
// TRANSCRIPTYT_API_KEY=ts_live_... node download_subtitles.mjs dQw4w9WgXcQ https://youtu.be/9bZkp7q19f0
import { writeFile } from "node:fs/promises";
import { TranscriptYT, TranscriptYTError } from "transcriptyt";

const client = new TranscriptYT();
const idOf = (video) => video.match(/(?:v=|youtu\.be\/|shorts\/|embed\/)([\w-]{11})/)?.[1] ?? video;

for (const video of process.argv.slice(2)) {
  try {
    const srt = await client.getTranscript(video, { format: "srt" });
    await writeFile(`${idOf(video)}.srt`, srt);
    console.log(`saved ${idOf(video)}.srt`);
  } catch (e) {
    if (!(e instanceof TranscriptYTError)) throw e;
    console.error(`${video}: ${e.code} ${e.message}`);
  }
}
