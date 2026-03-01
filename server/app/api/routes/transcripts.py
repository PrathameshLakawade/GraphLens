"""Transcript routes."""

from fastapi import APIRouter, HTTPException, status

from server.app.schemas.transcripts import TranscriptRequest, TranscriptResponse
from server.app.services.transcript_service import transcribe_youtube_video

router = APIRouter()


@router.post(
    "/transcripts/youtube",
    response_model=TranscriptResponse,
    status_code=status.HTTP_200_OK,
)
def create_youtube_transcript(payload: TranscriptRequest) -> TranscriptResponse:
    try:
        transcript = transcribe_youtube_video(
            url=str(payload.url),
            model_name=payload.model,
            language=payload.language,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        ) from exc

    return TranscriptResponse(**transcript)
