from datetime import datetime

from sentence_transformers import SentenceTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction
from database import get_vector_collection
from settings import (
    CHROMA_TEXT_SPLITTER_CHUNK_SIZE,
    CHROMA_TEXT_SPLITTER_CHUNK_OVERLAP,
    CHROMA_EMBEDDING_MODEL,
    CHROMA_TOP_K,
)


def get_embedding_model(default=False):
    if default:
        return DefaultEmbeddingFunction()

    local_path = f"./{CHROMA_EMBEDDING_MODEL}"
    model = SentenceTransformer(local_path)
    return model


def gen_vectors(
    embedding_model: SentenceTransformer, file_hash, file_name, file_type, docs
):
    vectors = {"ids": [], "embeddings": [], "metadatas": []}
    for idx, doc in enumerate(docs):
        vector = embedding_model.encode(doc)
        unique_id = f"doc_{file_hash}_{idx}"
        vectors["ids"].append(unique_id)
        vectors["embeddings"].append(vector)
        vectors["metadatas"].append(
            {
                "id": unique_id,
                "name": file_name,
                "hash": file_hash,
                "type": file_type,
                "content": doc,
                "created_at": f"{datetime.now()}",
            }
        )

    return vectors


def add_text_to_vector_db(file_hash: str, file_name: str, file_type: str, content: str):
    """
    Adds a document and its embedding to the ChromaDB collection.
    """
    collection = get_vector_collection()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHROMA_TEXT_SPLITTER_CHUNK_SIZE,
        chunk_overlap=CHROMA_TEXT_SPLITTER_CHUNK_OVERLAP,
    )
    split_docs = text_splitter.split_text(content)
    embedding_model = get_embedding_model()

    print(f"Split docs: {len(split_docs)}")
    vectors = gen_vectors(embedding_model, file_hash, file_name, file_type, split_docs)

    collection.add(vectors)


def retrieve_relevant_docs(query, collection, embedding_model: SentenceTransformer):
    # 生成查询向量
    query_vector = embedding_model.encode(query)
    # 从向量库检索相似文档
    results = collection.query(
        query_embeddings=[query_vector],
        n_results=CHROMA_TOP_K,  # 返回最相似的 top_k 个文档
    )
    return results["documents"][0]  # 返回检索到的文本列表


def query_vector_db(query: str):
    """
    Queries the vector database for relevant documents.
    """
    collection = get_vector_collection()
    relevant_docs = retrieve_relevant_docs(query, collection, get_embedding_model())
    docs_str = "\n".join([f"- {doc}" for doc in relevant_docs])
    return docs_str
    prompt = f"""
    基于以下参考文档，回答用户问题。如果文档中没有相关信息，直接说“无法回答”。
    参考文档：
    {docs_str}

    用户问题：{query}
    回答：
    """
    # query_embedding = retrieve_relevant_docs(prompt, collection, get_embedding_model())
    # TODO: 调用LLM
    # return prompt
    return ""


def delete_vector(file_hash: str):
    """
    Deletes a vector from the collection by its ID.
    """
    collection = get_vector_collection()
    collection.delete(ids=[file_hash])
