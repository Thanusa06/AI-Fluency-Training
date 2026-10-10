
from pathlib import Path

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import FastEmbedEmbeddings

from lc_config import CHROMA_DB_DIR, EMBEDDING_MODEL


# Get the folder containing this Python file.
BASE_DIR = Path(__file__).resolve().parent

# Folder containing the handbook Markdown documents.
DATA_DIR = BASE_DIR / "data"


def main():
    print("Starting handbook ingestion...")

    # Check whether the data folder exists.
    if not DATA_DIR.exists():
        print(f"ERROR: Data folder not found: {DATA_DIR}")
        return

    # Load all Markdown documents from the data folder.
    loader = DirectoryLoader(
        str(DATA_DIR),
        glob="**/*.md",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
        show_progress=True,
    )

    documents = loader.load()

    if not documents:
        print("ERROR: No Markdown documents were found.")
        return

    print(f"Documents loaded: {len(documents)}")

    # Split each document into smaller chunks.
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
    )

    chunks = splitter.split_documents(documents)

    print(f"Chunks created: {len(chunks)}")

    # Create the embedding model.
    embeddings = FastEmbedEmbeddings(
        model_name=EMBEDDING_MODEL
    )

    # Store the document chunks in ChromaDB.
    # Use a separate collection for the task.
    vector_store = Chroma(
        collection_name="day8_task_handbook",
        embedding_function=embeddings,
        persist_directory=str(CHROMA_DB_DIR),
    )

    # Clear this task's old collection before re-ingesting,
    # preventing duplicate chunks when you run this script again.
    existing_ids = vector_store.get()["ids"]

    if existing_ids:
        vector_store.delete(ids=existing_ids)

    vector_store.add_documents(chunks)

    print(f"Vectors stored: {len(chunks)}")
    print(f"Vector database: {CHROMA_DB_DIR}")
    print("Ingestion completed successfully.")


if __name__ == "__main__":
    main()

