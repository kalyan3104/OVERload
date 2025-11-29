from typing import Dict, List
import re
from obfuscation import detect_obfuscation

LEAK_PATTERNS = [
    re.compile(r"api[_-]?key", re.IGNORECASE),
    re.compile(r"password", re.IGNORECASE),
    re.compile(r"private\s+key", re.IGNORECASE),
    re.compile(r"ssh-rsa", re.IGNORECASE),
    re.compile(r"BEGIN [A-Z ]+PRIVATE KEY"),
]

MISUSE_KEYWORDS = [
    "disable security",
    "backdoor",
    "exploit",
    "weapon",
    "harm",
    "attack",
]


def _check_patterns(text: str) -> List[str]:
    matches = []
    for pattern in LEAK_PATTERNS:
        if pattern.search(text):
            matches.append(pattern.pattern)
    for keyword in MISUSE_KEYWORDS:
        if keyword in text.lower():
            matches.append(f"keyword:{keyword}")
    return matches


def scan_response(text: str) -> Dict:
    if not text:
        return {"risk": 0.0, "flags": [], "notes": []}

    flags = []
    notes = []
    risk = 0.0

    patterns = _check_patterns(text)
    if patterns:
        flags.append("potential_leak")
        notes.extend(patterns)
        risk += 0.4

    obf = detect_obfuscation(text)
    if obf["obf_flags"]:
        flags.append("response_obfuscation")
        notes.append(f"obf:{','.join(obf['obf_flags'])}")
        risk += 0.2 * len(obf["obf_flags"])

    risk = min(risk, 1.0)
    return {"risk": risk, "flags": list(set(flags)), "notes": notes}
