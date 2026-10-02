# Installing the TranscriptYT MCP server

TranscriptYT is a **remote** MCP server. There is nothing to clone, build, or run locally: the client connects to a hosted Streamable HTTP endpoint with an API key header.

- Endpoint: `https://transcript-yt.com/mcp`
- Transport: Streamable HTTP
- Auth: header `Authorization: Bearer <API key>`

## 1. Get an API key

Ask the user for their TranscriptYT API key (it starts with `ts_live_`). If they don't have one, they can create one for free (100 transcripts, no card) at https://transcript-yt.com/dashboard/keys after signing in with Google.

## 2. Add the server

### Cline

Add this to `cline_mcp_settings.json`, replacing the key:

```json
{
  "mcpServers": {
    "transcriptyt": {
      "type": "streamableHttp",
      "url": "https://transcript-yt.com/mcp",
      "headers": { "Authorization": "Bearer ts_live_..." },
      "disabled": false
    }
  }
}
```

### Claude Code

```bash
claude mcp add --transport http transcriptyt https://transcript-yt.com/mcp \
  --header "Authorization: Bearer ts_live_..."
```

### Cursor (`.cursor/mcp.json`) and other `mcpServers` JSON clients

```json
{
  "mcpServers": {
    "transcriptyt": {
      "url": "https://transcript-yt.com/mcp",
      "headers": { "Authorization": "Bearer ts_live_..." }
    }
  }
}
```

More clients (VS Code, Codex, Claude Desktop): https://transcript-yt.com/docs#mcp

## 3. Verify

Call `get_usage`. It is free and returns the plan and remaining credits. A "Missing API key" tool error means the header is not being sent; an HTTP 401 means the key is invalid.

## Tools

- `get_transcript`: transcript of a public YouTube video by URL or 11-character ID. Optional `language`, `translate_to` (150+ languages), `format` (`md` default, `text`, `json`, `srt`, `vtt`, `csv`), `timestamps`. 1 credit; videos without captions are AI-transcribed at 1 credit per started 3 minutes.
- `list_languages`: caption tracks available for a video. Free.
- `get_usage`: remaining credits and plan. Free.
