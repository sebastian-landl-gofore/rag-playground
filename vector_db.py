from typing import List, Optional, Dict
import chromadb

def get_chroma_client(path: Optional[str] = None):
    """
    Create a ChromaDB client instance.

    If a path is provided, a persistent client is created that stores data 
    on disk at the given path. Otherwise, an ephemeral client is created 
    that only stores data in memory.

    Args:
        path (Optional[str]): Filesystem path for persistent storage. 
            If None, an in-memory client is used.

    Returns:
        A ChromaDB client instance.
    """
    if path:
        return chromadb.PersistentClient(path=path)
    else:
        return chromadb.EphemeralClient()


def get_or_create_collection(client, name: str, similarity_metric: str = "cosine"):
    """
    Retrieve or create a collection in ChromaDB.

    A collection is a named container for documents, embeddings, and 
    metadata. If the collection does not exist, it will be created 
    with the given similarity metric.

    Args:
        client: A ChromaDB client instance.
        name (str): Name of the collection.
        similarity_metric (str, optional): Distance metric for nearest-neighbor 
            search. Supported values include "cosine", "l2", and "ip".
            Defaults to "cosine".

    Returns:
        The retrieved or created collection.
    """
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
    """
    Add a single document to a ChromaDB collection.

    The document is stored along with its ID, optional metadata, and 
    optional pre-computed embedding.

    Args:
        collection: A ChromaDB collection instance.
        doc_id (str): Unique identifier for the document.
        document (str): The text content of the document.
        metadata (Optional[Dict], optional): Additional metadata associated 
            with the document. Defaults to None.
        embedding (Optional[List[float]], optional): Pre-computed vector 
            embedding for the document. Defaults to None.

    Returns:
        None
    """
    collection.add(
        ids=[doc_id],
        documents=[document],
        metadatas=[metadata] if metadata else None,
        embeddings=[embedding] if embedding else None,
    )


def query_by_embedding(
    collection, query_embedding: List[float], n_results: int = 3
) -> List[Dict]:
    """
    Query a collection using a vector embedding.

    Finds the most similar documents in the collection to the given 
    embedding, ranked by similarity score.

    Args:
        collection: A ChromaDB collection instance.
        query_embedding (List[float]): Vector embedding used as the query.
        n_results (int, optional): Maximum number of results to return. 
            Defaults to 3.

    Returns:
        List[Dict]: A list of result dictionaries containing:
            - "id": Document ID (str)
            - "document": Document text (str)
            - "metadata": Associated metadata (dict or None)
            - "distance": Similarity/distance score (float)
    """
    documents = collection.query(query_embeddings=[query_embedding], n_results=n_results)

    result = []
    for id, document, metadata, distance in zip(
        documents["ids"][0],
        documents["documents"][0],
        documents["metadatas"][0],
        documents["distances"][0],
    ):
        result.append({
            "id": id,
            "document": document,
            "metadata": metadata,
            "distance": distance,
        })
    return result
