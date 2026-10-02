const DEFAULT_BASE_URL = "https://transcript-yt.com";

export class TranscriptYTError extends Error {
  constructor(message, { status, code, body } = {}) {
    super(message);
    this.name = "TranscriptYTError";
    this.status = status;
    this.code = code;
    this.body = body;
  }
}

export class TranscriptYT {
  constructor({ apiKey = globalThis.process?.env?.TRANSCRIPTYT_API_KEY, baseUrl = DEFAULT_BASE_URL, fetch: fetchImpl = globalThis.fetch } = {}) {
    if (!apiKey) throw new TranscriptYTError("Missing API key. Pass { apiKey } or set TRANSCRIPTYT_API_KEY.");
    this.apiKey = apiKey;
    this.baseUrl = baseUrl.replace(/\/$/, "");
    this.fetch = fetchImpl;
  }

  async #request(path, params = {}) {
    const url = new URL(this.baseUrl + path);
    for (const [name, value] of Object.entries(params)) {
      if (value !== undefined && value !== null) url.searchParams.set(name, String(value));
    }
    const res = await this.fetch(url, { headers: { Authorization: `Bearer ${this.apiKey}` } });
    if (res.ok) return res;

    let body;
    try {
      body = await res.json();
    } catch {
      body = undefined;
    }
    // 402 (out of credits) uses a flat shape; every other error uses { error: { code, message } }.
    const code = res.status === 402 ? "QUOTA_EXCEEDED" : body?.error?.code;
    const message = res.status === 402 ? "Out of credits" : body?.error?.message ?? `HTTP ${res.status}`;
    throw new TranscriptYTError(message, { status: res.status, code, body });
  }

  /**
   * Fetch a transcript. Returns parsed JSON for format "json" (default), otherwise the file body as a string.
   * @param {string} url YouTube URL or 11-character video ID
   */
  async getTranscript(url, { language, translateTo, format, includeSegments, timestamps, paragraphs } = {}) {
    const res = await this.#request("/v1/transcript", {
      url,
      language,
      translate_to: translateTo,
      format,
      includeSegments,
      timestamps,
      paragraphs,
    });
    return !format || format === "json" ? res.json() : res.text();
  }

  /** List a video's caption tracks. Free. */
  async listLanguages(url) {
    return (await this.#request("/v1/languages", { url })).json();
  }

  /** Plan and remaining credits. Free. */
  async getUsage() {
    return (await this.#request("/v1/usage")).json();
  }
}

export default TranscriptYT;
