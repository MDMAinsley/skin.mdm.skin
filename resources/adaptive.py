"""Pure conservative home recommendation; no account, network or Kodi writes."""
import math
import re


def memory_mb(label):
    if not isinstance(label, str):
        return None
    match = re.fullmatch(r"\s*([0-9]+(?:\.[0-9]+)?)\s*(MB|MiB|GB|GiB)?\s*", label, re.I)
    if not match:
        return None
    value = float(match[1]) * (1024 if (match[2] or "").lower() in ("gb", "gib") else 1)
    return value if math.isfinite(value) and value > 0 else None


def recommend(memory, free_bytes, light=False):
    known_storage = type(free_bytes) in (int, float) and math.isfinite(free_bytes) and free_bytes >= 0
    if light:
        return False, "Flix has the Light artwork preference"
    if memory is None or not known_storage:
        return False, "Memory or available storage is unknown"
    if memory <= 2048:
        return False, "Total memory is 2 GiB or less"
    if free_bytes <= 512 * 1024 * 1024:
        return False, "Available userdata storage is 512 MiB or less"
    return True, "Memory and available storage support the artwork recommendation"
