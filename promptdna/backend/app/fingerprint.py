from utils import sha256_str
from obfuscation import detect_obfuscation
from embeddings import embed_text


def extract_genes(prompt: str) -> list:
    genes = []
    text = prompt.lower()
    if "story" in text or "poem" in text:
        genes.append("narrative_task")
    if "code" in text or "script" in text:
        genes.append("coding_task")
    if "first letter" in text or "acrostic" in text:
        genes.append("acrostic_hint")
    obf = detect_obfuscation(prompt)
    for f in obf["obf_flags"]:
        genes.append(f)
    return genes


def generate_dna(prompt: str) -> dict:
    genes = sorted(list(set(extract_genes(prompt))))
    emb = embed_text(prompt).tolist()
    base = "|".join(genes) + "|" + prompt[:100]
    dna_hash = sha256_str(base)
    return {"dna_hash": dna_hash, "genes": genes, "embedding": emb}
