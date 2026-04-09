from app.ingestion.chunker import TextChunker


def test_chunker_outputs_multiple_chunks():
    chunker = TextChunker(chunk_size=20, chunk_overlap=5)
    text = "abcdefghijklmnopqrstuvwxyz0123456789"
    chunks = chunker.chunk(text)
    assert len(chunks) >= 2


def test_chunker_handles_empty_text():
    chunker = TextChunker(chunk_size=20, chunk_overlap=5)
    assert chunker.chunk("") == []
