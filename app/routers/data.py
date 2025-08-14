from fastapi import APIRouter, HTTPException
from typing import List, Optional
from datetime import datetime

router = APIRouter(tags=["data"])

@router.get("/teams")
async def get_teams(league: Optional[str] = None):
    return {"message": "Teams endpoint"}

@router.get("/leagues")
async def get_leagues():
    return {"message": "Leagues endpoint"}

@router.get("/matches")
async def get_matches(
    team: Optional[str] = None,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    limit: int = 100
):
    return {"message": "Matches endpoint"}

@router.post("/data/refresh")
async def refresh_data():
    return {"message": "Data refresh triggered"}