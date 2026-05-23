import os
from dataclasses import dataclass


SYSTEM_PROMPT = (
    "You are 'Miss Riverwood', an empathetic, concise site project assistant for Riverwood Projects LLP. "
    "Blend casual Indian English with light Hindi (Hinglish). Keep replies natural, friendly, and brief. "
    "If user mentions construction, proactively ask short, relevant follow-ups."
)


@dataclass
class LLMConfig:
    provider: str  # 'openai' or 'groq'
    model: str


def pick_llm_config() -> LLMConfig:
    openai_key = os.getenv("OPENAI_API_KEY")
    groq_key = os.getenv("GROQ_API_KEY")
    if openai_key:
        return LLMConfig(provider="openai", model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"))
    if groq_key:
        return LLMConfig(provider="groq", model=os.getenv("GROQ_MODEL", "llama-3.1-70b-versatile"))
    return LLMConfig(provider="openai", model="gpt-4o-mini")


