from typing import Tuple
from obfuscation import detect_obfuscation

SUSPICIOUS_KEYWORDS = [
    "bomb",
    "exploit",
    "bypass",
    "password",
    "backdoor",
    "secret",
    "time bomb",
    "hack",
    "disable security",
]


def rule_based_check(prompt: str) -> Tuple[bool, float, str]:
    low = prompt.lower()
    score = 0.0
    reason = ""
    for kw in SUSPICIOUS_KEYWORDS:
        if kw in low:
            score += 0.6
            reason += f"keyword:{kw};"
    obf = detect_obfuscation(prompt)
    if obf["obf_score"] > 0:
        score += 0.5 * obf["obf_score"]
        reason += f"obf_flags:{','.join(obf['obf_flags'])};"
    blocked = score >= 0.8
    return blocked, min(score, 1.0), reason
