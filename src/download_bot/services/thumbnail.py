import asyncio
from pathlib import Path


class ThumbnailService:
    async def create(self, video_path: Path) -> Path:
        thumbnail_path = video_path.with_suffix(".jpg")

        last_error: RuntimeError | None = None
        for timestamp in ("1", "0"):
            process = await asyncio.create_subprocess_exec(
                "ffmpeg",
                "-y",
                "-ss",
                timestamp,
                "-i",
                str(video_path),
                "-frames:v",
                "1",
                "-vf",
                "scale=320:-2",
                "-q:v",
                "2",
                str(thumbnail_path),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            _, stderr = await process.communicate()

            if process.returncode == 0 and thumbnail_path.exists():
                return thumbnail_path

            last_error = RuntimeError(
                f"ffmpeg не смог создать thumbnail: {stderr.decode(errors='replace').strip()}"
            )
            thumbnail_path.unlink(missing_ok=True)

        if last_error is not None:
            raise last_error

        raise RuntimeError("Не удалось создать thumbnail")