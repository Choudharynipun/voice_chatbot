# livekit_utils.py

import os
import time
import asyncio
from dotenv import load_dotenv

# Import the main components from the LiveKit Agent SDK
from livekit.agents import Agent, Room, TrackSource

# Import custom utilities for STT, LLM interaction, TTS, and metrics logging
from stt import transcribe_audio_chunk
from llm_agent import query_llm
from tts import synthesize_speech
from metrics_logger import log_metrics_to_excel

# ✅ Load environment variables securely from .env file
load_dotenv()
LIVEKIT_URL = os.getenv("LIVEKIT_URL")
LIVEKIT_API_KEY = os.getenv("LIVEKIT_API_KEY")
LIVEKIT_API_SECRET = os.getenv("LIVEKIT_API_SECRET")
LIVEKIT_ROOM_NAME = os.getenv("LIVEKIT_ROOM_NAME", "voice-room")
AGENT_ID = "voice-agent"

# 🔁 Main asynchronous function to start the agent
async def start_voice_agent():
    print("\n🤖 Initializing voice agent session...")

    # 🎯 Define a callback for handling audio input from the user
    async def on_audio_track(room: Room, track: TrackSource):
        print("🎧 Received an audio track from participant...")

        # 🔁 Stream audio chunks in real-time
        async for chunk in track:
            start_time = time.time()  # Timestamp at start of user utterance

            # 🔊 Convert speech to text
            user_text = transcribe_audio_chunk(chunk)
            print(f"📝 Transcribed Text: {user_text}")

            if not user_text.strip():
                print("⚠️ Empty input detected, skipping this chunk...\n")
                continue

            # 🧠 Send transcribed text to LLM and time the response
            llm_start = time.time()
            response_text = query_llm(user_text)
            llm_end = time.time()
            print(f"🤖 LLM Response: {response_text}")

            # 🗣️ Convert LLM response to speech
            tts_start = time.time()
            response_audio = synthesize_speech(response_text)
            tts_end = time.time()

            # 🔈 Publish synthesized audio back to the room
            await room.publish_audio(response_audio)
            print("🔊 Published response audio to LiveKit room.")

            end_time = time.time()

            # 📊 Log interaction metrics to an Excel file
            log_metrics_to_excel({
                "input_text": user_text,
                "response_text": response_text,
                "eou_delay": llm_start - start_time,  # End-of-utterance delay
                "ttft": llm_end - llm_start,          # Time-to-first-token
                "ttfb": tts_end - tts_start,          # Time-to-first-byte
                "total_latency": end_time - start_time
            })

            print("✅ Interaction completed and metrics logged.\n")

    # 🚀 Initialize LiveKit agent with credentials
    agent = Agent(
        agent_id=AGENT_ID,
        url=LIVEKIT_URL,
        api_key=LIVEKIT_API_KEY,
        api_secret=LIVEKIT_API_SECRET,
    )

    # 📡 Join the specified LiveKit room and assign the audio handler
    await agent.join(
        room_name=LIVEKIT_ROOM_NAME,
        auto_subscribe=True,
        on_audio_track=on_audio_track
    )

    print("🟢 Voice Agent is actively listening in the room...\n")

    # 🔄 Start the agent's event loop
    await agent.run()
