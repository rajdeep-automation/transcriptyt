"""YouTube Transcript API client for https://transcript-yt.com."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Optional

__all__ = ["TranscriptYT", "TranscriptYTError"]
__version__ = "1.0.0"

DEFAULT_BASE_URL = "https://transcript-yt.com"


class TranscriptYTError(Exception):
    """Raised for any non-2xx response. `code` is the API error code, e.g. NO_CAPTIONS."""

    def __init__(self, message: str, status: Optional[int] = None, code: Optional[str] = None, body: Any = None):
        super().__init__(message)
        self.status = status
        self.code = code
        self.body = body


class TranscriptYT:
    def __init__(self, api_key: Optional[str] = None, base_url: str = DEFAULT_BASE_URL, timeout: float = 300):
        self.api_key = api_key or os.environ.get("TRANSCRIPTYT_API_KEY")
        if not self.api_key:
            raise TranscriptYTError("Missing API key. Pass api_key= or set TRANSCRIPTYT_API_KEY.")
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def _request(self, path: str, params: Optional[dict] = None) -> tuple[str, str]:
        query = {
            k: (str(v).lower() if isinstance(v, bool) else str(v))
            for k, v in (params or {}).items()
            if v is not None
        }
        url = f"{self.base_url}{path}"
        if query:
            url += "?" + urllib.parse.urlencode(query)
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {self.api_key}", "User-Agent": f"transcriptyt-python/{__version__}"})
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as res:
                return res.read().decode("utf-8"), res.headers.get("Content-Type", "")
        except urllib.error.HTTPError as e:
            raw = e.read().decode("utf-8", errors="replace")
            try:
                body = json.loads(raw)
            except ValueError:
                body = raw
            # 402 (out of credits) uses a flat shape; every other error uses {"error": {"code", "message"}}.
            if e.code == 402:
                raise TranscriptYTError("Out of credits", e.code, "QUOTA_EXCEEDED", body) from None
            err = body.get("error", {}) if isinstance(body, dict) else {}
            raise TranscriptYTError(err.get("message") or f"HTTP {e.code}", e.code, err.get("code"), body) from None

    def get_transcript(
        self,
        url: str,
        *,
        language: Optional[str] = None,
        translate_to: Optional[str] = None,
        format: Optional[str] = None,
        include_segments: Optional[bool] = None,
        timestamps: Optional[bool] = None,
        paragraphs: Optional[bool] = None,
    ) -> Any:
        """Return a dict for format "json" (default), otherwise the file body as a string.

        format: json, text, srt, vtt, csv, or md.
        """
        body, _ = self._request(
            "/v1/transcript",
            {
                "url": url,
                "language": language,
                "translate_to": translate_to,
                "format": format,
                "includeSegments": include_segments,
                "timestamps": timestamps,
                "paragraphs": paragraphs,
            },
        )
        return json.loads(body) if format in (None, "json") else body

    def list_languages(self, url: str) -> dict:
        """List a video's caption tracks. Free."""
        return json.loads(self._request("/v1/languages", {"url": url})[0])

    def get_usage(self) -> dict:
        """Plan and remaining credits. Free."""
        return json.loads(self._request("/v1/usage")[0])
