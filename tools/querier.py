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
    db_path = "./data/milvus_example.db"
    embeddings = OllamaEmbeddings(model="embeddinggemma:latest")
    vector_store = Milvus(
        embedding_function=embeddings,
        connection_args={"uri": db_path},
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
