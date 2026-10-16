"""OTP storage — uses in-memory dict when Redis is unavailable (demo mode)."""
import random
import time
from typing import Dict, Tuple

_store: Dict[str, Tuple[str, float]] = {}  # email -> (otp, expires_at)
TTL = 300


def generate_otp(email: str) -> str:
    otp = f"{random.randint(100000, 999999)}"
    _store[email] = (otp, time.time() + TTL)
    return otp


def verify_otp(email: str, otp: str) -> bool:
    entry = _store.get(email)
    if not entry:
        return False
    stored, expires = entry
    if time.time() > expires:
        _store.pop(email, None)
        return False
    if stored == otp:
        _store.pop(email, None)
        return True
    return False
