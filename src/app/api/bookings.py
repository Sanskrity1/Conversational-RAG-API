from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

from app.services.booking_service import BookingService

router = APIRouter()
booking_service = BookingService()


class BookingRequest(BaseModel):
    name: str
    email: EmailStr
    date: str  # ISO date/time string
    time: str  # ISO time or combined datetime
    notes: Optional[str] = None


@router.post("/", status_code=201)
async def create_booking(req: BookingRequest, request: Request):
    memory = request.app.state.memory
    # basic validation & parse
    try:
        dt = datetime.fromisoformat(f"{req.date}T{req.time}")
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Invalid date/time format: {exc}")

    booking = await booking_service.create_booking(memory=memory, name=req.name, email=req.email, datetime_iso=dt.isoformat(), notes=req.notes)
    return {"status": "ok", "booking_id": booking["id"], "booking": booking}
