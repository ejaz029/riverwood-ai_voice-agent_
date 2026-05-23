# How to Test Your Voice Agent with Microphone

## ✅ EASIEST METHOD: Use LiveKit Playground

When you run your agent in dev mode, LiveKit automatically provides a web interface!

### Steps:

1. **Start your agent** (if not already running):
   ```bash
   python src/agent.py dev
   ```

2. **Look for the URL in the terminal output**. You should see something like:
   ```
   Dev mode enabled. Playground available at: https://agents-playground.livekit.io/#...
   ```

3. **Click that URL** or copy-paste it into your browser

4. **Allow microphone access** when prompted

5. **Start talking!** Say things like:
   - "Namaste Rahul"
   - "Hello, chai pee li?"
   - "Give me a construction update"

---

## Alternative Method 1: Use the Python Test Client

I've created a simple Python client for you:

```bash
python test_client.py
```

This will:
- Connect to your LiveKit room
- Enable your microphone
- Let you talk to Rahul

---

## Alternative Method 2: Use the Web Client

1. **Install Node.js dependencies** (one-time setup):
   ```bash
   npm install livekit-server-sdk
   ```

2. **Start the token server**:
   ```bash
   node token-server.js
   ```

3. **Open `client.html` in your browser**:
   - Just double-click the file, or
   - Use a local server: `python -m http.server 8000`
   - Then go to: http://localhost:8000/client.html

4. **Click "Connect & Talk"** and allow microphone access

---

## Troubleshooting

### "Agent only responds to text"
- Make sure you're using one of the methods above to connect with microphone
- The agent needs a **client** to send audio to it

### "No audio output"
- Check your browser's audio settings
- Make sure your speakers/headphones are working
- Check the browser console for errors (F12)

### "Microphone not working"
- Allow microphone permissions in your browser
- Check your system microphone settings
- Try a different browser (Chrome works best)

---

## What's Happening Behind the Scenes

1. **Your agent** (`python src/agent.py dev`) runs on your computer and waits for connections
2. **A client** (web browser or Python script) connects to the LiveKit room
3. **Your microphone audio** is sent to the agent
4. **Deepgram** converts your speech to text
5. **Gemini** generates a response
6. **ElevenLabs** converts the response to speech
7. **The audio** is sent back to your browser/client

---

## Quick Test

The **easiest way** is to just look at your terminal when you run:
```bash
python src/agent.py dev
```

You should see a **playground URL**. Click it and start talking! 🎤

