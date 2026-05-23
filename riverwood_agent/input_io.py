try:
    import speech_recognition as sr
except Exception:
    sr = None


def mic_available() -> bool:
    if sr is None:
        return False
    try:
        return bool(sr.Microphone.list_microphone_names())
    except Exception:
        return False


def capture_user_input() -> str:
    if sr and mic_available():
        print("[Input] Listening on microphone... (speak now)")
        recognizer = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.4)
                audio = recognizer.listen(source, timeout=6, phrase_time_limit=12)
            try:
                text = recognizer.recognize_google(audio)
                print("[Input] You said:", text)
                return text
            except Exception as e:
                print("[Input] Speech recognition failed:", e)
        except Exception as e:
            print("[Input] Microphone error:", e)
    return input("You: ").strip()


