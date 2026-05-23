import os
import sys
import uuid
import tempfile

try:
    from gtts import gTTS
except Exception:
    gTTS = None

try:
    from playsound import playsound
except Exception:
    playsound = None

try:
    import requests
except Exception:
    requests = None


def speak_tts(text: str) -> None:
    text = text.strip()
    if not text:
        return

    eleven_key = os.getenv("ELEVENLABS_API_KEY")
    voice_id = os.getenv("ELEVENLABS_VOICE_ID", "Rachel")
    if eleven_key and requests:
        print("[TTS] Using ElevenLabs voice:", voice_id)
        try:
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
            headers = {
                "xi-api-key": eleven_key,
                "accept": "audio/mpeg",
                "content-type": "application/json",
            }
            payload = {
                "text": text,
                "model_id": os.getenv("ELEVENLABS_MODEL", "eleven_turbo_v2"),
                "voice_settings": {"stability": 0.5, "similarity_boost": 0.8},
            }
            r = requests.post(url, json=payload, headers=headers, timeout=60)
            r.raise_for_status()
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
                f.write(r.content)
                audio_path = f.name
            _play_audio(audio_path)
            _safe_unlink(audio_path)
            return
        except Exception as e:
            print("[TTS] ElevenLabs failed, falling back to gTTS:", e)

    if gTTS is None:
        print("[TTS] gTTS not available. Skipping audio.")
        return

    print("[TTS] Using gTTS (Google Text-to-Speech)")
    try:
        tts = gTTS(text=text, lang="en")
        tmp_file = os.path.join(tempfile.gettempdir(), f"riverwood_tts_{uuid.uuid4().hex}.mp3")
        tts.save(tmp_file)
        _play_audio(tmp_file)
        _safe_unlink(tmp_file)
    except Exception as e:
        print("[TTS] gTTS failed:", e)


def _play_audio(path: str) -> None:
    print(f"[Audio] Playing: {path}")
    if playsound:
        try:
            playsound(path)
            return
        except Exception as e:
            print("[Audio] playsound failed, trying OS fallback:", e)
    try:
        if sys.platform.startswith("win"):
            os.startfile(path)  # type: ignore[attr-defined]
        else:
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            os.system(f"{opener} '{path}'")
    except Exception as e:
        print("[Audio] Fallback failed:", e)


def _safe_unlink(path: str) -> None:
    try:
        os.remove(path)
    except Exception:
        pass


