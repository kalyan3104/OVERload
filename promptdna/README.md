# PromptDNA Prototype

PromptDNA is a middleware layer that fingerprints, classifies, and optionally forwards user prompts to a downstream LLM. This prototype includes:

- FastAPI backend with obfuscation detection, embedding fingerprinting, FAISS similarity search, Mongo logging, and LLM forwarding stub.
- React frontend to submit prompts and inspect recent decisions.
- MongoDB for storage and docker-compose stack for local dev.

Architecture diagram reference: `/mnt/data/A_digital_flowchart_depicts_the_architecture_of_a_.png` (copy to `docs/architecture.png` if you want it inside the repo).

## Quick start (Docker)

```bash
cd infra
docker-compose up --build
```

Then open:
- API docs: http://localhost:8000/docs
- Frontend: http://localhost:3000

## Local backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

## Seeding FAISS index

```bash
cd backend
python seed_index.py
```

## Safety

This is a prototype for research/testing only. Add authentication, rate limiting, full monitoring, and a trained classifier before production. Keep malicious prompt datasets sanitized and handled ethically.
