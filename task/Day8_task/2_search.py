
from pathlib import Path

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import FastEmbedEmbeddings

from lc_config import CHROMA_DB_DIR, EMBEDDING_MODEL


BASE_DIR = Path(__file__).resolve().parent

def main():
    query = "What CGPA do I need to be eligible for placements?"

    embeddings = FastEmbedEmbeddings(model_name=EMBEDDING_MODEL)

    store = Chroma(
        collection_name="day8_task_handbook",
        embedding_function=embeddings,
        persist_directory=str(CHROMA_DB_DIR),
    )

    results = store.similarity_search_with_score(query, k=3)

    print(f"Question: {query}")
    print("\nTop search results:")

    for i, (document, score) in enumerate(results, start=1):
        source = Path(document.metadata.get("source", "unknown")).name
        print(f"\nResult {i}")
        print(f"Source: {source}")
        print(f"Distance score: {score:.4f}")
        print(f"Content:\n{document.page_content}")

    if results:
        best_source = Path(
            results[0][0].metadata.get("source", "unknown")
        ).name

        if best_source == "placement_policy.md":
            print("\nPASS: Top result is placement_policy.md")
        else:
            print("\nCHECK: Top result is not placement_policy.md")


if __name__ == "__main__":
    main()

