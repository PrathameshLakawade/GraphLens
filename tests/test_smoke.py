from graphlens.pipelines.rag import answer_query
from server.app.services.rag_service import answer_user_query
from server.app.services.transcript_service import _build_transcript_payload
from server.app.schemas.transcripts import TranscriptRequest


def test_answer_query_returns_text() -> None:
    result = answer_query("test query")
    assert "test query" in result


def test_rag_service_returns_text() -> None:
    result = answer_user_query("service query")
    assert "service query" in result


def test_build_transcript_payload_formats_response() -> None:
    payload = _build_transcript_payload(
        url="https://www.youtube.com/watch?v=abc123",
        model_name="base",
        metadata={"title": "Example", "duration": 42},
        result={
            "text": " transcript text ",
            "language": "en",
            "segments": [
                {"id": 1, "start": 0.0, "end": 1.5, "text": " hello "},
                {"id": 2, "start": 1.5, "end": 3.0, "text": " world "},
            ],
        },
    )
    assert payload["title"] == "Example"
    assert payload["segment_count"] == 2
    assert payload["segments"][0] == {
        "start_seconds": 0.0,
        "end_seconds": 1.5,
        "text": "hello",
    }
    assert payload["segments"][1] == {
        "start_seconds": 1.5,
        "end_seconds": 3.0,
        "text": "world",
    }


def test_transcript_request_url_can_be_converted_to_string() -> None:
    payload = TranscriptRequest(url="https://www.youtube.com/watch?v=abc123")
    assert str(payload.url) == "https://www.youtube.com/watch?v=abc123"
