import os
import time
from .config import SYSTEM_PROMPT, pick_llm_config
from .llm import generate_reply
from .tts import speak_tts
from .input_io import capture_user_input
from .memory import init_memory, memory_to_messages, remember


def main():
    print("\n=== Riverwood AI Voice Agent Challenge – 'Miss Riverwood' ===\n")
    print("[Setup] Checking environment and initializing components...")

    llm_cfg = pick_llm_config()
    memory_obj = init_memory()

    print("[Agent] Greeting user...")
    greeting = "Namaste sir, chai pee li? Main Miss Riverwood hoon. Main madad karu?"
    print("Miss Riverwood:", greeting)
    speak_tts(greeting)

    construction_nudge = "Kal site visit kaisa raha, sir? Kisi contractor ke saath meeting hui?"

    turns = 0
    max_turns = int(os.getenv("RIVERWOOD_MAX_TURNS", "6"))
    hard_stop_secs = int(os.getenv("RIVERWOOD_MAX_SECONDS", "120"))
    start_time = time.time()

    while turns < max_turns and (time.time() - start_time) < hard_stop_secs:
        try:
            if turns == 0:
                print("\n[Prompt] (Optional construction update)")
                print("Miss Riverwood:", construction_nudge)
                speak_tts(construction_nudge)

            user_text = capture_user_input()
            if not user_text:
                print("[Info] Empty input received. Ending conversation.")
                break
            if user_text.lower() in {"exit", "quit", "bye", "stop"}:
                print("[Info] Exit keyword detected. Bye!")
                break

            messages = [{"role": "system", "content": SYSTEM_PROMPT}]
            messages.extend(memory_to_messages(memory_obj))
            messages.append({"role": "user", "content": user_text})

            reply = generate_reply(messages, llm_cfg)
            if not reply:
                reply = "Samjha, main dubara try karti hoon. Aap thoda aur batayein."

            print("Miss Riverwood:", reply)
            speak_tts(reply)
            remember(memory_obj, user_text, reply)

            turns += 1
        except KeyboardInterrupt:
            print("\n[Info] Stopped by user (Ctrl+C). Shukriya!")
            break
        except Exception as e:
            print("[Error] Unexpected issue:", e)
            break

    closing = "Aaj ki baat-cheet ke liye dhanyavaad, sir. Phir milte hain!"
    print("Miss Riverwood:", closing)
    speak_tts(closing)

    print("\nSubmit this demo to hr@riverwoodindia.com – AI Voice Agent Challenge 💬\n")


