try:
    from langchain.memory import ConversationBufferMemory
except Exception:
    ConversationBufferMemory = None


def init_memory():
    if ConversationBufferMemory is None:
        print("[Memory] LangChain not installed. Running without memory.")
        return None
    print("[Memory] Using LangChain ConversationBufferMemory")
    return ConversationBufferMemory(memory_key="history", return_messages=True)


def memory_to_messages(memory_obj) -> list:
    messages = []
    if memory_obj is None:
        return messages
    try:
        history = memory_obj.load_memory_variables({}).get("history", [])
        for m in history:
            role = "assistant" if getattr(m, "type", "") == "ai" else (
                "user" if getattr(m, "type", "") == "human" else "user"
            )
            messages.append({"role": role, "content": m.content})
    except Exception as e:
        print("[Memory] Failed to read memory:", e)
    return messages


def remember(memory_obj, user_text: str, ai_text: str) -> None:
    if memory_obj is None:
        return
    try:
        memory_obj.chat_memory.add_user_message(user_text)
        memory_obj.chat_memory.add_ai_message(ai_text)
    except Exception as e:
        print("[Memory] Failed to write memory:", e)


