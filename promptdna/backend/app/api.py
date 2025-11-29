from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from fingerprint import generate_dna
from classifier import rule_based_check
from forwarder import forward_prompt
from response_scanner import scan_response
from faiss_index import FaissIndex
from pymongo import MongoClient
from config import MONGO_URI, DB_NAME
import datetime

router = APIRouter()
faiss = FaissIndex()
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
events = db.events


class AnalyzeRequest(BaseModel):
    user_id: str
    prompt: str
    context: dict = {}


@router.post("/v1/analyze")
async def analyze(req: AnalyzeRequest):
    prompt = req.prompt
    dna = generate_dna(prompt)
    blocked, risk_score, reason = rule_based_check(prompt)

    D, ids = faiss.search(dna["embedding"], topk=5)
    similar = [{"id": i, "score": s} for i, s in zip(ids, D) if i is not None]

    decision = "allow"
    if blocked:
        decision = "block"
    elif risk_score > 0.6:
        decision = "warn"

    event = {
        "timestamp": datetime.datetime.utcnow(),
        "user_id": req.user_id,
        "prompt": prompt[:1000],
        "dna_hash": dna["dna_hash"],
        "genes": dna["genes"],
        "decision": decision,
        "risk_score": risk_score,
        "reasons": reason,
        "similar": similar,
    }
    events.insert_one(event)

    response_scan = None
    if decision == "allow":
        response = forward_prompt(prompt)
        response_scan = scan_response(response)
    elif decision == "warn":
        response = (
            "⚠️ Warning: This prompt looks suspicious. We sanitized the request. Proceed? "
            "(prototype sanitization)."
        )
    else:
        response = "⛔ Prompt blocked: suspicious or unsafe."

    if response_scan:
        event["response_scan"] = response_scan

    return {
        "decision": decision,
        "risk_score": risk_score,
        "reasons": reason,
        "similar": similar,
        "response": response,
        "response_scan": response_scan,
    }


@router.get("/v1/logs")
def get_logs(limit: int = 50):
    docs = list(events.find().sort("timestamp", -1).limit(limit))
    for d in docs:
        d["_id"] = str(d["_id"])
        d["timestamp"] = d["timestamp"].isoformat()
    return {"logs": docs}
