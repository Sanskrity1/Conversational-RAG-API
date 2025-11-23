from typing import List, Optional
import os
import asyncio
from dataclasses import dataclass


@dataclass
class LLMClient:
    model: str

    def __post_init__(self):
        self.api_key = os.environ.get("OPENAI_API_KEY")

    def build_prompt(self, user_message: str, history: List[dict], contexts: List["ContextChunk"]) -> str:
        """
        Create the final prompt to send to the LLM.
        - history: list of {"role": "...", "text": "..."}
        - contexts: list of ContextChunk with .text and .meta
        """
        parts = []
        if history:
            parts.append("Conversation history:")
            for m in history:
                parts.append(f"{m['role']}: {m['text']}")
            parts.append("\n---\n")

        if contexts:
            parts.append("Relevant documents:")
            for c in contexts:
                parts.append(f"- {c.meta.get('title','unknown')}: {c.text[:800]}")
            parts.append("\n---\n")

        parts.append("User message:")
        parts.append(user_message)

        prompt = "\n".join(parts)
        return prompt

    async def generate(self, prompt: str) -> str:
        """
        Default implementation uses synchronous network call placeholder.
        Replace with OpenAI/other SDK as required.
        Here we'll use a very small placeholder that echoes the prompt for safety.
        """
        await asyncio.sleep(0.1)
        return f"[LLM generated answer based on prompt of {len(prompt)} chars]\n\n{prompt[:1000]}"
