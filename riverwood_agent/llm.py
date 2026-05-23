from typing import List, Dict
from .config import LLMConfig


def generate_reply(messages: List[Dict[str, str]], llm_cfg: LLMConfig) -> str:
    print("[LLM] Generating reply via:", llm_cfg.provider, "model:", llm_cfg.model)

    if llm_cfg.provider == "openai":
        try:
            from openai import OpenAI
        except Exception as e:
            print("[LLM] OpenAI SDK not installed:", e)
            return "Mujhe thoda issue aa raha hai setup me. Please try text mode."
        client = OpenAI()
        resp = client.chat.completions.create(
            model=llm_cfg.model,
            messages=messages,
            temperature=0.7,
            max_tokens=300,
        )
        return (resp.choices[0].message.content or "").strip()

    if llm_cfg.provider == "groq":
        try:
            from groq import Groq
        except Exception as e:
            print("[LLM] Groq SDK not installed:", e)
            return "Setup issue with Groq SDK. Thoda rukiyega, please use text mode."
        client = Groq()
        resp = client.chat.completions.create(
            model=llm_cfg.model,
            messages=messages,
            temperature=0.7,
            max_tokens=300,
        )
        return (resp.choices[0].message.content or "").strip()

    return "Config error: Unknown LLM provider."


