from typing import List, Dict
from openai import OpenAI
from app.utils.text_utils import split_sentences


class LLMGenerator:
    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model
        self.client = OpenAI(api_key=api_key) if api_key else None

    def _fallback_answer(self, question: str, text_hits: List[Dict], image_hits: List[Dict]) -> str:
        snippets = []
        for item in text_hits[:3]:
            snippets.extend(split_sentences(item.get("content", ""))[:2])
        answer_bits = snippets[:4]
        image_note = ""
        if image_hits:
            image_names = [hit.get("metadata", {}).get("filename", "image") for hit in image_hits[:2]]
            image_note = f" Relevant images include: {', '.join(image_names)}."
        if answer_bits:
            return "Fallback extractive answer (no API key configured): " + " ".join(answer_bits) + image_note
        return "Fallback extractive answer: insufficient evidence retrieved."

    def generate(self, prompt: str, question: str, text_hits: List[Dict], image_hits: List[Dict]) -> str:
        if not self.client:
            return self._fallback_answer(question, text_hits, image_hits)
        response = self.client.responses.create(
            model=self.model,
            input=prompt,
        )
        return response.output_text
