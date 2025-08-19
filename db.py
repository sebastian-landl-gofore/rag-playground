from typing import List, Optional, Dict
import chromadb

def get_chroma_client(path: Optional[str] = None):
    if path:
        return chromadb.PersistentClient(path=path)
    else:
        return chromadb.EphemeralClient()

def get_or_create_collection(client, name: str, similarity_metric: str = "cosine"):
    return client.get_or_create_collection(
        name=name,
        metadata={
            "hnsw:space": similarity_metric,
        }
    )

def add_document(
    collection,
    doc_id: str,
    document: str,
    metadata: Optional[Dict] = None,
    embedding: Optional[List[float]] = None,
):
    collection.add(
        ids=[doc_id],
        documents=[document],
        metadatas=[metadata] if metadata else None,
        embeddings=[embedding] if embedding else None,
    )

def query_by_embedding(
    collection, query_embedding: List[float], n_results: int = 3
) -> List[Dict]:
    documents = collection.query(query_embeddings=[query_embedding], n_results=n_results)

    result = []
    for id, document, metadata, distance in zip(documents["ids"][0], documents["documents"][0], documents["metadatas"][0], documents["distances"][0]):
        result.append({
            "id": id,
            "document": document,
            "metadata": metadata,
            "distance": distance,
        })
    return result
