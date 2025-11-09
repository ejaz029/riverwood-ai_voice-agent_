import os
import asyncio
from dotenv import load_dotenv
from livekit.agents import (
    Agent, AgentSession, JobContext, WorkerOptions, cli, RunContext,
    RoomInputOptions, RoomOutputOptions
)
from livekit.agents.llm import function_tool
# Near line 11
from livekit.plugins import elevenlabs, google, deepgram
# Load all the API keys from your .env file
load_dotenv()

# -------------------------------------------------------------------------
# TOOLS - Keep responses SHORT for tool calls
# -------------------------------------------------------------------------

@function_tool
async def get_project_update(project_id: str) -> str:
    """Gets the latest construction progress update for a given project_id."""
    print(f"Tool called: get_project_update for project_id: {project_id}")
    if "45A" in project_id.upper():
        return "Foundation complete. Brickwork starting today. On schedule."
    else:
        return f"Project {project_id}: Foundation work ongoing and on track."

@function_tool
async def check_material_status(material_type: str) -> str:
    """Checks the delivery and availability status of a specific construction material."""
    print(f"Tool called: check_material_status for material: {material_type}")
    if "cement" in material_type.lower():
        return "Cement delivered yesterday. Available on-site."
    elif "brick" in material_type.lower():
        return "Brick delivery scheduled tomorrow morning."
    else:
        return f"{material_type} status not in system. Will check and call back."

@function_tool
async def get_team_update(work_type: str) -> str:
    """Gets an update on the labor, masons, or work crews on-site."""
    print(f"Tool called: get_team_update for work_type: {work_type}")
    return "15 workers on-site today. Both head masons present."

@function_tool
async def get_site_visit_slots(preferred_date: str) -> str:
    """Checks for available time slots for a client to visit the construction site."""
    print(f"Tool called: get_site_visit_slots for date: {preferred_date}")
    return f"11 AM slot for {preferred_date} is available. Booked for you."

# -------------------------------------------------------------------------
# IMPROVED SYSTEM PROMPT - Optimized for voice quality
# -------------------------------------------------------------------------

SYSTEM_PROMPT = """You are Rahul, a warm project manager at Riverwood Projects. Your goal is bond-building and accurate information.

🚨 CRITICAL VOICE QUALITY RULES 🚨

1. ULTRA-SHORT RESPONSES (1-2 sentences max)
    - Long responses = broken voice
    - Example: "Haan Sir, foundation complete ho gaya hai aur brickwork shuru ho raha hai."
    - NOT: Multiple paragraphs or long explanations

2. SPEAK WHILE TOOLS RUN (Hide latency)
    - NEVER say: "let me check", "one moment", "hold on"
    - ALWAYS say: "Aapka project check kar raha hoon Sir... [tool runs] ...haan bilkul!"
    - Keep talking to mask the tool call delay

3. MIRROR USER'S LANGUAGE
    - Hindi user → Reply in Hindi ONLY
    - English user → Reply in English ONLY
    - Hinglish user → Reply in Hinglish
    - Never switch languages mid-conversation

4. USE TOOLS, NEVER FAKE DATA
    - Always call tools for real data
    - If you need project_id, ask: "Sir aapka plot number kya hai?"
    - If you don't know: "Sir, yeh info mere paas nahi hai, main check karke call back karta hoon"

5. BE PROACTIVE AND ENGAGING
    - Always respond to what the user says
    - Ask follow-up questions
    - Don't just wait for specific commands

🗣️ CONVERSATION STYLE

Greetings:
- "Namaste Sir! Rahul bol raha hoon Riverwood Projects se. Aaj kaisa chal raha hai?"
- "Namaste Sir! Riverwood Projects, Rahul here. How's your day going?"

Bond-Building (Keep it brief):
- "Chai pi li aaj?" 
- "Site visit ka plan hai weekend?"
- "Garmi bahut hai, hydrated rahiye"

Reassurance:
- "Aap fikar mat kijiye"
- "Main dekh lunga"
- "Sab on track hai Sir"

🛠️ TOOLS (Call when needed)

1. get_project_update(project_id) - Construction progress
2. check_material_status(material_type) - Material delivery
3. get_team_update(work_type) - Labor/mason updates
4. get_site_visit_slots(preferred_date) - Visit scheduling

📅 CONTEXT
- Date: November 8, 2025
- Riverwood: 50+ workers, 5 experienced masons
- Current Phase: Foundation and brickwork

REMEMBER: Keep responses SHORT. One or two sentences maximum. This prevents voice breaking."""

# -------------------------------------------------------------------------
# LOGGING
# -------------------------------------------------------------------------

import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("riverwood-agent")

# -------------------------------------------------------------------------
# MAIN AGENT
# -------------------------------------------------------------------------

async def entrypoint(ctx: JobContext):
    logger.info("🚀 Starting Riverwood Agent...")
    await ctx.connect()
    logger.info("✅ Connected to LiveKit room")

    # IMPROVED CONFIGURATION FOR VOICE QUALITY
   # Near line 140
    # 1. LLM - Use Google Gemini (via the google plugin) with a temperature for natural responses
    # Use the google.LLM wrapper which supports Gemini models. This replaces the undefined
    # `GeminiLLM` reference and keeps the same model/temperature settings.
    llm = google.LLM(
        model="gemini-2.5-flash",  # recommended full model name
        temperature=0.7,    # More natural responses
    )

    # 2. STT - Deepgram with optimized settings for Hinglish
    stt = deepgram.STT(
        model="nova-2-general",
        language="multi",  # Critical for Hinglish
        interim_results=True,  # Faster response
        smart_format=True,  # Better punctuation
        keywords=[
            ("Riverwood", 2.5),
            ("Namaste", 2.5),
            ("chai", 2.0),
            ("project", 2.0),
            ("construction", 2.0),
            ("update", 2.0),
            ("foundation", 2.0),
            ("brickwork", 2.0),
            ("cement", 2.0),
            ("brick", 2.0),
            ("workers", 2.0),
            ("masons", 2.0),
            ("visit", 2.0),
            ("plot", 2.0),
        ]
    )

    # 3. TTS - ElevenLabs with WORKING voice ID
    tts = elevenlabs.TTS(
        # Use a standard voice ID that exists in all accounts
        voice_id="pNInz6obpgDQGcFmaJgB",  # Adam - a standard ElevenLabs voice
    )

    # 4. Create Agent with tools
    agent = Agent(
        instructions=SYSTEM_PROMPT,
        tools=[
            get_project_update,
            check_material_status,
            get_team_update,
            get_site_visit_slots
        ],
        llm=llm  # IMPORTANT: Connect LLM to agent
    )
    
    # 5. Create Session with minimal supported parameters
    try:
        logger.info("📞 Creating agent session...")
        
        session = AgentSession(
            llm=llm,
            stt=stt,
            tts=tts,
            allow_interruptions=True,  # User can interrupt
            # VAD completely removed
        )

        # Event logging for debugging
        def _on_user_input_transcribed(ev):
            try:
                if ev.is_final:
                    logger.info(f"🎤 User said: {ev.transcript}")
            except Exception as e:
                logger.error(f"Transcription error: {e}")

        def _on_conversation_item_added(ev):
            try:
                item = ev.item
                role = getattr(item, "role", "unknown")
                text = getattr(item, "text_content", None) or getattr(item, "content", "")
                
                if role == "assistant" and text:
                    logger.info(f"🤖 Agent said: {text}")
                elif role == "user" and text:
                    logger.info(f"👤 User message: {text}")
            except Exception as e:
                logger.error(f"Conversation item error: {e}")

        def _on_agent_response_started(ev):
            logger.info("🔄 Agent started processing response...")

        def _on_agent_response_finished(ev):
            logger.info("✅ Agent finished response")

        session.on("user_input_transcribed", _on_user_input_transcribed)
        session.on("conversation_item_added", _on_conversation_item_added)
        session.on("agent_response_started", _on_agent_response_started)
        session.on("agent_response_finished", _on_agent_response_finished)

        # 6. Start the session
        logger.info("▶️  Starting agent session...")
        await session.start(agent=agent, room=ctx.room)

        # 7. Initial greeting with slight delay - MAKE IT SHORT
        logger.info("👋 Sending initial greeting...")
        await asyncio.sleep(1.5)
        
        # SHORT greeting to test responsiveness
        await session.say("Namaste Sir! Rahul bol raha hoon Riverwood Projects se. Aapka din kaisa hai?")
        logger.warning("✅ Agent ready and waiting for user input")
        
        # Keep the session alive and listening
        try:
            while True:
                await asyncio.sleep(1)
        except asyncio.CancelledError:
            logger.info("Agent session cancelled")
    
    except Exception as e:
        logger.error(f"❌ Error in agent session: {str(e)}", exc_info=True)
        raise

# -------------------------------------------------------------------------
# RUN
# -------------------------------------------------------------------------

if __name__ == "__main__":
    # Load your LiveKit credentials from .env
    livekit_url = os.getenv("LIVEKIT_URL")
    livekit_key = os.getenv("LIVEKIT_API_KEY")
    livekit_secret = os.getenv("LIVEKIT_API_SECRET")

    if not (livekit_url and livekit_key and livekit_secret):
        raise SystemExit("Missing LiveKit credentials in .env (LIVEKIT_URL / LIVEKIT_API_KEY / LIVEKIT_API_SECRET)")

    # WorkerOptions without metadata
    opts = WorkerOptions(
        entrypoint_fnc=entrypoint,
        agent_name="riverwood-agent",
        ws_url=livekit_url,
        api_key=livekit_key,
        api_secret=livekit_secret,
    )

    cli.run_app(opts)
