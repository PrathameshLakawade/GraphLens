"""Schemas for transcript APIs."""

from pydantic import BaseModel, Field, HttpUrl


class TranscriptRequest(BaseModel):
    url: HttpUrl
    model: str = Field(default="base", description="Whisper model name.")
    language: str | None = Field(
        default=None,
        description="Optional language override, e.g. 'en'.",
    )


class TranscriptSegment(BaseModel):
    start_seconds: float
    end_seconds: float
    text: str


class TranscriptResponse(BaseModel):
    source_url: HttpUrl
    title: str
    duration_seconds: int | None = None
    language: str | None = None
    model: str
    segment_count: int
    segments: list[TranscriptSegment]
