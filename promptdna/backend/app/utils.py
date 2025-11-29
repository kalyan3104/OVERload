import hashlib
import json


def sha256_str(s: str) -> str:
    return hashlib.sha256(s.encode('utf-8')).hexdigest()


def pretty_json(o):
    return json.dumps(o, indent=2, ensure_ascii=False)
