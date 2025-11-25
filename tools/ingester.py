from langchain_community.document_loaders import PyPDFLoader
import asyncio
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_milvus import Milvus
import os
from uuid import uuid4


async def main():
    loader = PyPDFLoader(
        file_path="./docs/example.pdf",
        mode="single"
    )

    embeddings = OllamaEmbeddings(model="embeddinggemma:latest")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=800,
        length_function=len,
        is_separator_regex=False,
    )

    docs = loader.load()
    doc_splits = text_splitter.split_documents(docs)

    milvus_addr = os.getenv('MILVUS_ADDR')
    if not milvus_addr:
        raise ValueError("MILVUS_ADDR environment variable is not set.")
    
    milvus_collection = os.getenv('MILVUS_COLLECTION')
    if not milvus_collection:
        raise ValueError("MILVUS_COLLECTION environment variable is not set.")

    vector_store = Milvus(
        embedding_function=embeddings,
        collection_name=milvus_collection,
        collection_description="Knowledge base collection",
        connection_args={"uri": milvus_addr},
        index_params={"index_type": "FLAT", "metric_type": "L2"},
    )

    # Clean up existing collection if it exists. for demo purposes.
    vector_store.drop()

    uuids = [str(uuid4()) for _ in range(len(doc_splits))]

    vector_store.add_documents(documents=doc_splits, ids=uuids)
    print("Documents added to Milvus vector store.")

    results = vector_store.similarity_search_with_score(
        "what is the typical ML pipeline comprised of?", k=3
    )

    for res, score in results:
        print(f"* [SIM={score:3f}] {res.page_content} [{res.metadata}]")


if __name__ == "__main__":
    asyncio.run(main())

