import json
import pickle
from pathlib import Path
import os

import faiss
import numpy as np
from google import genai
from sentence_transformers import SentenceTransformer, CrossEncoder


INDEX_FILE = Path("data/hnsw_index.faiss")
METADATA_FILE = Path("data/hnsw_metadata.pkl")

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
CROSS_ENCODER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"


def generate_hyde_document(query: str) -> str:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("A variável de ambiente GEMINI_API_KEY não foi encontrada.")

    client = genai.Client(api_key=api_key)

    prompt = f"""
Você é um assistente especialista em análise forense digital.

Receba uma pergunta coloquial e vaga de um usuário e produza um pequeno
documento hipotético técnico, como se fosse um trecho de manual pericial.

A saída deve:
- usar jargão técnico de perícia forense digital
- ter entre 3 e 6 linhas
- não responder diretamente ao usuário
- servir como ponte semântica para busca vetorial
- estar em português do Brasil

Pergunta do usuário:
{query}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    return response.text.strip()


def load_metadata(file_path: Path) -> list[dict]:
    with file_path.open("rb") as f:
        return pickle.load(f)


def search_hnsw(index, query_vector: np.ndarray, metadata: list[dict], top_k: int = 10) -> list[dict]:
    distances, indices = index.search(query_vector.astype(np.float32), top_k)

    results = []
    for score, idx in zip(distances[0], indices[0]):
        if idx == -1:
            continue

        doc = metadata[idx]
        results.append(
            {
                "id": doc["id"],
                "title": doc["title"],
                "text": doc["text"],
                "score": float(score),
            }
        )

    return results


def rerank_documents(query: str, documents: list[dict], cross_encoder) -> list[dict]:
    pairs = [(query, doc["text"]) for doc in documents]
    scores = cross_encoder.predict(pairs)

    reranked = []
    for doc, score in zip(documents, scores):
        new_doc = doc.copy()
        new_doc["rerank_score"] = float(score)
        reranked.append(new_doc)

    reranked.sort(key=lambda x: x["rerank_score"], reverse=True)
    return reranked


def main() -> None:
    if not INDEX_FILE.exists():
        raise FileNotFoundError(f"Índice não encontrado: {INDEX_FILE}")

    if not METADATA_FILE.exists():
        raise FileNotFoundError(f"Metadados não encontrados: {METADATA_FILE}")

    query = "apagaram uns arquivos e eu quero saber se ainda dá pra recuperar"

    print("=== QUERY ORIGINAL ===")
    print(query)

    print("\nCarregando índice e metadados...")
    index = faiss.read_index(str(INDEX_FILE))
    metadata = load_metadata(METADATA_FILE)

    print("Carregando modelo de embedding...")
    embedding_model = SentenceTransformer(EMBEDDING_MODEL)

    print("Gerando documento hipotético com HyDE...")
    hyde_document = generate_hyde_document(query)

    print("\n=== DOCUMENTO HIPOTÉTICO (HyDE) ===")
    print(hyde_document)

    print("\nGerando embedding do documento hipotético...")
    hyde_vector = embedding_model.encode(
        [hyde_document],
        convert_to_numpy=True,
        normalize_embeddings=True,
    )

    print("Buscando Top-10 no índice HNSW...")
    retrieved_docs = search_hnsw(index, hyde_vector, metadata, top_k=10)

    print("\n=== TOP-10 RECUPERADOS (BUSCA RÁPIDA) ===")
    for i, doc in enumerate(retrieved_docs, start=1):
        print(f"\n[{i}] {doc['title']} | score={doc['score']:.4f}")
        print(doc["text"])

    print("\nCarregando Cross-Encoder para reranking...")
    cross_encoder = CrossEncoder(CROSS_ENCODER_MODEL)

    reranked_docs = rerank_documents(query, retrieved_docs, cross_encoder)

    print("\n=== TOP-3 FINAIS (APÓS RERANKING) ===")
    for i, doc in enumerate(reranked_docs[:3], start=1):
        print(f"\n[{i}] {doc['title']} | rerank_score={doc['rerank_score']:.4f}")
        print(doc["text"])


if __name__ == "__main__":
    main()