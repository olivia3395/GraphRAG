from typing import List, Dict


def build_prompt(question: str, text_hits: List[Dict], image_hits: List[Dict]) -> str:
    text_block = "\n\n".join(
        [f"[TEXT {i+1}] {item['content']}" for i, item in enumerate(text_hits[:8])]
    )

    image_block = "\n".join(
        [f"[IMAGE {i+1}] {item.get('metadata', {})}" for i, item in enumerate(image_hits[:5])]
    )

    return f"""
You are a grounded retrieval QA assistant.
Answer ONLY using the provided evidence.
If the evidence is insufficient, say so clearly.

Question:
{question}

Text Evidence:
{text_block}

Image Evidence:
{image_block}

Please provide:
1. A concise answer.
2. A short explanation grounded in the evidence.
""".strip()
