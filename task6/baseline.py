from livekit.plugins import (
    cartesia,
    openai,
    deepgram,
    noise_cancellation,
    silero,
)
from livekit.agents import (
    Agent,
    AgentSession,
    RoomInputOptions,
    WorkerOptions,
    cli,
    JobContext,
    AutoSubscribe,
    JobProcess,
    metrics,
)

from config.settings import settings
from config.logger_config import logger
from services.chart_handler import plot_latency

def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()

async def entrypoint(ctx: JobContext):
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    participant = await ctx.wait_for_participant()
    logger.info(f"Starting voice assistant for participant {participant.identity}")

    def on_metrics_collected(agent_metrics: metrics.AgentMetrics):
        metrics_of_instance = agent_metrics.metrics
        if not metrics_of_instance:
            return
        try :
            speech_id = metrics_of_instance.speech_id
        except AttributeError:
            speech_id = None
        
        if not speech_id:
            return

        tracker = response_tracker.setdefault(speech_id, {})

        if metrics_of_instance.type == "eou_metrics":
            tracker["end_of_utterance_delay"] = metrics_of_instance.end_of_utterance_delay
        
        elif metrics_of_instance.type == "llm_metrics":
            tracker["llm_ttft"] = metrics_of_instance.ttft

        elif metrics_of_instance.type == "tts_metrics":
            eou_time = tracker.get("end_of_utterance_delay")
            llm_ttft = tracker.get("llm_ttft")
            tts_ttfb = metrics_of_instance.ttfb

            if eou_time is not None and llm_ttft is not None and tts_ttfb is not None:
                total_latency = eou_time + llm_ttft + tts_ttfb
                logger.info(f"EOU Time: {eou_time}, LLM TTFT: {llm_ttft}, TTS TTFB: {tts_ttfb}")
                logger.info(f"Total latency - {total_latency} seconds")
                latency_tracker.append([eou_time, llm_ttft, tts_ttfb, total_latency])
                plot_latency(latency_tracker)
            response_tracker.pop(speech_id, None)

    stt = deepgram.STT(model="nova", api_key=settings.DEEPGRAM_API_KEY, interim_results=False, no_delay=False)
    tts = cartesia.TTS(model="sonic-2", api_key=settings.CARTESIA_API_KEY, voice="78ab82d5-25be-4f7d-82b3-7ad64e5b85b2")

    agent = Agent(instructions="You are a voice assistant created by I-Stem.")
    
    session = AgentSession(
        stt=stt,
        tts=tts,
        llm=openai.LLM(model="gpt-4o-mini", api_key=settings.OPENAI_API_KEY),
        vad=ctx.proc.userdata["vad"],
        min_endpointing_delay=1.0,
        max_endpointing_delay=6.0,
        allow_interruptions=True
        )
    
    response_tracker = {}
    latency_tracker = []
    session.on("metrics_collected", on_metrics_collected)

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
            prewarm_fnc=prewarm,
        ),
    )