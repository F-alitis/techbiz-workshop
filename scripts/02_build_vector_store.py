import sys
from pathlib import Path

sys.path.insert(0, ".")
from src.rag.chunker import chunk_documents
from src.rag.vector_store import add_documents, get_collection_stats


def main():
    raw_dir = Path("data/raw")
    if not raw_dir.exists() or not list(raw_dir.glob("*.md")):
        print("No raw data found. Run 01_crawl_nbg.py first.")
        return

    docs = []
    for f in raw_dir.glob("*.md"):
        content = f.read_text()
        docs.append(
            {
                "url": f.stem.replace("_", "/"),
                "title": f.stem,
                "content": content,
                "timestamp": "",
            }
        )

    chunks = chunk_documents(docs)
    print(f"Created {len(chunks)} chunks from {len(docs)} documents")

    add_documents(chunks)
    stats = get_collection_stats()
    print(f"Vector store now has {stats['count']} documents")


if __name__ == "__main__":
    main()
