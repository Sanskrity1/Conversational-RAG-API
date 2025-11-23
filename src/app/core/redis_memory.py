from typing import List, Dict, Optional
import redis.asyncio as _aioredis
import json
import os
import asyncio

import redis.asyncio as redis_async

class RedisMemory:
    """
    Redis-backed conversational memory and booking storage.
    - messages stored as LPUSH lists per conversation key
    - bookings stored as Redis hashes with a UUID id
    """

    def __init__(self, redis_url: str = "redis://localhost:6379/0"):
        self._redis_url = redis_url
        self._r: Optional[redis_async.Redis] = None

    async def _get(self):
        if self._r is None:
            self._r = redis_async.from_url(self._redis_url, decode_responses=True)
        return self._r

    async def append_message(self, convo_key: str, message: Dict[str, str]):
        r = await self._get()
        await r.rpush(convo_key, json.dumps(message))

    async def get_messages(self, convo_key: str, limit: int = 10) -> List[Dict]:
        r = await self._get()
        raw = await r.lrange(convo_key, max(0, -limit), -1)
        res = []
        for j in raw:
            try:
                res.append(json.loads(j))
            except:
                continue
        return res

    async def create_booking(self, booking_id: str, payload: Dict):
        r = await self._get()
        key = f"booking:{booking_id}"
        await r.hset(key, mapping={k: json.dumps(v) for k, v in payload.items()})
        await r.sadd("bookings:index", booking_id)

    async def get_booking(self, booking_id: str) -> Optional[Dict]:
        r = await self._get()
        key = f"booking:{booking_id}"
        res = await r.hgetall(key)
        if not res:
            return None
        out = {k: json.loads(v) for k, v in res.items()}
        return out

    async def list_bookings(self) -> List[Dict]:
        r = await self._get()
        ids = await r.smembers("bookings:index")
        out = []
        for i in ids:
            b = await self.get_booking(i)
            if b:
                out.append(b)
        return out

    async def close(self):
        if self._r:
            await self._r.close()
            self._r = None
