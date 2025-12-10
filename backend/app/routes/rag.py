from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def rag_root():
    return {"message": "RAG API endpoint"}