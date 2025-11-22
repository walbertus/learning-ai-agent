from langchain_opendataloader_pdf import OpenDataLoaderPDFLoader
import asyncio
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_milvus import Milvus
import os
import pprint
from uuid import uuid4


async def main():
    loader = OpenDataLoaderPDFLoader(
        file_path="./docs/example.pdf",
        format="markdown",
        quiet=True,
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

    db_path = "./data/milvus_example.db"
    if os.path.exists(db_path):
        os.remove(db_path)

    vector_store = Milvus(
        embedding_function=embeddings,
        connection_args={"uri": db_path},
        index_params={"index_type": "FLAT", "metric_type": "L2"},
    )

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

