# voice-demo
try to run voice agent using local llm

1.]Install dependencies

pip install "livekit-agents[silero,cartesia,turn-detector]~=1.0"
pip install transformers torch python-dotenv
pip install git+https://github.com/snakers4/silero-models#egg=silero
pip install TTS sounddevice

pip install numpy


2.]Make sure your local DeepSeek model files are inside:

./models/deepseek/

3.]Changes to be done in code :
1.Replace "/path/to/your/deepseek-model" with the path where your DeepSeek LLM is stored.

2.If you are using CPU only, change "device": "cuda" to "device": "cpu".

3.Silero models allow you to run STT (speech-to-text) and TTS (text-to-speech) locally with no cloud dependencies.


4.]Run the agent



Run in console mode for quick local testing:

python my_agent.py console


This mode will use your microphone as input and speaker for output.

You should be able to speak to the agent and get voice responses.

For development with hot reload:

python my_agent.py dev


Starts a local LiveKit server session.

Changes in my_agent.py will automatically reload.

For production deployment:

python my_agent.py start



