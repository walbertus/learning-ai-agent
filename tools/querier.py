import os
from mcp.server.fastmcp import FastMCP
from langchain_ollama import OllamaEmbeddings
from langchain_milvus import Milvus


# mcp = FastMCP("weather")
mcp = FastMCP(
    name="knowledge_center",
    port=8001,
)


@mcp.tool()
def gather_knowlege(query: str) -> str:
    """Gather knowledge from the vector store.

    Args:
        query: The query string to search for.
    """
    milvus_addr = os.getenv('MILVUS_ADDR')
    if not milvus_addr:
        raise ValueError("MILVUS_ADDR environment variable is not set.")
    
    milvus_collection = os.getenv('MILVUS_COLLECTION')
    if not milvus_collection:
        raise ValueError("MILVUS_COLLECTION environment variable is not set.")
    embeddings = OllamaEmbeddings(model="embeddinggemma:latest")
    vector_store = Milvus(
        embedding_function=embeddings,
        collection_name=milvus_collection,
        connection_args={"uri": milvus_addr},
        index_params={"index_type": "FLAT", "metric_type": "L2"},
    )
    retriever = vector_store.as_retriever()
    results = retriever.invoke(
        input=query,
        config={"k": 5},
    )
    response = ""
    for res in results:
        response += f"* content: {res.page_content} metadata:[{res.metadata}]\n"
    return response


def main():
    mcp.run(
        transport="sse",
    )

if __name__ == "__main__":
    main()
