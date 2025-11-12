import asyncio
from dotenv import load_dotenv
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from livekit import agents
from livekit.agents import AgentSession, Agent, JobContext
from livekit.plugins import silero

load_dotenv()

# ------------------------------
# DeepSeek LLM setup
# ------------------------------
MODELS = {
    "llm": {
        "model_path": "/path/to/your/deepseek-model",  # <-- update this
        "device": "cuda"  # or "cpu"
    }
}

quantization_config = None  # Optional: Add if you want quantized weights

# Load model
model = AutoModelForCausalLM.from_pretrained(
    MODELS['llm'].get('model_path'),
    quantization_config=quantization_config,
    device_map="auto" if MODELS['llm']['device'] == "cuda" else None,
    torch_dtype=torch.float16 if MODELS['llm']['device'] == "cuda" else torch.float32,
    trust_remote_code=True,
    low_cpu_mem_usage=True
)

# Load tokenizer
tokenizer = AutoTokenizer.from_pretrained(
    MODELS['llm'].get('model_path'),
    trust_remote_code=True
)

# ------------------------------
# Silero STT & TTS setup
# ------------------------------
vad = silero.VAD.load()
stt = silero.STT.load()
tts = silero.TTS.load()

# ------------------------------
# Entrypoint for LiveKit agent
# ------------------------------
async def entrypoint(ctx: agents.JobContext):
    await ctx.connect()

    session = AgentSession(
        vad=vad,
        stt=stt,
        llm=model,  # DeepSeek LLM
        tts=tts
    )

    agent = Agent(instructions="You are a helpful offline voice assistant.")

    await session.start(room=ctx.room, agent=agent)

    # Example greeting
    await session.generate_reply(
        instructions="Greet the user and offer assistance."
    )


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))
