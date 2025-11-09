# 🚀 Riverwood AI Voice Agent – "Rahul"

### 🎥 Challenge Submission
Watch the full demo here 👉 [Loom Video]((https://www.loom.com/share/3d5d186e50814daca79c52727c655587))

---

### 🧠 About the Project
“Rahul” is a real-time AI voice agent built using **LiveKit Agents**, **Deepgram STT**, **ElevenLabs TTS**, and **Gemini 2.5 Flash LLM**.

It acts like a digital project manager who:
- Understands **Hinglish (Hindi + English)** naturally  
- Responds instantly with **low-latency speech**  
- Maintains **context** across conversation turns  
- Uses a friendly and relatable **voice personality**

---

### ⚙️ Tech Stack
| Component | Technology Used |
|------------|----------------|
| **Framework** | LiveKit Agents |
| **Speech-to-Text (STT)** | Deepgram Multi-Language Model |
| **Text-to-Speech (TTS)** | ElevenLabs (Voice: Adam) |
| **LLM (Brain)** | Google Gemini 2.5 Flash |
| **Language Support** | English, Hindi, Hinglish |
| **Memory** | LiveKit Session Context |

---

### 🧩 Features
- Real-time speech streaming  
- Natural bilingual interaction (Hinglish)  
- Context awareness (remembers last project/topic)  
- Voice latency masking for fast response  
- Low-cost + efficient pipeline  

---

### 🧑‍💻 How to Run
```bash
# Clone repo
git clone https://github.com/ejaz029/riverwood-ai_voice-agent_.git
cd riverwood-ai_voice-agent_

# Install dependencies
pip install -r requirements.txt

# Add your API keys in .env
# (LIVEKIT_API_KEY, LIVEKIT_SECRET, DEEPGRAM_API_KEY, ELEVENLABS_API_KEY, GOOGLE_API_KEY)

# Run Rahul Agent
python riverwood.py
