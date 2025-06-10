# agent.py

from dotenv import load_dotenv
from livekit.agents import Agent, AgentSession, AgentWorker
from livekit.agents import turn_detector
from livekit.plugins import deepgram, openai as lk_openai, elevenlabs

load_dotenv()

ROOM_NAME = "my-room"

async def entrypoint(session: AgentSession):
    """
    Called for each new user session in the room.
    """
    await session.connect()  # subscribe to user audio
    print("🟢 Agent session connected.")

    # Prepare Agent with custom instructions
    agent = Agent(
        instructions="You are a helpful voice assistant."
    )

    # Pipeline with interruption detection
    await session.start(
        room=session.room,
        agent=agent,
        stt=deepgram.STT(model="nova-3"),
        llm=lk_openai.LLM(model="gpt-3.5-turbo"),
        tts=elevenlabs.TTS(),
        vad=turn_detector.model(),
        allow_interruptions=True
    )

if __name__ == "__main__":
    AgentWorker(
        entrypoint=entrypoint,
        api_key=None,
        api_secret=None,
    ).run()
