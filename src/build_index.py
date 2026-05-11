import json
import pickle
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


DATA_FILE = Path("data/manual_fragments.jsonl")
INDEX_FILE = Path("data/hnsw_index.faiss")
METADATA_FILE = Path("data/hnsw_metadata.pkl")

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# HNSW
HNSW_M = 32
HNSW_EF_CONSTRUCTION = 200


def load_jsonl(file_path: Path) -> list[dict]:
    records = []
    with file_path.open("r", encoding="utf-8") as f:
        for line in f:
            records.append(json.loads(line))
    return records


def main() -> None:
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {DATA_FILE}")

    documents = load_jsonl(DATA_FILE)

    
    texts = [doc["text"] for doc in documents]

    print("Carregando modelo de embedding...")
    model = SentenceTransformer(EMBEDDING_MODEL)

    print("Gerando embeddings...")
    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=True,
    )

    dimension = embeddings.shape[1]
    print(f"Dimensão dos vetores: {dimension}")

    print("Criando índice HNSW...")
    index = faiss.IndexHNSWFlat(dimension, HNSW_M, faiss.METRIC_INNER_PRODUCT)
    index.hnsw.efConstruction = HNSW_EF_CONSTRUCTION

    index.add(embeddings.astype(np.float32))

    print("Salvando índice...")
    faiss.write_index(index, str(INDEX_FILE))

    print("Salvando metadados...")
    with METADATA_FILE.open("wb") as f:
        pickle.dump(documents, f)

    print(f"Total de documentos indexados: {len(documents)}")
    print(f"Índice salvo em: {INDEX_FILE.resolve()}")
    print(f"Metadados salvos em: {METADATA_FILE.resolve()}")


if __name__ == "__main__":
    main()