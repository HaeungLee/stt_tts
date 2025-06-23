# Voice Assistant with STT, LLM, and TTS

A voice assistant that uses Whisper for speech-to-text, Google's Gemma 3 (via Gemini API) for natural language processing, and ElevenLabs for text-to-speech.

## Features

- 🎙️ Real-time speech-to-text using Whisper
- 🧠 Natural language processing with Google's Gemma 3
- 🔊 High-quality text-to-speech with ElevenLabs
- 💬 Interactive voice conversation mode
- 🎧 Support for processing audio files
- 🎚️ Configurable settings for models and voices

## Prerequisites

- Python 3.8 or higher
- FFmpeg (required by Whisper)
- Google AI API key (for Gemma 3)
- ElevenLabs API key (for TTS)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd stt_tts
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install FFmpeg:
   - On Windows: Download from [FFmpeg website](https://ffmpeg.org/download.html) and add to PATH
   - On macOS: `brew install ffmpeg`
   - On Ubuntu/Debian: `sudo apt update && sudo apt install ffmpeg`

4. Create a `.env` file in the project root and add your API keys:
   ```
   # Google AI API Key (for Gemma 3)
   GOOGLE_API_KEY=your_google_api_key_here
   
   # ElevenLabs API Key (for TTS)
   ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
   
   # Optional: Customize voice and model
   # VOICE_ID=21m00Tcm4TlvDq8ikWAM  # Default: Rachel's voice
   # MODEL=eleven_multilingual_v2   # TTS model
   ```

## Usage

### Interactive Mode
Start an interactive voice conversation:
```bash
python src/main.py --mode interactive
```

### Process an Audio File
Process a pre-recorded audio file:
```bash
python src/main.py --mode file --audio path/to/your/audio.wav
```

### Command Line Options
```
--mode MODE           Run mode: interactive or file (default: interactive)
--audio AUDIO         Path to audio file to process (for file mode)
--stt-model MODEL     Whisper model size (tiny, base, small, medium, large) (default: base)
--duration DURATION   Recording duration in seconds (for interactive mode) (default: 5.0)
--voice VOICE_ID      Voice ID for TTS (default: Rachel's voice)
--model TTS_MODEL     TTS model to use (default: eleven_multilingual_v2)
```

## Project Structure

```
stt_tts/
│
├── src/
│   ├── __init__.py
│   ├── stt_whisper.py    # Speech-to-Text with Whisper
│   ├── gemma_client.py   # Gemma 3 API client
│   ├── tts_elevenlabs.py # Text-to-Speech with ElevenLabs
│   └── main.py           # Main application
│
├── config/              # Configuration directory
├── recordings/           # Saved audio recordings
├── output/               # Generated output files
│
├── .env.example         # Example environment variables
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Customization

### Changing the Voice
You can change the TTS voice by modifying the `VOICE_ID` in your `.env` file. To list available voices, run:
```bash
python -c "from src.tts_elevenlabs import ElevenLabsTTS; tts = ElevenLabsTTS(); print('Available voices:'); [print(f'{i+1}. {v[\"name\"]} (ID: {v[\"id\"]}') for i, v in enumerate(tts.list_voices()[:10])]"
```

### Using Different Models
- **STT Model**: Change the `--stt-model` parameter (tiny, base, small, medium, large)
- **LLM Model**: Modify the `model` parameter in `gemma_client.py`
- **TTS Model**: Change the `MODEL` in `.env` file

## Troubleshooting

### Common Issues
1. **Whisper not working**: Ensure FFmpeg is installed and in your system PATH
2. **API errors**: Verify your API keys are correct and have sufficient credits
3. **Audio device issues**: Check your microphone and speaker settings

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [OpenAI Whisper](https://github.com/openai/whisper) for speech recognition
- [Google AI](https://ai.google.dev/) for the Gemma 3 model
- [ElevenLabs](https://elevenlabs.io/) for high-quality text-to-speech
