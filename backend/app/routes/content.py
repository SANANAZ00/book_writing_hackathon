from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def content_root():
    return {"message": "Content API endpoint"}