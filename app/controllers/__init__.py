import logging

from fastapi import APIRouter


logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/ping")
async def ping():
    """Create a new flow"""
    return 'hi'