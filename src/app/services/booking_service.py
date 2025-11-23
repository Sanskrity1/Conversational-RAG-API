from typing import Dict, Any
import uuid
import datetime

class BookingService:
    async def create_booking(self, memory, name: str, email: str, datetime_iso: str, notes: str = None) -> Dict[str, Any]:
        booking_id = str(uuid.uuid4())
        now = datetime.datetime.utcnow().isoformat()
        payload = {
            "id": booking_id,
            "name": name,
            "email": email,
            "datetime_iso": datetime_iso,
            "notes": notes,
            "created_at": now,
        }
        await memory.create_booking(booking_id, payload)
        return payload
