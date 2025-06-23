from elevenlabs.client import ElevenLabs, AsyncElevenLabs
from elevenlabs import play, stream
import asyncio

client = ElevenLabs(api_key="sk_d8a182a0733c3aa8d7375ab85f1b24d79c29a40f0b154d16")

audio = client.text_to_speech.convert(
    text="Hello, world!",
    voice_id="JBFqnCBsd6RMkjVDRZzb",  # 원하는 보이스 ID
    model_id="eleven_flash_v2_5", # 또는 eleven_flash_v2_5, eleven_turbo_v2_5
    output_format="mp3_44100_128"
)

play(audio)

audio_stream = client.text_to_speech.stream(
    text="Streaming test",
    voice_id="JBFqnCBsd6RMkjVDRZzb",
    model_id="eleven_flash_v2_5"
)

stream(audio_stream)


async def print_models():
    eleven = AsyncElevenLabs(api_key="sk_d8a182a0733c3aa8d7375ab85f1b24d79c29a40f0b154d16")
    models = await eleven.models.list()
    print(models)

asyncio.run(print_models())