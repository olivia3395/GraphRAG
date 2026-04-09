# OmniGraphRAG Overview

OmniGraphRAG is a retrieval-augmented generation system that combines dense vector retrieval, graph-based expansion, and multimodal evidence fusion. The pipeline first performs dense retrieval over chunk embeddings to identify the most directly relevant passages. After that, it extracts entities from both the user query and the corpus, and traverses an entity-chunk graph to recover second-hop evidence that vanilla RAG often misses.

This graph expansion step is useful when relevant information is distributed across multiple documents or chunks that share concepts, tools, organizations, or methods. For example, a question about CLIP-based multimodal retrieval may require one chunk about image embeddings and another chunk about how those images are fused with text evidence during answer generation.
