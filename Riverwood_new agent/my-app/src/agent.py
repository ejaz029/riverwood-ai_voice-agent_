


##################->                    new code from here

import os
import asyncio
from dotenv import load_dotenv
from livekit.agents import Agent, AgentSession, JobContext, WorkerOptions, cli
from livekit.plugins import elevenlabs, google, deepgram

# Load all the API keys from your .env file
load_dotenv()

# --- THIS IS YOUR AGENT'S "SOUL" ---
# This is the prompt that defines the personality.
SYSTEM_PROMPT = """
You are 'Rahul,' a friendly and warm project manager from Riverwood Projects.
Your goal is to build a personal bond, not just give updates.

LANGUAGE RULES:
- You can speak in BOTH Hindi and English fluently
- MIRROR the user's language preference:
  * If they speak in Hindi, respond in Hindi
  * If they speak in English, respond in English
  * If they speak in Hinglish (mix), respond in Hinglish
- Your default style is casual Hinglish (mix of Hindi and English)
- Your tone is informal, warm, and friendly

CONVERSATION STYLE:
- Start the call with a casual greeting like "Namaste Sir, chai pee li?" or "Hello Sir, how are you?"
- Keep your responses very short and conversational, like a real phone call
- Remember what the user says and reference it in conversation

CONSTRUCTION UPDATES:
- If the user asks for a construction update in Hindi/Hinglish, say: "Haan sir, update ye hai ki foundation kaam complete ho gaya hai aur brickwork aaj start ho raha hai. Sab time pe chal raha hai."
- If the user asks in English, say: "Yes sir, the update is that foundation work is complete and brickwork is starting today. Everything is on schedule."
- If the user asks anything else, just be friendly and chat naturally
"""

# This is the main function that runs when the agent joins a room
async def entrypoint(ctx: JobContext):
    await ctx.connect()

    # 1. --- CONFIGURE THE "BRAIN" (Gemini) ---
    # We use "gemini-1.5-flash" for speed (to meet the Latency requirement)
    # Create an Agent with the system prompt as instructions
    agent = Agent(instructions=SYSTEM_PROMPT)

    # 2. --- CONFIGURE THE "EARS" (Speech-to-Text) ---
    # We'll use Deepgram for fast transcription.
    
    stt = deepgram.STT(
        model="nova-2-general",  # Best model for multilingual including Hindi+English
        language="multi",  # Multilingual mode for both Hindi and English
        # Note: detect_language is not supported in streaming mode
        keywords=[  # Give it "hint" words with boost values
            ("Riverwood", 2.0),
            ("Namaste", 2.0),
            ("chai", 2.0),
            ("pee li", 2.0),
            ("kaise hain", 2.0),
            ("aapne", 2.0),
            ("construction", 1.5),
            ("update", 1.5),
            ("foundation", 1.5),
            ("brickwork", 1.5),
            ("hello", 1.5),
            ("how are you", 1.5)
        ]
    )

    # 3. --- CONFIGURE THE "MOUTH" (ElevenLabs) ---
    tts = elevenlabs.TTS(
        model="eleven_multilingual_v2",
        voice_id="pNInz6obpgDQGcFmaJgB"  # <-- (kept Rahul voice)IMPORTANT: Paste the Voice ID you copied here!
    )

    # 4. --- CONFIGURE THE LLM (Gemini) ---
    # Using gemini-1.5-flash (stable, higher quota than 2.0-exp)
    llm = google.LLM(model="gemini-2.0-flash")

    # 5. --- CREATE THE SESSION ---
    # This connects the Brain, Ears, and Mouth together
    session = AgentSession(
        llm=llm,
        stt=stt,
        tts=tts,
    )

    # 6. --- START THE CONVERSATION ---
    # This tells the agent to join the room and start the session
    await session.start(agent=agent, room=ctx.room)

    # This makes the agent speak its first line *without* waiting for the user.
    # This is key for a natural-feeling call.
    await asyncio.sleep(1) # Give a 1s pause
    await session.say("Namaste Sir, chai pee li aapne?")

# This is the code that allows you to run the file
if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, agent_name="riverwood-agent"))