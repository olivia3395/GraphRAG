# Multimodal Retrieval Notes

The system maintains a separate image index using CLIP-style embeddings. At query time, text queries can retrieve images through the shared embedding space. Those image hits are not treated as raw pixels in the answer prompt; instead, they contribute metadata such as filename, source path, and optional captions if the project is extended.

This design supports multimodal RAG: text chunks provide semantic explanation, while image retrieval can surface diagrams, figures, and visual references that strengthen grounding. In a production version, image captioning and OCR can be added before indexing to make image evidence even more useful.
