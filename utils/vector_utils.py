from datetime import datetime

from database import get_vector_collection

# In a real scenario, you would use a sentence transformer model
# from sentence_transformers import SentenceTransformer

# Placeholder for a sentence transformer model
# model = SentenceTransformer('all-MiniLM-L6-v2')


def get_text_embedding(text: str):
    """
    Generates a vector embedding for the given text.
    This is a placeholder. You should use a real model.
    """
    # return model.encode(text).tolist()
    # Simple placeholder: returns a list of character ordinals
    # THIS IS NOT A REAL EMBEDDING AND SHOULD BE REPLACED
    print("Warning: Using placeholder for text embedding. Replace with a real model.")
    return [ord(c) for c in text[:768]]  # Limit to a fixed size for example


def add_text_to_vector_db(file_hash: str, file_name: str, file_type: str, content: str):
    """
    Adds a document and its embedding to the ChromaDB collection.
    """
    collection = get_vector_collection()
    embedding = get_text_embedding(content)

    collection.add(
        ids=[file_hash],
        embeddings=[embedding],
        metadatas=[
            {
                "id": file_hash,
                "name": file_name,
                "type": file_type,
                "content": content,  # Storing full content might not be ideal for large files
                "created_at": str(datetime.utcnow()),
            }
        ],
    )


def query_vector_db(query_text: str, n_results: int = 5):
    """
    Queries the vector database for relevant documents.
    """
    collection = get_vector_collection()
    query_embedding = get_text_embedding(query_text)

    results = collection.query(query_embeddings=[query_embedding], n_results=n_results)
    return results


def delete_vector(file_hash: str):
    """
    Deletes a vector from the collection by its ID.
    """
    collection = get_vector_collection()
    collection.delete(ids=[file_hash])
