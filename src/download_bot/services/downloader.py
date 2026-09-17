import asyncio
from pathlib import Path

import yt_dlp


class YouTubeDownloader:
    QUALITY_LIMITS = (720, 480, 360, 240)
    MAX_TELEGRAM_FILE_SIZE = 49 * 1024 * 1024

    def build_quality_candidates(self) -> list[str]:
        return [
            f"bestvideo[height<={height}]+bestaudio/best[height<={height}]/best"
            for height in self.QUALITY_LIMITS
        ]

    def _download(self, url: str, directory: Path, max_height: int | None = None) -> Path:
        limits = list(self.QUALITY_LIMITS)
        if max_height is not None:
            limits = [height for height in limits if height <= max_height]
            if not limits:
                limits = [max_height]

        last_error = None

        for height in limits:
            options: yt_dlp._Params = {
                "format": (
                    f"bestvideo[height<={height}][vcodec^=avc1]+"
                    f"bestaudio[acodec^=mp4a]/"
                    f"best[height<={height}][vcodec^=avc1][acodec^=mp4a]/"
                    f"bestvideo[height<={height}]+bestaudio/"
                    f"best[height<={height}]/best"
                ),
                "outtmpl": str(directory / "%(id)s.%(ext)s"),
                "merge_output_format": "mp4",
                "noplaylist": True,
                "quiet": True,
                "no_warnings": True,
            }

            try:
                with yt_dlp.YoutubeDL(options) as ydl:
                    info = ydl.extract_info(url, download=True)
                    path = Path(ydl.prepare_filename(info))

                    if path.exists() and path.stat().st_size > self.MAX_TELEGRAM_FILE_SIZE:
                        path.unlink(missing_ok=True)
                        continue

                    return path
            except Exception as error:  # pragma: no cover - depends on yt-dlp runtime
                last_error = error
                continue

        if last_error is not None:
            raise last_error

        raise ValueError("Не удалось скачать видео для переданного URL")

    async def download(self, url: str, directory: Path, max_height: int | None = None) -> Path:
        return await asyncio.to_thread(
            self._download,
            url,
            directory,
            max_height,
        )