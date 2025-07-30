from livekit.plugins import (
    cartesia,
    openai,
    deepgram,
    noise_cancellation,
)
from livekit.agents import (
    Agent,
    AgentSession,
    RoomInputOptions,
    WorkerOptions,
    cli,
    JobContext,
    AutoSubscribe
)

from config.settings import settings
from config.logger_config import logger


async def entrypoint(ctx: JobContext):
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    # Wait for the first participant to connect
    participant = await ctx.wait_for_participant()
    logger.info(f"Starting voice assistant for participant {participant.identity}")

    stt = deepgram.STT(model="nova", api_key=settings.DEEPGRAM_API_KEY)
    tts = cartesia.TTS(model="sonic-2", api_key=settings.CARTESIA_API_KEY, voice="78ab82d5-25be-4f7d-82b3-7ad64e5b85b2")

    agent = Agent(instructions="You are a voice assistant created by I-Stem. Your interface with users will be voice. You should use short and concise responses, and avoiding usage of unpronouncable punctuation. Always start by saying Howdy")
    
    session = AgentSession(
        stt=stt,
        tts=tts,
        llm=openai.LLM(model="gpt-4o-mini", api_key=settings.OPENAI_API_KEY),
        min_endpointing_delay=0.5,
        max_endpointing_delay=6.0,
        allow_interruptions=True
        )

    await session.start(
        room=ctx.room,
        agent=agent,
        room_input_options=RoomInputOptions(
            noise_cancellation=noise_cancellation.BVC()
            )
    )

if __name__ == "__main__":
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
        ),
    )