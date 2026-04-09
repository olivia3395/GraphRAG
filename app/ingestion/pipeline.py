from app.utils.file_utils import list_text_files, list_image_files
from app.utils.id_utils import stable_id
from app.ingestion.loaders import load_text_file
from app.ingestion.chunker import TextChunker
from app.ingestion.image_loader import load_image


class IngestionPipeline:
    def __init__(
        self,
        text_embedder,
        image_embedder,
        text_store,
        image_store,
        entity_extractor,
        graph_builder,
        chunk_size: int,
        chunk_overlap: int,
    ):
        self.text_embedder = text_embedder
        self.image_embedder = image_embedder
        self.text_store = text_store
        self.image_store = image_store
        self.entity_extractor = entity_extractor
        self.graph_builder = graph_builder
        self.chunker = TextChunker(chunk_size=chunk_size, chunk_overlap=chunk_overlap)

    def ingest(self, data_dir: str):
        text_files = list_text_files(data_dir)
        image_files = list_image_files(data_dir)

        self.graph_builder.clear()

        all_chunk_ids = []
        all_chunks = []
        all_chunk_meta = []

        for path in text_files:
            raw = load_text_file(path)
            chunks = self.chunker.chunk(raw)
            for idx, chunk in enumerate(chunks):
                chunk_id = stable_id(f"{path}-{idx}-{chunk[:80]}")
                meta = {"source": str(path), "chunk_index": idx}
                all_chunk_ids.append(chunk_id)
                all_chunks.append(chunk)
                all_chunk_meta.append(meta)

                ents = self.entity_extractor.extract(chunk)
                self.graph_builder.add_chunk_entities(
                    chunk_id,
                    ents,
                    metadata={
                        "source": str(path),
                        "chunk_index": idx,
                        "content": chunk,
                    },
                )
                self.graph_builder.connect_cooccurring_entities(ents)

        if all_chunks:
            chunk_embs = self.text_embedder.encode(all_chunks).tolist()
            self.text_store.add(
                ids=all_chunk_ids,
                embeddings=chunk_embs,
                documents=all_chunks,
                metadatas=all_chunk_meta,
            )

        image_ids = []
        image_docs = []
        image_metas = []
        images = []
        for path in image_files:
            img = load_image(path)
            images.append(img)
            image_ids.append(stable_id(str(path)))
            image_docs.append(f"Image file: {path.name}")
            image_metas.append({"source": str(path), "filename": path.name})

        if images:
            img_embs = self.image_embedder.encode_images(images).tolist()
            self.image_store.add(
                ids=image_ids,
                embeddings=img_embs,
                documents=image_docs,
                metadatas=image_metas,
            )

        return {
            "num_text_files": len(text_files),
            "num_image_files": len(image_files),
            "num_chunks": len(all_chunks),
        }
