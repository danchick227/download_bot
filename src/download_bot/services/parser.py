import re

YOUTUBE_RE = re.compile(
    r"https?://(?:www\.)?"
    r"(?:youtube\.com/watch\?v=|youtu\.be/)"
    r"[A-Za-z0-9_-]{11}"
)

def extract_youtube_url(text: str) -> str | None:
    match = YOUTUBE_RE.search(text)

    if match is None:
        return None

    return match.group(0)