"""Query routes."""

from fastapi import APIRouter

from server.app.schemas.query import QueryRequest, QueryResponse
from server.app.services.rag_service import answer_user_query

router = APIRouter()


@router.post("/query", response_model=QueryResponse)
def query(payload: QueryRequest) -> QueryResponse:
    return QueryResponse(answer=answer_user_query(payload.query))
