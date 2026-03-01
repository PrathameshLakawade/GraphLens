"""Service layer for YouTube transcription."""

from __future__ import annotations

from pathlib import Path
import sys
from tempfile import TemporaryDirectory
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[3]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))


def _load_dependencies() -> tuple[Any, Any]:
    try:
        import whisper
        import yt_dlp
    except ImportError as exc:
        raise RuntimeError(
            "Missing transcription dependencies. Install with `pip install -e .`."
        ) from exc

    return whisper, yt_dlp


def _download_audio(url: str, download_dir: Path, yt_dlp_module: Any) -> tuple[dict[str, Any], Path]:
    options = {
        "format": "bestaudio/best",
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
        "outtmpl": str(download_dir / "%(id)s.%(ext)s"),
    }

    with yt_dlp_module.YoutubeDL(options) as downloader:
        info = downloader.extract_info(url, download=True)
        if info is None:
            raise RuntimeError("yt-dlp did not return any video metadata.")

        filename = downloader.prepare_filename(info)

    audio_path = Path(filename)
    if not audio_path.exists():
        raise RuntimeError("Downloaded audio file could not be found.")

    return info, audio_path


def _build_transcript_payload(
    url: str,
    model_name: str,
    metadata: dict[str, Any],
    result: dict[str, Any],
) -> dict[str, Any]:
    raw_segments = result.get("segments") or []
    segments = [
        {
            "start_seconds": segment.get("start", 0.0),
            "end_seconds": segment.get("end", 0.0),
            "text": (segment.get("text") or "").strip(),
        }
        for segment in raw_segments
    ]

    return {
        "source_url": url,
        "title": metadata.get("title") or "Unknown title",
        "duration_seconds": metadata.get("duration"),
        "language": result.get("language"),
        "model": model_name,
        "segment_count": len(segments),
        "segments": segments,
    }


def transcribe_youtube_video(
    url: str,
    model_name: str = "base",
    language: str | None = None,
) -> dict[str, Any]:
    if "youtube.com/" not in url and "youtu.be/" not in url:
        raise ValueError("Only YouTube URLs are supported.")

    whisper_module, yt_dlp_module = _load_dependencies()

    try:
        with TemporaryDirectory() as temp_dir:
            metadata, audio_path = _download_audio(url, Path(temp_dir), yt_dlp_module)
            model = whisper_module.load_model(model_name)
            result = model.transcribe(str(audio_path), language=language)
    except ValueError:
        raise
    except Exception as exc:
        raise RuntimeError(f"Transcription failed: {exc}") from exc

    return _build_transcript_payload(url, model_name, metadata, result)
