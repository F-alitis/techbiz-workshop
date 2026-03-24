from src.rag.chunker import chunk_text, chunk_documents


def test_chunk_text_respects_size():
    text = "Hello world. " * 200  # ~2600 chars
    chunks = chunk_text(text)
    for chunk in chunks:
        assert len(chunk.page_content) <= 1200  # some tolerance for splitter


def test_chunk_text_with_metadata():
    text = "Banking products include savings accounts and credit cards." * 20
    metadata = {"source_url": "https://www.nbg.gr/en/retail", "title": "Retail"}
    chunks = chunk_text(text, metadata=metadata)
    for chunk in chunks:
        assert chunk.metadata.get("source_url") == "https://www.nbg.gr/en/retail"


def test_chunk_documents():
    docs = [
        {
            "url": "https://www.nbg.gr/en/retail",
            "title": "Retail Banking",
            "content": "NBG offers various retail products. " * 50,
            "timestamp": "2026-03-24",
        }
    ]
    chunks = chunk_documents(docs)
    assert len(chunks) > 0
    assert chunks[0].metadata.get("source_url") == "https://www.nbg.gr/en/retail"


def test_chunk_overlap():
    text = "Sentence one. Sentence two. Sentence three. " * 100
    chunks = chunk_text(text)
    if len(chunks) >= 2:
        # Check that consecutive chunks have some overlapping content
        c1_end = chunks[0].page_content[-50:]
        c2_start = chunks[1].page_content[:200]
        # With 200 char overlap, there should be some shared text
        assert any(word in c2_start for word in c1_end.split())
