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

    import time
    batch_size = 10
    total_batches = (len(chunks) + batch_size - 1) // batch_size
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i : i + batch_size]
        retries = 3
        for attempt in range(retries):
            try:
                add_documents(batch)
                print(f"  Added batch {i // batch_size + 1}/{total_batches} ({len(batch)} chunks)")
                break
            except Exception as e:
                if attempt < retries - 1:
                    wait = 30 * (attempt + 1)
                    print(f"  Rate limited, waiting {wait}s...")
                    time.sleep(wait)
                else:
                    raise e
        if i + batch_size < len(chunks):
            time.sleep(5)

    stats = get_collection_stats()
    print(f"Vector store now has {stats['count']} documents")


if __name__ == "__main__":
    main()
