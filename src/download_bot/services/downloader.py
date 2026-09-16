import asyncio
from pathlib import Path

import yt_dlp


class YouTubeDownloader:
    def _download(self, url: str, directory: Path) -> Path:
        options: yt_dlp._Params = {
            "format": "bv*+ba/b",
            "outtmpl": str(directory / "%(id)s.%(ext)s"),
            "merge_output_format": "mp4",
            "noplaylist": True,
            "quiet": True,
            "no_warnings": True,
        }

        with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=True)
            return Path(ydl.prepare_filename(info))

    async def download(self, url: str, directory: Path) -> Path:
        return await asyncio.to_thread(
            self._download,
            url,
            directory,
        )