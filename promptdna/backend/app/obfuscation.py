import re
import base64
import codecs

ZERO_WIDTH_RE = re.compile(r'[\u200B-\u200D\uFEFF]')
BASE64_RE = re.compile(r'^[A-Za-z0-9+/=]+\Z')

def has_zero_width(text: str) -> bool:
    return bool(ZERO_WIDTH_RE.search(text))


def looks_like_base64(s: str) -> bool:
    s_clean = s.strip()
    if len(s_clean) < 12:
        return False
    try:
        if not BASE64_RE.match(s_clean):
            return False
        base64.b64decode(s_clean, validate=True)
        return True
    except Exception:
        return False


def has_rot13_hint(text: str) -> bool:
    hints = [
        "rot13",
        "decode",
        "first letter",
        "first character",
        "acrostic",
        "hidden",
        "secret",
        "encode",
    ]
    t = text.lower()
    return any(h in t for h in hints)


def detect_obfuscation(text: str) -> dict:
    flags = []
    if has_zero_width(text):
        flags.append("zero_width")
    if looks_like_base64(text):
        flags.append("base64")
    if has_rot13_hint(text):
        flags.append("obfuscation_hint")
    return {"obf_flags": flags, "obf_score": len(flags)}
