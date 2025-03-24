from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get("/")
async def get_kitespots():
    # Placeholder route - replace with your actual implementation
    return [{"id": "1", "name": "Example Kitespot"}]