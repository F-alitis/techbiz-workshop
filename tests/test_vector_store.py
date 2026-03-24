def test_chroma_add_and_search():
    """Test ChromaDB operations with a temporary directory."""
    # Use in-memory chroma for testing (no API key needed)
    import chromadb

    client = chromadb.Client()
    collection = client.get_or_create_collection("test_collection")

    # Add documents
    collection.add(
        documents=["NBG offers Visa credit cards", "NBG mortgage rates are competitive", "Contact NBG at 210-484-8484"],
        ids=["doc1", "doc2", "doc3"],
        metadatas=[{"source": "cards"}, {"source": "loans"}, {"source": "contact"}],
    )

    # Search
    results = collection.query(query_texts=["credit cards"], n_results=2)
    assert len(results["documents"][0]) == 2
    assert "Visa" in results["documents"][0][0] or "credit" in results["documents"][0][0]


def test_chroma_empty_collection():
    import chromadb

    client = chromadb.Client()
    collection = client.get_or_create_collection("empty_test")

    assert collection.count() == 0
