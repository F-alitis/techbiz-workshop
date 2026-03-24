import sys

sys.path.insert(0, ".")
from src.rag.vector_store import get_collection_stats, search

TEST_QUERIES = [
    "What credit cards does NBG offer?",
    "What are the mortgage loan options?",
    "How can I open a bank account?",
    "What are NBG business banking services?",
    "How to contact NBG?",
]


def main():
    stats = get_collection_stats()
    print(f"Vector store has {stats['count']} documents\n")

    for query in TEST_QUERIES:
        print(f"Query: {query}")
        results = search(query, k=3)
        for i, doc in enumerate(results):
            print(f"  [{i + 1}] {doc.page_content[:100]}...")
            print(f"      Source: {doc.metadata.get('source_url', 'N/A')}")
        print()


if __name__ == "__main__":
    main()
