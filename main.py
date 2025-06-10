from fastapi import FastAPI, UploadFile, File
from dotenv import load_dotenv
import os
import uuid
import time
import shutil
import asyncio
from livekit_utils import start_voice_agent
import sys
from agent import entrypoint
from livekit.agents import AgentWorker

if __name__ == "__main__":
    AgentWorker(entrypoint=entrypoint).run()


from stt import transcribe_audio
from llm_agent import query_llm
from tts import synthesize_speech
from metrics_logger import log_metrics_to_excel

load_dotenv()

# Creating a FastAPI app
app = FastAPI()

# Root route for health check
@app.get("/")
def root():
    print("GET / called - Backend is up.")
    return {"message": "Voice Agent backend is running."}


# POST endpoint to simulate one full voice agent session
@app.post("/run-session/")
async def run_session(audio: UploadFile = File(...)):
    """
    This endpoint simulates a complete pipeline:
    1. Accepts an audio file
    2. Transcribes it (STT)
    3. Sends transcription to LLM
    4. Converts LLM response to audio (TTS)
    5. Logs all the latency metrics to an Excel file
    """
    print("----- New Session Started -----")

    # Create a unique session ID
    session_id = str(uuid.uuid4())
    print(f"Session ID: {session_id}")

    # Save uploaded audio to a temporary file
    audio_file_path = f"temp_{session_id}.wav"
    with open(audio_file_path, "wb") as buffer:
        shutil.copyfileobj(audio.file, buffer)
    print(f"Uploaded audio file saved as: {audio_file_path}")

    # === Step 1: Transcribe Audio ===
    print("Starting speech-to-text (STT)...")
    stt_start = time.time()
    transcribed_text = transcribe_audio(audio_file_path)
    stt_end = time.time()
    eou_delay = stt_end - stt_start
    print(f"EOU Delay (STT time): {eou_delay:.2f} seconds")

    if not transcribed_text.strip():
        return {"error": "STT failed. Could not extract text from audio."}

    # === Step 2: Send to LLM ===
    print("Sending transcribed text to LLM...")
    llm_response, ttft = query_llm(transcribed_text)

    if not llm_response.strip():
        return {"error": "LLM failed to return a response."}

    # === Step 3: Convert LLM response to Speech ===
    print("Starting text-to-speech (TTS)...")
    tts_start = time.time()
    tts_output_path = synthesize_speech(llm_response, output_path=f"tts_{session_id}.wav")
    tts_end = time.time()
    ttfb = tts_end - tts_start
    print(f"TTS done. Time to First Byte (TTFB): {ttfb:.2f} seconds")

    # === Step 4: Log metrics ===
    total_latency = eou_delay + ttft + ttfb
    print(f"Total Session Latency: {total_latency:.2f} seconds")
    log_metrics_to_excel(session_id, eou_delay, ttft, ttfb, total_latency)

    # Clean up: delete temporary uploaded audio
    if os.path.exists(audio_file_path):
        os.remove(audio_file_path)

    return {
        "session_id": session_id,
        "input_transcription": transcribed_text,
        "llm_response": llm_response,
        "tts_audio_path": tts_output_path,
        "metrics": {
            "eou_delay": round(eou_delay, 2),
            "ttft": round(ttft, 2),
            "ttfb": round(ttfb, 2),
            "total_latency": round(total_latency, 2)
        }
    }

from livekit_utils import start_voice_agent_session
@app.get("/start-streaming/")
async def start_streaming():
    asyncio.create_task(start_voice_agent_session())
    return {
        "status": "✅ Voice agent session started successfully via LiveKit!",
        "note": "Please join the room in LiveKit Playground to test the conversation."
    }

@app.get("/run-agent/")
async def run_agent():
    asyncio.create_task(start_voice_agent())
    return {"status": "Voice agent is running and joined the room."}
