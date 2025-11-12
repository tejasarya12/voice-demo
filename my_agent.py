import asyncio
from dotenv import load_dotenv
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from livekit import agents
from livekit.agents import AgentSession, Agent, JobContext
from livekit.plugins import silero
from livekit.plugins import transformers as hf_transformers

load_dotenv()

# DeepSeek LLM setup

MODELS = {
    "llm": {
        "model_path": "/path/to/your/deepseek-model", 
        "device": "cuda"  
    }
}

quantization_config = None  

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



processor = hf_transformers.ChatProcessor(model=model, tokenizer=tokenizer)

# This is  DeepSeek template
processor.chat_template = (
    "{% for message in messages %}"
    "{% if message['role'] == 'user' %}"
    "user: {{ message['content'] }}\n\n"
    "{% elif message['role'] == 'assistant' %}"
    "assistant: {{ message['content'] }}\n\n"
    "{% endif %}"
    "{% endfor %}"
    "assistant:"
)


llm = hf_transformers.LLM(processor=processor)





vad = silero.VAD.load()
stt = silero.STT.load()
tts = silero.TTS.load()




async def entrypoint(ctx: agents.JobContext):
    await ctx.connect()

    session = AgentSession(
        vad=vad,
        stt=stt,
        llm=llm,  
        tts=tts
    )

    agent = Agent(instructions="You are a helpful offline voice assistant.")

    await session.start(room=ctx.room, agent=agent)

 
    await session.generate_reply(
        instructions="Greet the user and offer assistance."
    )


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))
