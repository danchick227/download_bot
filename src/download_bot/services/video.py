import asyncio
import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class VideoMetadata:
    duration: int | None
    width: int | None
    height: int | None


class VideoPreparationService:
    async def prepare(self, video_path: Path) -> tuple[Path, VideoMetadata]:
        metadata = await self._probe(video_path)
        if await self._is_telegram_compatible(video_path):
            return video_path, metadata

        prepared_path = video_path.with_name(f"{video_path.stem}.telegram.mp4")
        process = await asyncio.create_subprocess_exec(
            "ffmpeg",
            "-y",
            "-i",
            str(video_path),
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "aac",
            "-movflags",
            "+faststart",
            str(prepared_path),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        _, stderr = await process.communicate()

        if process.returncode != 0 or not prepared_path.exists():
            prepared_path.unlink(missing_ok=True)
            raise RuntimeError(
                f"ffmpeg не смог подготовить видео: {stderr.decode(errors='replace').strip()}"
            )

        video_path.unlink(missing_ok=True)
        return prepared_path, await self._probe(prepared_path)

    async def _probe(self, video_path: Path) -> VideoMetadata:
        process = await asyncio.create_subprocess_exec(
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "stream=codec_type,width,height,duration:format=format_name,duration",
            "-of",
            "json",
            str(video_path),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            raise RuntimeError(
                f"ffprobe не смог прочитать видео: {stderr.decode(errors='replace').strip()}"
            )

        try:
            data = json.loads(stdout)
            video_stream = next(
                stream for stream in data.get("streams", [])
                if stream.get("codec_type") == "video"
            )
            duration = float(data.get("format", {}).get("duration", video_stream.get("duration", 0)))
            return VideoMetadata(
                duration=max(1, round(duration)) if duration else None,
                width=video_stream.get("width"),
                height=video_stream.get("height"),
            )
        except (KeyError, StopIteration, TypeError, ValueError, json.JSONDecodeError) as error:
            raise RuntimeError("ffprobe вернул некорректные метаданные видео") from error

    async def _is_telegram_compatible(self, video_path: Path) -> bool:
        process = await asyncio.create_subprocess_exec(
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "stream=codec_type,codec_name,pix_fmt:format=format_name",
            "-of",
            "json",
            str(video_path),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, _ = await process.communicate()
        if process.returncode != 0:
            return False

        try:
            data = json.loads(stdout)
            streams = data.get("streams", [])
            video_stream = next(stream for stream in streams if stream.get("codec_type") == "video")
            audio_stream = next(stream for stream in streams if stream.get("codec_type") == "audio")
            format_names = data.get("format", {}).get("format_name", "").split(",")
        except (StopIteration, TypeError, json.JSONDecodeError):
            return False

        return (
            "mp4" in format_names
            and video_stream.get("codec_name") == "h264"
            and video_stream.get("pix_fmt") == "yuv420p"
            and audio_stream.get("codec_name") == "aac"
        )