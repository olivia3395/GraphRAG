from app.llm.prompt_builder import build_prompt


class AnswerPipeline:
    def __init__(self, retriever, generator):
        self.retriever = retriever
        self.generator = generator

    def answer(self, question: str, top_k_text: int = 5, top_k_image: int = 3, graph_hops: int = 1, use_multimodal: bool = True):
        retrieved = self.retriever.retrieve(
            query=question,
            top_k_text=top_k_text,
            top_k_image=top_k_image,
            graph_hops=graph_hops,
            use_multimodal=use_multimodal,
        )
        prompt = build_prompt(question, retrieved["text_hits"], retrieved["image_hits"])
        answer = self.generator.generate(
            prompt=prompt,
            question=question,
            text_hits=retrieved["text_hits"],
            image_hits=retrieved["image_hits"],
        )
        return {
            "answer": answer,
            "text_evidence": retrieved["text_hits"],
            "image_evidence": retrieved["image_hits"],
            "expanded_nodes": retrieved["expanded_nodes"],
        }
