import json
from pathlib import Path

from embeddings import embed_text
from faiss_index import FaissIndex


def main():
    idx = FaissIndex()
    seeds_path = Path(__file__).resolve().parents[1] / "data" / "seeds" / "malicious_seeds.jsonl"
    with open(seeds_path) as f:
        for i, line in enumerate(f):
            j = json.loads(line)
            v = embed_text(j["prompt"])
            idx.add(v, f"mal_{i:04d}")
    print("Seeded index.")


if __name__ == "__main__":
    main()
