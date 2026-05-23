"""
Simple test client to connect to the LiveKit room with microphone
"""
import asyncio
import os
from dotenv import load_dotenv
from livekit import rtc, api

load_dotenv()

LIVEKIT_URL = os.getenv("LIVEKIT_URL")
LIVEKIT_API_KEY = os.getenv("LIVEKIT_API_KEY")
LIVEKIT_API_SECRET = os.getenv("LIVEKIT_API_SECRET")


async def main():
    print("🎙️ Starting LiveKit Voice Client...")
    print("This will connect you to Rahul, the voice agent")
    print("-" * 50)
    
    # Generate a room name
    room_name = f"test-room-{os.urandom(4).hex()}"
    
    # Create access token
    token = api.AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET)
    token.with_identity("test-user").with_name("Test User").with_grants(
        api.VideoGrants(
            room_join=True,
            room=room_name,
            can_publish=True,
            can_subscribe=True,
        )
    )
    
    jwt_token = token.to_jwt()
    
    print(f"✅ Room: {room_name}")
    print(f"✅ Connecting to: {LIVEKIT_URL}")
    print("-" * 50)
    
    # Create room
    room = rtc.Room()
    
    @room.on("participant_connected")
    def on_participant_connected(participant: rtc.RemoteParticipant):
        print(f"👤 Participant connected: {participant.identity}")
        if "agent" in participant.identity.lower():
            print("🤖 Rahul (Agent) has joined! Start speaking...")
    
    @room.on("track_subscribed")
    def on_track_subscribed(
        track: rtc.Track,
        publication: rtc.RemoteTrackPublication,
        participant: rtc.RemoteParticipant,
    ):
        print(f"🔊 Subscribed to {participant.identity}'s track: {track.kind}")
        if track.kind == rtc.TrackKind.KIND_AUDIO:
            # Play the audio
            audio_stream = rtc.AudioStream(track)
            asyncio.create_task(play_audio(audio_stream))
    
    @room.on("track_unsubscribed")
    def on_track_unsubscribed(
        track: rtc.Track,
        publication: rtc.RemoteTrackPublication,
        participant: rtc.RemoteParticipant,
    ):
        print(f"Track unsubscribed: {track.sid}")
    
    # Connect to room
    try:
        await room.connect(LIVEKIT_URL, jwt_token)
        print("✅ Connected to room!")
        
        # Publish microphone
        print("🎤 Enabling microphone...")
        
        # Get audio source from microphone
        source = rtc.AudioSource(24000, 1)
        track = rtc.LocalAudioTrack.create_audio_track("microphone", source)
        options = rtc.TrackPublishOptions()
        options.source = rtc.TrackSource.SOURCE_MICROPHONE
        
        await room.local_participant.publish_track(track, options)
        print("✅ Microphone enabled! You can now speak...")
        print("\n💬 Say something like:")
        print("   - 'Namaste Rahul'")
        print("   - 'Hello, chai pee li?'")
        print("   - 'Construction update do'")
        print("\nPress Ctrl+C to disconnect\n")
        
        # Keep the connection alive
        while True:
            await asyncio.sleep(1)
            
    except KeyboardInterrupt:
        print("\n👋 Disconnecting...")
        await room.disconnect()
        print("✅ Disconnected!")
    except Exception as e:
        print(f"❌ Error: {e}")
        await room.disconnect()


async def play_audio(audio_stream: rtc.AudioStream):
    """Play audio from the stream"""
    async for frame in audio_stream:
        # In a real implementation, you'd play this audio
        # For now, we just acknowledge we're receiving it
        pass


if __name__ == "__main__":
    asyncio.run(main())

